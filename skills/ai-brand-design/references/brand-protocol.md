# 核心资产协议（Core Asset Protocol）

源自 huashu-design v2.0 的品牌资产定义方法论，融合 Lovart 的自动提取思路。

> **v2.0 核心升级**：从"品牌资产协议"升级为"核心资产协议"。之前的版本过度聚焦色值和字体，漏掉了设计中最基础的 logo / 产品图 / UI 截图。

## 核心理念

> 品牌不是"描述"出来的，是"提取"或"抽卡"出来的。
> 让用户凭空描述一套视觉规范几乎不可能；但让他们看一套方案说"这个对"很容易。

**品牌的本质是「它被认出来」**。按识别度排序：

| 资产类型 | 识别度贡献 | 必需性 |
|---|---|---|
| **Logo** | 最高 · 任何品牌出现 logo 就一眼识别 | **任何品牌都必须有** |
| **产品图/产品渲染图** | 极高 · 实体产品的"主角"就是产品本身 | **实体产品必须有** |
| **UI 截图/界面素材** | 极高 · 数字产品的"主角"是它的界面 | **数字产品必须有** |
| **色值** | 中 · 辅助识别，脱离前三项时经常撞衫 | 辅助 |
| **字体** | 低 · 需配合前述才能建立识别 | 辅助 |

**翻译成执行规则**：
- 只抽色值 + 字体、不找 logo / 产品图 / UI → **违反本协议**
- 用 CSS 剪影/SVG 手画替代真实产品图 → **违反本协议**
- 找不到资产不告诉用户、也不 AI 生成，硬做 → **违反本协议**
- 宁可停下问用户要素材，也不要用 generic 填充

## 5 步硬流程（每步有 fallback，绝不静默跳过）

### Step 1 · 问（资产清单一次问全）

按清单逐项问：

```
关于 <brand/product>，你手上有以下哪些资料？我按优先级列：
1. Logo（SVG / 高清 PNG）—— 任何品牌必备
2. 产品图 / 官方渲染图 —— 实体产品必备
3. UI 截图 / 界面素材 —— 数字产品必备
4. 色值清单（HEX / RGB / 品牌色盘）
5. 字体清单（Display / Body）
6. Brand guidelines PDF / Figma design system / 品牌官网链接

有的直接发我，没有的我去搜/抓/生成。
```

### Step 2 · 搜官方渠道（按资产类型）

| 资产 | 搜索路径 |
|---|---|
| **Logo** | `<brand>.com/brand` · `<brand>.com/press` · 官网 header 的 inline SVG |
| **产品图** | 产品详情页 hero image + gallery · 官方 press kit · YouTube launch film 截帧 |
| **UI 截图** | App Store / Google Play 产品页截图 · 官网 screenshots · 产品演示视频截帧 |
| **色值** | 官网 inline CSS / Tailwind config / brand guidelines PDF |
| **字体** | 官网 `<link rel="stylesheet">` 引用 · Google Fonts 追踪 |

兜底搜索关键词：
- Logo 找不到 → `<brand> logo download SVG`、`<brand> press kit`
- 产品图找不到 → `<brand> <product> official renders`、`<brand> <product> product photography`
- UI 找不到 → `<brand> app screenshots`、`<brand> dashboard UI`

### Step 3 · 下载资产 · 按类型兜底

#### 3.1 Logo（任何品牌必需）

三条路径按成功率递减：
1. 独立 SVG/PNG 文件（最理想）
2. 官网 HTML 全文提取 inline SVG（80% 场景必用）
3. 官方社交媒体 avatar（最后手段，通常是 400×400 或 800×800 透明底 PNG）

#### 3.2 产品图/渲染图（实体产品必需）

按优先级：
1. 官方产品页 hero image（最高优先级）
2. 官方 press kit
3. 官方 launch video 截帧
4. Wikimedia Commons
5. AI 生成兜底（以真实产品图为参考生成变体，**不要用 CSS/SVG 手画**）

#### 3.3 UI 截图（数字产品必需）

- App Store / Google Play 的产品截图
- 官网 screenshots section
- 产品演示视频截帧
- 产品官方 Twitter/X 的发布截图

#### 3.4 素材质量门槛「5-10-2-8」原则（铁律）

