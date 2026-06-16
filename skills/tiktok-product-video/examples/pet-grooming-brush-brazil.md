# Example: Brazil TikTok Pet Grooming Brush

> Golden sample for `evals/evals.json` prompt #1. This is a representative expected output shape, not a performance claim or a live ad result.

## Input

```text
我想在巴西 TikTok 上卖一款宠物开结梳（蓝灰色双排不锈钢刀片、浮动刀头、防滑手柄，约17.5cm），用即梦做一条15秒的视频，帮我出一套完整方案。
```

## 0. Route Decision

Recommended route: **B · 逐镜分镜（逐镜 + 剪辑）**.

Reason: the product is a hard-detail tool with visible blades, handle texture, and a specific colorway. Product close-ups should be locked with a real product image or generated still reference, while the pet-use scenes can stay medium distance to avoid product deformation.

Style track: **原生直拍流**. The video should feel like a Brazilian pet owner filming at home, not a polished TV commercial.

## 1. 痒点 & 卖点

- 痒点：长毛宠物脖子和肚子下面容易打结，普通梳子一拉就疼，宠物会躲。
- 主打利益点：双排不锈钢刀片 + 浮动刀头，轻轻滑过就能把结梳开，减少拉扯感。
- 一句话定位：为巴西长毛猫狗主人解决“毛结拉疼、越梳越烦”的日常护理问题。

## 2. 15 秒脚本结构

| 时间 | 作用 | 画面 | 素材来源 |
|---|---|---|---|
| 0-2s | 钩子 | 巴西家庭客厅里，一只长毛狗脖子下有一小块明显毛结，主人拿普通白色旧梳子轻碰，狗立刻躲开 | AI 静图 + 轻微图生视频 |
| 2-4s | 产品登场 | 蓝灰色双排开结梳放在手心，刀片和防滑手柄清楚可见 | 真实产品图 / 首帧图生视频 |
| 4-9s | 核心爽点 | 主人沿顺毛方向轻轻滑过一小段毛结，镜头中远景，不给产品硬特写 | AI 图生视频 |
| 9-12s | 结果证明 | 梳齿上挂着一小撮毛，狗的脖子毛顺了，狗平静坐着 | 结果静图 + 轻微推近 |
| 12-15s | 收口 | 主人把梳子放在宠物旁边，宠物贴近镜头，字幕 CTA | AI 图生视频 + 后期字幕 |

镜头数量建议：3 段叙事视频 + 1 个结果特写插入。核心爽点段不能省。

## 3. 分镜提示词（即梦 + Veo）

### 镜头 1 · 痛点钩子 · 2s

**即梦首帧图**

```text
9:16 vertical phone photo, Brazilian home living room with warm natural window light, realistic lived-in background. A long-haired medium-size dog sits on a light sofa, head facing left, neck fur has one small visible tangled patch under the collar area. A human hand holds an old white plastic comb near the tangled patch, the comb is clearly old and different from the promoted product. The dog pulls its head slightly away, ears tense, uncomfortable but not harmed. Candid phone-shot realism, deep focus, slight handheld imperfection, natural skin and fur texture. No text, no logo, no watermark.
```

**即梦图生视频**

```text
中景，固定手机机位，轻微手持晃动。画面里始终只有一只长毛狗，狗头朝左、尾部朝右。主人手里的白色旧梳子从狗脖子下方的毛结旁边轻轻靠近，不真正拉扯；狗轻微后缩并转头躲开，动作约2秒完成。毛结只是一小块，不增加、不扩散。避免：主推蓝灰色开结梳出现在本镜、毛结突然变多、狗表情痛苦夸张、多出第二只狗、画面文字、logo、水印。
```

**Veo version**

```text
A vertical candid smartphone shot inside a Brazilian living room. A long-haired dog sits on a sofa, head turned left, with one small tangled patch visible under the neck fur. A hand brings an old white plastic comb close to the knot, and the dog gently pulls away, showing mild discomfort without distress. Natural window light, realistic home details, subtle handheld movement, no on-screen text, no logo, no watermark.
```

