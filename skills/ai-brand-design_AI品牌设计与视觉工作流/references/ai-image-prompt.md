# AI 图像生成 Prompt 方法论

## 七维 Prompt 构建框架

> 给 AI 画画的 prompt 不是散文诗，是**导演分镜脚本**。每个维度都是一个必须回答的问题，缺了就会产生随机噪声。

| 维度 | 核心问题 | 示例 |
|------|---------|------|
| **主体** | 画面里是谁/是什么？ | `"一只戴着巫师帽的机器人"`（海报用引号括住核心内容） |
| **动作** | 发生了什么？ | `正在赛博朋克街道上奔跑` |
| **场景** | 故事发生在哪里？ | `霓虹灯映照的未来城市小巷，地面有积水倒影` |
| **风格** | 是拍出来的还是画出来的？ | `拍立得胶片风`、`日系赛博朋克`、`水彩手绘`、`3D 渲染` |
| **构图** | 导演视角的把控 | `极度特写`、`超广角俯视`、`三分法构图`、`对称中心构图` |
| **光线** | 给它打什么光？ | `丁达尔光效`、`冷色调霓虹灯`、`黄金时段暖光`、`伦勃朗光` |
| **细节** | 决定质感的咒语 | `8k 分辨率`、`工业级细节`、`电影级调色`、`浅景深` |

**注意**：很多教程里"构图"和"光线"会写反。记住：
- **构图 = 视角/取景**（镜头在哪里、怎么拍）
- **光线 = 光源/色调**（光从哪来、什么颜色、什么质感）

---

## 维度详解

### 1. 主体（Subject）—— 画面主角

**规则**：
- 海报/宣发图：用引号 `""` 把核心内容括住，确保 AI 识别为画面主体
- 品牌相关：主体应包含品牌角色/IP/产品
- 避免模糊描述：`"一个科技感的图"` ❌ → `"一台发光的量子计算机"` ✅

**示例**：
```
"A robot wizard holding a glowing magic wand"
"一台复古打字机，上面坐着穿巫师袍的小机器人"
```

### 2. 动作（Action）—— 叙事驱动力

**规则**：
- 静态图也需要"动作"——哪怕是"凝视"、"悬浮"、"散发光芒"
- 动作决定画面的"故事感"，没有动作就是证件照

**示例**：
```
正在从旧书中抬起头，眼睛发出温暖的橙色光芒
悬浮在半空中，周围环绕着漂浮的代码碎片
```

### 3. 场景（Scene）—— 搭建舞台

**规则**：
- 场景要与主体/动作形成**叙事呼应**，不是随便加个背景
- 用 2-3 个具象元素定义场景，不要堆砌形容词

**示例**：
```
❌ "未来科技感背景"（太空洞）
✅ "一张旧木桌上散落着泛黄的代码纸页，桌角有一杯冒着热气的咖啡"
```

### 4. 风格（Style）—— 视觉语言

**常见风格库**：

| 风格类型 | 关键词 | 适用场景 |
|---------|--------|---------|
| 胶片摄影 | `拍立得胶片风`、`Kodak Portra 400`、`胶片颗粒` | 温暖、怀旧、人文感 |
| 赛博朋克 | `霓虹灯`、`雨夜`、`高对比度` | 科技产品发布 |
| 极简主义 | `纯白背景`、`留白`、`单色主体` | 品牌 Logo/名片 |
| 水彩手绘 | `水彩晕染`、`手绘线条`、`纸张纹理` | 温暖科技品牌 |
| 3D 渲染 | `Octane Render`、`光线追踪`、`C4D` | 产品渲染、图标 |
| 扁平插画 | `flat illustration`、`矢量风格`、`无描边` | UI 配图、 Landing page |

### 5. 构图（Composition）—— 镜头语言

**常见构图模式**：

