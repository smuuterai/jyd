#!/usr/bin/env python3
"""
video_deconstruct.py — 对参考视频做"基于画面+声音的二次拆解"预处理。

在输出目录生成：
  info.json            ffprobe 元数据（时长、分辨率、帧率、音轨）
  frames/              每秒 1 帧（frame_0001.jpg ...）
  scenes/              转场/镜头切换帧（best-effort）
  grid.jpg             1fps 帧拼成的网格图，便于快速扫描画面变化
  audio.wav            提取的音频（若有音轨，单声道 16k）
  audio_analysis.json  静音/响度粗判（人声/BGM 是否存在的代理指标）
  transcript.txt       若装了 whisper/faster-whisper 则转写口播，否则写明不可用
  report.md            汇总，并提示下一步（喂给 references/video-deconstruction.md 做分析）

依赖：ffmpeg + ffprobe 必须在 PATH 上。
可选：faster-whisper 或 openai-whisper（用于自动转写口播）。

用法：
  python video_deconstruct.py <视频路径> [-o 输出目录] [--scene-threshold 0.3]
"""
import argparse
import json
import math
import re
import shutil
import subprocess
import sys
from pathlib import Path


def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")


def need(tool):
    if shutil.which(tool) is None:
        sys.exit(
            f"ERROR: 未找到 '{tool}'（需要 ffmpeg，含 ffprobe）。请先安装：\n"
            f"  Windows: winget install Gyan.FFmpeg\n"
            f"  macOS:   brew install ffmpeg\n"
            f"  Linux:   sudo apt install ffmpeg"
        )


def ffprobe_info(video: Path) -> dict:
    r = run(["ffprobe", "-v", "quiet", "-print_format", "json",
             "-show_format", "-show_streams", str(video)])
    if r.returncode != 0:
        sys.exit("ffprobe 失败：" + r.stderr)
    data = json.loads(r.stdout)
    streams = data.get("streams", [])
    fmt = data.get("format", {})
    vid = next((s for s in streams if s.get("codec_type") == "video"), None)
    auds = [s for s in streams if s.get("codec_type") == "audio"]

    info = {"filename": video.name, "duration_sec": round(float(fmt.get("duration", 0) or 0), 2)}
    if vid:
        info["width"], info["height"] = vid.get("width"), vid.get("height")
        fr = vid.get("avg_frame_rate") or vid.get("r_frame_rate") or "0/1"
        try:
            n, d = fr.split("/")
            info["fps"] = round(float(n) / float(d), 3) if float(d) else None
        except Exception:
            info["fps"] = None
        info["video_codec"] = vid.get("codec_name")
        if info.get("width") and info.get("height"):
            info["aspect"] = f'{info["width"]}x{info["height"]}'
            info["orientation"] = "竖屏(9:16类)" if info["height"] > info["width"] else "横屏/方形"
    info["audio_tracks"] = len(auds)
    info["audio_codec"] = auds[0].get("codec_name") if auds else None
    return info


def extract_frames(video: Path, outdir: Path):
    fdir = outdir / "frames"
    fdir.mkdir(parents=True, exist_ok=True)
    run(["ffmpeg", "-y", "-i", str(video), "-vf", "fps=1", "-q:v", "3",
         str(fdir / "frame_%04d.jpg")])
    return sorted(fdir.glob("frame_*.jpg"))


def extract_scenes(video: Path, outdir: Path, threshold: float):
    sdir = outdir / "scenes"
    sdir.mkdir(parents=True, exist_ok=True)
    run(["ffmpeg", "-y", "-i", str(video),
         "-vf", f"select='gt(scene,{threshold})',showinfo",
         "-vsync", "vfr", "-q:v", "3", str(sdir / "scene_%04d.jpg")])
    return sorted(sdir.glob("scene_*.jpg"))


def make_grid(frames, outdir: Path, cols: int = 5, tile_w: int = 320):
    if not frames:
        return None
    rows = math.ceil(len(frames) / cols)
    fdir = frames[0].parent
    grid = outdir / "grid.jpg"
    r = run(["ffmpeg", "-y", "-start_number", "1", "-framerate", "1",
             "-i", str(fdir / "frame_%04d.jpg"),
             "-vf", f"scale={tile_w}:-1,tile={cols}x{rows}:padding=4:color=white",
             "-frames:v", "1", str(grid)])
    return grid if grid.exists() else None


def extract_audio(video: Path, outdir: Path, has_audio: bool):
    if not has_audio:
        return None
    a = outdir / "audio.wav"
    run(["ffmpeg", "-y", "-i", str(video), "-vn", "-ac", "1", "-ar", "16000", str(a)])
    return a if a.exists() else None


def audio_stats(video: Path, has_audio: bool) -> dict:
    if not has_audio:
        return {"has_audio": False, "note": "无音轨"}
    r = run(["ffmpeg", "-i", str(video),
             "-af", "silencedetect=noise=-30dB:d=0.5,volumedetect",
             "-f", "null", "-"])
    err = r.stderr or ""
    mean = re.search(r"mean_volume:\s*(-?[\d.]+) dB", err)
    maxv = re.search(r"max_volume:\s*(-?[\d.]+) dB", err)
    silences = re.findall(r"silence_duration:\s*([\d.]+)", err)
    total_sil = round(sum(float(x) for x in silences), 2) if silences else 0.0
    stats = {
        "has_audio": True,
        "mean_volume_db": float(mean.group(1)) if mean else None,
        "max_volume_db": float(maxv.group(1)) if maxv else None,
        "silence_segments": len(silences),
        "total_silence_sec": total_sil,
    }
    # 粗略提示（仅供参考，分析时请标注不确定）
    if stats["mean_volume_db"] is not None:
        if stats["mean_volume_db"] > -22 and total_sil < 1.5:
            stats["hint"] = "音频持续且较满 → 很可能有 BGM 或连续口播（不确定）"
        elif stats["silence_segments"] >= 3:
            stats["hint"] = "存在多段静音 → 可能是分段口播/有停顿（不确定）"
        else:
            stats["hint"] = "音频特征一般，请结合画面判断（不确定）"
    return stats