**易翻车点**：旧梳子必须和主推产品颜色/形态拉开，否则观众会误以为主推产品不好用。

### 镜头 2 · 产品登场 · 2s

**即梦首帧图**

```text
9:16 vertical close-up phone photo of one blue-gray pet dematting comb held in a human palm. Product details: blue-gray ergonomic anti-slip handle, floating cutter head, double rows of stainless steel curved blades, compact size around 17.5 cm, handle below and blade head above. Clean natural window light, simple Brazilian home background softly visible, realistic product texture, sharp focus. No extra tools, no text, no logo, no watermark.
```

**即梦图生视频**

```text
产品中近景，固定机位，产品外观、刀片数量、蓝灰色手柄、防滑纹理、浮动刀头全程保持与首帧完全一致。镜头只允许自然光从左到右轻轻扫过不锈钢刀片，产品本体不旋转、不翻面、不变形，手掌保持稳定。约2秒，真实手机直拍质感。避免：产品旋转超过20度、刀片数量增减、手柄颜色变化、出现乱码文字、logo、水印。
```

**Veo version**

```text
A vertical close-up image-to-video shot using the product still as the first frame. The blue-gray pet dematting comb rests steadily in a hand, showing the anti-slip handle, floating cutter head, and double rows of stainless steel curved blades. The camera stays still while soft daylight glides across the metal blades. Keep the product shape, color, blade count, and proportions perfectly consistent. No rotation, no text, no watermark.
```

**易翻车点**：硬细节产品不能转身展示背面；没有背面参考图就不要让模型编。

### 镜头 3 · 使用过程 · 5s

**即梦首帧图**

```text
9:16 vertical medium shot, same Brazilian living room. The same long-haired dog sits calmly, head facing left, owner hand holds the blue-gray dematting comb near the neck fur. The product appears at medium distance, not a close-up. Fur direction is clear from neck toward shoulder. Natural window light, candid phone-shot realism, no text, no logo, no watermark.
```

**即梦图生视频**

```text
中景，固定手机机位，画面始终只有一只长毛狗。狗头朝左、尾朝右，主人手持蓝灰色双排开结梳，从画面左侧狗脖子下方沿顺毛方向缓慢滑到右侧肩部，约5秒完成一次轻柔梳理。产品只保持中远景，不给刀片特写；重点是动作轻、狗平静。毛发在梳过后自然顺向平伏，出现轻微光泽。避免：梳出大量毛、毛发喷涌、产品变形、刀片数量变化、狗突然站起、多出第二只狗、文字、水印。
```

**Veo version**

```text
A vertical medium smartphone shot in the same Brazilian living room. The long-haired dog remains calm, head facing left. A hand gently guides the blue-gray dematting comb along the direction of the fur, from the neck area toward the shoulder, completing one slow pass over about five seconds. Keep the comb at medium distance, not a product close-up. The fur settles smoother after the pass, with a soft natural shine. No large clumps appearing during the motion, no extra animals, no on-screen text.
```

**易翻车点**：不要写“梳出大量毛发”。累积效果交给结果特写，不让视频连续生成。

### 镜头 4 · 结果证明 + CTA · 6s

**结果静图提示词**

```text
9:16 vertical phone photo close-up. The same blue-gray dematting comb is held near the dog, and the comb teeth carry one small loose tuft of fur, not a huge pile. In the background, the dog sits relaxed with smoother neck fur. Natural Brazilian home light, candid phone-shot realism, clean composition with empty upper area for later subtitle. No generated text, no logo, no watermark.
```

**即梦图生视频**

```text
中近景，固定机位，使用结果静图作为首帧。产品外形保持完全一致，梳齿上只有一小撮松散毛发。镜头极缓慢推近约10%，狗在背景中平静眨眼，毛发顺滑。不要让毛团变大，不要生成新毛发，不要让产品旋转。画面上方留字幕空间。无任何文字、logo、水印。
```

**Veo version**