| 构图 | 关键词 | 效果 |
|------|--------|------|
| 中心对称 | `symmetrical composition`、`centered` | 权威、稳定、正式 |
| 三分法 | `rule of thirds`、`主体偏右` | 自然、呼吸感 |
| 极度特写 | `extreme close-up`、`macro lens` | 强调细节、冲击力 |
| 超广角 | `ultra-wide angle`、`fisheye` | 宏大、沉浸 |
| 俯视 | `overhead shot`、`bird's eye view` | 全局感、信息密度 |
| 平视 | `eye-level`、`straight on` | 亲和、对话感 |

### 6. 光线（Lighting）—— 情绪调色板

**常见光线模式**：

| 光线 | 关键词 | 情绪 |
|------|--------|------|
| 丁达尔光 | `Tyndall effect`、`god rays`、`体积光` | 神圣、温暖、希望 |
| 霓虹灯 | `neon lighting`、`cyan and magenta` | 未来、科技、前卫 |
| 黄金时段 | `golden hour`、`warm sunset light` | 温暖、怀旧、安心 |
| 伦勃朗光 | `Rembrandt lighting`、`dramatic side light` | 戏剧、深沉、权威 |
| 柔光箱 | `softbox`、`diffused light`、`even lighting` | 专业、干净、商业 |
| 背光剪影 | `backlit`、`silhouette`、`rim light` | 神秘、轮廓、戏剧性 |

### 7. 细节（Details）—— 质感咒语

**分层使用，不要全堆**：

| 层级 | 关键词 | 作用 |
|------|--------|------|
| 分辨率 | `8k resolution`、`ultra-detailed` | 清晰度保证 |
| 渲染质量 | `unreal engine 5`、`Octane Render` | 3D 渲染质感 |
| 纹理 | `film grain`、`paper texture`、`noise overlay` | 增加"手工感" |
| 景深 | `shallow depth of field`、`bokeh` | 主体突出 |
| 调色 | `cinematic color grading`、`teal and orange` | 电影感 |

---

## Prompt 模板

### 基础模板（5 维）

```
[主体] + [动作] + [场景] + [风格] + [光线]
```

示例：
```
"A robot wizard" holding a glowing magic wand, 
standing on an old wooden desk covered with yellowed code pages, 
watercolor painting style, 
golden hour warm light
```

### 完整模板（7 维）

```
[主体] + [动作] + [场景] + [风格] + [构图] + [光线] + [细节]
```

示例：
```
"A robot wizard" holding a glowing magic wand,
standing on an old wooden desk covered with yellowed code pages,
watercolor painting style,
rule of thirds composition,
golden hour warm light with Tyndall effect,
8k resolution, paper texture overlay, shallow depth of field
```

### Hermes 3 Series 品牌风格 Prompt

```
"A cute robot character wearing a wizard hat and holding a magic wand",
standing next to an open book with glowing code snippets,
on a warm cream-colored background with subtle paper texture,
flat illustration style with hand-drawn outlines,
centered composition,
warm terracotta orange (#C45C2C) accent lighting,
clean lines, minimal details, friendly expression
```

---

## 常见错误

| 错误 | 为什么错 | 正确做法 |
|------|---------|---------|
| 只写风格不写主体 | AI 不知道画什么，随机出 slop | 先定主体，再定风格 |
| 堆砌 20+ 个形容词 | 信号过载，AI 随机取舍 | 每个维度 1-2 个精准词 |
| 构图和光线混淆 | 镜头语言和光源是两回事 | 构图=视角，光线=光源 |
| 不指定品牌色 | AI 默认紫色渐变（slop） | 明确写 HEX 或色名 |
| 用抽象形容词 | "好看的"、"科技感的"太空洞 | 用具象名词+动词描述 |

---

## 与品牌设计工作流的集成

当用户要求生成品牌相关的图像（封面、海报、插图、social media 图）时：

1. **先读 Brand Kit**：确定品牌色、角色、调性
2. **套用 7 维框架**：确保 prompt 不缺维度
3. **反 slop 检查**：确认没有 AI 默认紫色渐变/emoji/烂 SVG
4. **生成 → 评审 → 迭代**：用 5 维设计评审框架检查产出