def transcribe(audio, outdir: Path):
    out = outdir / "transcript.txt"
    if audio is None:
        out.write_text("（无音轨，无口播可转写）", encoding="utf-8")
        return
    # 1) faster-whisper（优先 GPU，失败回退 CPU；很多机器无 CUDA 必须用 CPU）
    def _fw(device):
        from faster_whisper import WhisperModel  # type: ignore
        model = WhisperModel("base", device=device, compute_type="int8")
        segments, info = model.transcribe(str(audio), vad_filter=True)
        lines = [f"[{s.start:.1f}-{s.end:.1f}] {s.text.strip()}" for s in segments]
        header = f"LANG: {info.language} ({info.language_probability:.2f})\n"
        return header + ("\n".join(lines) or "（未识别到清晰语音）")
    try:
        try:
            text = _fw("cuda")
        except Exception:
            text = _fw("cpu")
        out.write_text(text, encoding="utf-8")
        return
    except Exception:
        pass
    # 2) openai-whisper
    try:
        import whisper  # type: ignore
        model = whisper.load_model("base")
        res = model.transcribe(str(audio))
        out.write_text(res.get("text", "").strip() or "（未识别到清晰语音）", encoding="utf-8")
        return
    except Exception:
        pass
    # 3) 不可用
    out.write_text(
        "（转写不可用：未安装 whisper / faster-whisper。）\n"
        "请在分析时根据音频特征(audio_analysis.json)与画面做近似判断，并明确标注\"不确定\"。\n"
        "如需自动转写：pip install faster-whisper  然后重跑本脚本。",
        encoding="utf-8",
    )


def write_report(outdir: Path, info, frames, scenes, grid, audio, astats):
    report = outdir / "report.md"
    lines = [
        f"# 预处理结果：{info.get('filename')}",
        "",
        "## 基础信息",
        f"- 时长：{info.get('duration_sec')} 秒",
        f"- 分辨率：{info.get('aspect')}（{info.get('orientation')}）",
        f"- 帧率：{info.get('fps')} fps",
        f"- 音轨：{info.get('audio_tracks')} 条（{info.get('audio_codec')}）",
        "",
        "## 产物",
        f"- 每秒帧：{len(frames)} 张 → frames/",
        f"- 转场帧：{len(scenes)} 张 → scenes/",
        f"- 网格图：{'grid.jpg' if grid else '未生成'}",
        f"- 音频：{'audio.wav' if audio else '无'}",
        f"- 音频粗判：{astats.get('hint', astats.get('note',''))}",
        f"- 口播转写：见 transcript.txt",
        "",
        "## 下一步",
        "把 grid.jpg（和需要的逐帧/转场帧）连同 transcript.txt、audio_analysis.json，",
        "按 references/video-deconstruction.md 的七段格式做完整拆解。",
        "无法确认的声音/字幕，务必标注\"不确定\"。",
    ]
    report.write_text("\n".join(lines), encoding="utf-8")
    return report


def main():
    ap = argparse.ArgumentParser(description="参考视频二次拆解预处理")
    ap.add_argument("video", type=Path)
    ap.add_argument("-o", "--outdir", type=Path, default=None)
    ap.add_argument("--scene-threshold", type=float, default=0.3)
    ap.add_argument("--grid-cols", type=int, default=5)
    args = ap.parse_args()

    need("ffmpeg")
    need("ffprobe")
    if not args.video.exists():
        sys.exit(f"找不到视频：{args.video}")

    outdir = args.outdir or args.video.with_suffix("").parent / (args.video.stem + "_deconstruct")
    outdir.mkdir(parents=True, exist_ok=True)

    print("[1/6] 读取信息 ...")
    info = ffprobe_info(args.video)
    (outdir / "info.json").write_text(json.dumps(info, ensure_ascii=False, indent=2), encoding="utf-8")

    print("[2/6] 每秒抽帧 ...")
    frames = extract_frames(args.video, outdir)

    print("[3/6] 转场帧 ...")
    scenes = extract_scenes(args.video, outdir, args.scene_threshold)

    print("[4/6] 拼网格图 ...")
    grid = make_grid(frames, outdir, cols=args.grid_cols)

    has_audio = info.get("audio_tracks", 0) > 0
    print("[5/6] 抽音频 + 粗判 ...")
    audio = extract_audio(args.video, outdir, has_audio)
    astats = audio_stats(args.video, has_audio)
    (outdir / "audio_analysis.json").write_text(json.dumps(astats, ensure_ascii=False, indent=2), encoding="utf-8")

    print("[6/6] 转写口播（best-effort）...")
    transcribe(audio, outdir)

    report = write_report(outdir, info, frames, scenes, grid, audio, astats)
    print(f"\n完成 → {outdir}")
    print(f"  帧 {len(frames)} | 转场 {len(scenes)} | 网格 {'✓' if grid else '✗'} | 音频 {'✓' if audio else '✗'}")
    print(f"  先看 {report.name} 和 grid.jpg，再按 references/video-deconstruction.md 做七段拆解。")


if __name__ == "__main__":
    main()