> 2026-04-20 花叔原话：「搜索 5 轮，找到 10 个素材，选择 2 个好的。每个需要评分 8/10 以上，宁可少一些，也不为了完成任务滥竽充数。」

| 维度 | 标准 | 反模式 |
|---|---|---|
| **5 轮搜索** | 多渠道交叉搜，不是一轮抓前 2 个就停 | 第一页结果直接用 |
| **10 个候选** | 至少凑 10 个备选才开始筛 | 只抓 2 个，没得选 |
| **选 2 个好的** | 从 10 个里精选 2 个作为最终素材 | 全都用 = 视觉过载 + 品位稀释 |
| **每个 8/10 分以上** | 不够 8 分**宁可不用**，用诚实 placeholder | 凑数 7 分素材 |

**Logo 例外**（重申）：有就必须用，不适用「5-10-2-8」。因为 logo 不是"多选一"问题，而是"识别度根基"问题。

### Step 4 · 验证 + 提取

| 资产 | 验证动作 |
|---|---|
| **Logo** | 文件存在 + SVG/PNG 可打开 + 至少两个版本（深底/浅底用）+ 透明背景 |
| **产品图** | 至少一张 2000px+ 分辨率 + 去背或干净背景 + 多个角度 |
| **UI 截图** | 分辨率真实 + 是最新版本 + 无用户数据污染 |
| **色值** | 从真实 HTML/SVG/CSS 中 grep 提取，过滤黑白灰 |

**警惕示范品牌污染**：产品截图里常有用户 demo 的品牌色，那不是该工具的色。同时出现两种强色时必须区分。

### Step 5 · 固化为 `brand-spec.md`

```markdown
# <Brand> · Brand Spec
> 采集日期：YYYY-MM-DD
> 资产来源：<列出下载来源>
> 资产完整度：<完整 / 部分 / 推断>

## 🎯 核心资产（一等公民）

### Logo
- 主版本：`assets/<brand>-brand/logo.svg`
- 浅底反色版：`assets/<brand>-brand/logo-white.svg`
- 使用场景：<片头/片尾/角落水印/全局>

### 产品图（实体产品必填）
- 主视角：`assets/<brand>-brand/product-hero.png`
- 细节图：`assets/<brand>-brand/product-detail-1.png`

### UI 截图（数字产品必填）
- 主页：`assets/<brand>-brand/ui-home.png`
- 核心功能：`assets/<brand>-brand/ui-feature-<name>.png`

## 🎨 辅助资产

### 色板
- Primary: #XXXXXX
- Background: #XXXXXX
- Ink: #XXXXXX

### 字型
- Display: <font stack>
- Body: <font stack>

### 气质关键词
- <3-5 个形容词>
```

**写完 spec 后的执行纪律**：
- 所有 HTML 必须**引用** `brand-spec.md` 里的资产文件路径
- Logo 作为 `<img>` 引用真实文件，不重画
- 产品图作为 `<img>` 引用真实文件，不用 CSS 剪影代替
- CSS 变量从 spec 注入：`:root { --brand-primary: ...; }`

## 兜底处理

| 缺失 | 处理 |
|---|---|
| **Logo 完全找不到** | **停下问用户**，不要硬做 |
| **产品图（实体产品）找不到** | 优先 AI 生成（以官方参考图为基底）→ 向用户索取 → 诚实 placeholder（灰块+文字标签） |
| **UI 截图（数字产品）找不到** | 向用户索取自己账号的截屏 → 官方演示视频截帧 |
| **色值完全找不到** | 走设计方向顾问模式，向用户推荐 3 个方向并标注 assumption |

**禁止**：找不到资产就静默用 CSS 剪影/通用渐变硬做——这是协议最大的反 pattern。**宁可停下问，也不要凑**。

## 协议代价 vs 不做代价

| 场景 | 时间 |
|---|---|
| 正确走完协议 | 下载 logo 5 min + 下载 3-5 张产品图/UI 10 min + grep 色值 5 min + 写 spec 10 min = **30 分钟** |
| 不做协议的代价 | 做出没识别度的通用动画 → 用户返工 1-2 小时，甚至重做 |

**这是稳定性最便宜的投资**。
