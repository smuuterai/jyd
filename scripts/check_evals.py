#!/usr/bin/env python3
"""Static health check for the tiktok-product-video skill.

This script does not judge creative quality. It catches packaging and workflow
regressions that would make the skill harder to install, discover, or operate.
"""

from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def report(kind: str, message: str) -> None:
    print(f"{kind}: {message}")


def fail(message: str) -> None:
    report("FAIL", message)
    raise SystemExit(1)


def main() -> int:
    failures = 0
    warnings = 0

    def check(condition: bool, message: str, *, warning: bool = False) -> None:
        nonlocal failures, warnings
        if condition:
            report("PASS", message)
        elif warning:
            warnings += 1
            report("WARN", message)
        else:
            failures += 1
            report("FAIL", message)

    skill_path = ROOT / "SKILL.md"
    readme_path = ROOT / "README.md"
    evals_path = ROOT / "evals" / "evals.json"
    examples_dir = ROOT / "examples"
    golden_example_path = examples_dir / "pet-grooming-brush-brazil.md"

    check(skill_path.exists(), "SKILL.md exists at skill root")
    check(readme_path.exists(), "README.md exists at skill root")
    check(evals_path.exists(), "evals/evals.json exists")
    check(examples_dir.exists(), "examples/ directory exists")
    check(golden_example_path.exists(), "golden example exists: examples/pet-grooming-brush-brazil.md")

    if not skill_path.exists():
        fail("cannot continue without SKILL.md")

    skill_text = skill_path.read_text(encoding="utf-8")

    required_terms = [
        "先确认，再出全量",
        "先选生成路线",
        "即梦版 + Veo 版",
        "剪辑执行表",
        "素材回看验收",
        "合规提醒",
    ]
    for term in required_terms:
        check(term in skill_text, f"SKILL.md contains workflow term: {term}")

    required_files = [
        golden_example_path,
        ROOT / "references" / "controlled-generation-framework.md",
        ROOT / "references" / "failure-modes-cheatsheet.md",
        ROOT / "references" / "video-deconstruction.md",
        ROOT / "references" / "seedance2-multimodal.md",
        ROOT / "references" / "working-notes.md",
        ROOT / "references" / "subject-and-realism.md",
        ROOT / "references" / "cover-and-poster.md",
        ROOT / "references" / "voiceover-srt.md",
        ROOT / "references" / "testimonial-ugc.md",
        ROOT / "references" / "long-form-video.md",
        ROOT / "references" / "hook-library.md",
        ROOT / "references" / "ai-avatar.md",
        ROOT / "references" / "luxury-aesthetic.md",
        ROOT / "scripts" / "video_deconstruct.py",
    ]
    for path in required_files:
        check(path.exists(), f"required asset exists: {path.relative_to(ROOT)}")

    if evals_path.exists():
        try:
            data = json.loads(evals_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            failures += 1
            report("FAIL", f"evals/evals.json parses as JSON: {exc}")
        else:
            evals = data.get("evals", [])
            check(isinstance(evals, list) and len(evals) >= 3, "at least 3 eval prompts are defined")
            for idx, item in enumerate(evals, start=1):
                prefix = f"eval #{idx}"
                check(bool(item.get("id")), f"{prefix} has id")
                check(bool(item.get("prompt")), f"{prefix} has prompt")
                check(bool(item.get("expected_output")), f"{prefix} has expected_output")
                check(isinstance(item.get("files", []), list), f"{prefix} files is a list")
            linked_files = {
                file_name
                for item in evals
                for file_name in item.get("files", [])
                if isinstance(file_name, str)
            }
            check(
                "examples/pet-grooming-brush-brazil.md" in linked_files,
                "evals link to the golden example",
            )

    check(shutil.which("ffmpeg") is not None, "ffmpeg available for video_deconstruct.py", warning=True)
    check(shutil.which("ffprobe") is not None, "ffprobe available for video_deconstruct.py", warning=True)

    print("")
    print(f"Summary: {failures} failure(s), {warnings} warning(s)")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
