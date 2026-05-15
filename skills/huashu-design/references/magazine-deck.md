# 杂志演讲 Deck（Magazine Web PPT）

基于 guizang-ppt-skill（3.3k stars）融合的能力，**与路径 A（出版物 deck）并列**的另一条幻灯片路径。

**核心理念**：像做电子杂志一样做 PPT —— 横向 swipe 翻页、WebGL 动态背景、衬线标题 + 非衬线正文、5 套精心调配主题色、10 种布局骨架、Motion One 翻页动效。

---

## 何时选择杂志路径

| 场景 | 推荐路径 |
|------|---------|
| 线下分享 / 演讲 / demo day | **杂志路径**（视觉冲击力强） |
| AI 新产品发布 / 私享会 | **杂志路径**（个人风格强） |
| B2B brochure / 学术课件 | 出版物路径 A（信息密度高） |
| 大段表格 / 数据报告 | 出版物路径 A（支持 pdf/pptx 导出） |
| 需要可编辑 PPTX | 出版物路径 A（html2pptx 链路） |

---

## 工作流程

### Step 1 · 需求澄清（6 问）

**如果用户已给完整大纲 + 图片**，直接进 Step 2。

**如果只给主题或模糊想法**，用这 6 个问题对齐后再动手：

| # | 问题 | 为什么 |
|---|------|--------|
| 1 | 受众是谁？分享场景？ | 决定语言风格和深度 |
| 2 | 分享时长？ | 15min ≈ 10 页，30min ≈ 20 页 |
| 3 | 有原始素材吗？ | 有素材就基于素材做 |
| 4 | 有图片吗？放哪？ | 命名规范：`{页号}-{语义}.{ext}` |
| 5 | 想要哪套主题色？ | 5 套预设（见下方） |
| 6 | 有硬约束吗？ | 避免返工 |

### Step 2 · 拷贝模板

```bash
cp assets/magazine_template.html 项目/XXX/ppt/index.html
mkdir -p 项目/XXX/ppt/images/
```

**必改占位符**（容易漏）：
- `<title>`：`[必填] 替换为 PPT 标题 · Deck Title` → 实际标题
- grep `\[必填\]` 确认全部替换完

### Step 3 · 选定主题色（5 套预设）

| # | 主题 | 适合 |
|---|------|------|
| 1 | 🖋 墨水经典 | 通用 / 商业发布 / 默认 |
| 2 | 🌊 靛蓝瓷 | 科技 / 研究 / 数据 |
| 3 | 🌿 森林墨 | 自然 / 可持续 / 文化 |
| 4 | 🍂 牛皮纸 | 怀旧 / 人文 / 文学 |
| 5 | 🌙 沙丘 | 艺术 / 设计 / 创意 |

**硬规则**：一份 deck 只用一套，不接受自定义 hex 值。操作：从 templates/themes.md 复制对应 `:root` 块，整体替换 `--ink` / `--paper` 等 6 个变量。

### Step 4 · 填充内容

#### 4.0 · 预检类名（最重要）

在写任何 slide 代码之前：
1. Read `assets/magazine_template.html`（至少读到 `<style>` 块末尾）
2. 确认你要用的每个类都在 `<style>` 里有定义
3. 如果某个类缺失：在 template 的 `<style>` 里补上，不要在每个 slide 里 inline 重写

**必须预先确认存在的类**：
`h-hero` / `h-xl` / `h-sub` / `h-md` / `lead` / `kicker` / `meta-row` / `stat-card` / `stat-label` / `stat-nb` / `stat-unit` / `stat-note` / `pipeline-section` / `pipeline-label` / `pipeline` / `step` / `step-nb` / `step-title` / `step-desc` / `grid-2-7-5` / `grid-2-6-6` / `grid-2-8-4` / `grid-3-3` / `grid-6` / `grid-3` / `grid-4` / `frame` / `frame-img` / `img-cap` / `callout` / `callout-src` / `chrome` / `foot`

#### 4.1 · 挑布局（10 种）

| Layout | 用途 |
|--------|------|
| 1. 开场封面 | 第 1 页 |
| 2. 章节幕封 | 每幕开场 |
| 3. 数据大字报 | 抛硬数据 |
| 4. 左文右图 | 身份反差 / 故事 |
| 5. 图片网格 | 多图对比 |
| 6. 两列流水线 | 工作流程 |
| 7. 悬念收束 / 问题页 | 幕末 / 收尾 |
| 8. 大引用页 | 衬线金句 |
| 9. 并列对比 | 旧模式 vs 新模式 |
| 10. 图文混排 | 信息密集的图文页 |

#### 4.2 · 主题节奏规划

**强制规则**：
- 每页 section 必须带 `light` / `dark` / `hero light` / `hero dark` 之一
- 连续 3 页以上同主题 = 视觉疲劳，不允许
- 8 页以上必须有 ≥1 个 `hero dark` + ≥1 个 `hero light`
- 整个 deck 不能只有 `light` 正文页，必须有 `dark` 正文页制造呼吸
- 每 3-4 页插入 1 个 hero 页（封面/幕封/问题/大引用）

#### 4.3 · 图片比例规范

| 场景 | 推荐比例 |
|------|---------|
| 左文右图主图 | 16:10 或 4:3 + `max-height:56vh` |
| 图片网格 | 固定 `height:26vh` |
| 左小图右文字 | 1:1 或 3:2 |
| 全屏主视觉 | 16:9 + `max-height:64vh` |

### Step 5 · 自检清单

1. **大标题必须是衬线字体** —— 如果显示成非衬线，99% 是 `h-hero` 类缺失
2. **不要出现 emoji** —— 用 Lucide 图标（`<i data-lucide="...">` + `lucide.createIcons()`）
3. **图片不要撑破** —— 用标准比例，不要用原图奇葩比例
4. **标题不要换行断裂** —— 用 `text-wrap: pretty` 或控制标题长度
5. **字体分工** —— 衬线=标题，非衬线=正文，等宽=meta 标签

---

## CDN 适配说明（国内阿里云环境）

| CDN | 状态 | 处理 |
|-----|------|------|
| Google Fonts | ✅ 可访问 | 保留原 URL |
| Motion.js | ✅ esm.sh | 已从 jsdelivr 改为 esm.sh |
| Lucide Icons | ✅ unpkg | 302 可达 |

模板已内置 Motion 加载降级：优先 esm.sh CDN，失败则尝试本地 `./assets/motion.min.js`。

---

## 与路径 A（出版物 deck）的互操作

| 维度 | 杂志路径 | 路径 A（出版物） |
|------|---------|-----------------|
| 输出格式 | 单文件 HTML | 多文件 HTML + index 聚合 |
| 导航方式 | 横向 swipe + 圆点 + ESC | 键盘翻页 + 计数器 |
| 视觉背景 | WebGL 流体动态 | 纯色 + 极淡 noise |
| PDF 导出 | 需 Playwright 截图 | `export_deck_pdf.mjs` 矢量 |
| PPTX 导出 | 不支持（视觉自由度太高） | `export_deck_pptx.mjs` 可编辑 |
| 适合页数 | ≤20 页（演讲场景） | 不限（长报告也可） |
| 制作成本 | 低（拷贝模板改文案） | 中（需建目录结构） |

**选择建议**：用户说「演讲 / 分享 / demo」→ 杂志路径；用户说「课件 / 报告 / 要 PPTX」→ 路径 A。