```text
A vertical image-to-video result shot. The blue-gray dematting comb is held near the dog, with one small loose tuft of fur caught in the teeth. The dog sits relaxed in the background, neck fur visibly smoother. The camera slowly pushes in by about ten percent. Keep the product consistent and the fur tuft small. Leave clean space at the top for subtitles added later. No on-screen text.
```

**易翻车点**：毛团只要“一小撮”，太大就会糊，也会显假。

## 4. 巴西本地化文案

| 用途 | 葡语文案 | 中文回译 |
|---|---|---|
| 钩子字幕 | Seu pet foge quando vê a escova? | 你家宠物一看到梳子就躲吗？ |
| 痛点字幕 | Nó no pelo machuca e irrita. | 毛结会拉疼，也会让宠物烦躁。 |
| 卖点字幕 | Duas fileiras de lâminas para desembaraçar sem puxar tanto. | 双排刀片，开结时没那么拉扯。 |
| 结果字幕 | Pelo mais solto em poucos segundos. | 几秒钟毛就顺很多。 |
| CTA | Clique e veja a oferta de hoje. | 点击看看今天优惠。 |

话题标签：

```text
#petsbrasil #cachorrofeliz #cuidadoscompet #petshopbrasil #escovaparapet #tiktokmademebuyit
```

BGM 建议：去巴西 TikTok 热榜找轻快、家居感、宠物类常用的 pop / funk leve 曲风；不要用过于激烈的 phonk，避免宠物护理画面显得粗暴。

## 5. 剪辑执行表

### 5.1 切点转场表

| 切点 | 时间码 | 转场类型 | 落点 | 配套音效 |
|---|---|---|---|---|
| 镜头1 -> 镜头2 | 2.0s | 白闪 2 帧 + whoosh | 狗躲开瞬间 | light whoosh |
| 镜头2 -> 镜头3 | 4.0s | 尾帧承接；产品从手心位置进入使用镜 | BGM 第 2 个重拍 | soft pop |
| 镜头3 -> 镜头4 | 9.0s | 蒙太奇硬切到结果特写 | 梳理动作结束后一拍 | small click |
| 镜头4 收尾 | 15.0s | 无转场，定格 0.3s | CTA 出现 | subtle chime |

### 5.2 音乐 cue 表

| 音轨 | 入点-出点 | 内容 | 音量 |
|---|---|---|---|
| BGM | 0-15s | 巴西区轻快 pet/lifestyle pop | 无口播可正常音量；有口播压到 -16dB |
| SFX | 2.0s | whoosh | 比 BGM 高 3dB |
| SFX | 4.0s | soft pop | 比 BGM 高 2dB |
| SFX | 9.0s | small click | 比 BGM 高 3dB |

第一步先关掉 AI 视频原声，只保留后期 BGM / SFX / 字幕。

### 5.3 字幕逐条表

| # | 起止 | 字幕 | 位置 | 样式 |
|---|---|---|---|---|
| 1 | 0.0-2.0s | Seu pet foge quando vê a escova? | 顶部 22% | 白字黑描边，`foge` 用蓝灰色高亮 |
| 2 | 2.0-4.0s | Desembaraça sem drama. | 底部 18% | 粗体，短句弹入 |
| 3 | 4.0-9.0s | Passa leve. Sem puxar tanto. | 顶部 25% | 分两行，`leve` 放大 1.2x |
| 4 | 9.0-12.0s | Olha o resultado. | 顶部 22% | 随节拍淡入 |
| 5 | 12.0-15.0s | Clique e veja a oferta de hoje. | 底部 18%，安全区内 | CTA 黄色描边 |

### 5.4 导出参数

- 9:16
- 1080x1920
- 30fps 或更高
- MP4 / H.264
- 手动确认 CapCut / 剪映导出不是 720P

## 6. 合规提醒

- 不写“100% 无痛”“永久解决”等绝对化承诺。
- 不暗示治疗皮肤病或兽医功效；只说日常护理和梳理体验。
- 产品效果要和实物一致，刀片数量、颜色、尺寸不要夸大。
- AI 生成素材按平台要求标注。

