# Methodology 02 · 多智能体管理 10 条铁律

> 来源：Crouzeix 猜想证明任务的"Use multiagents aggressively and dynamically"

## 为什么需要多智能体

单一 agent 死磕复杂问题有 3 大瓶颈：

1. **思路收敛** —— 单个 agent 会很快锁定一个方法
2. **盲点不可见** —— 单个 agent 看不到自己的盲点
3. **无对照系** —— 没有平行探索，无法判断哪条路径更优

**多智能体解决**：每个 agent 独立探索一种思路族 → root agent 综合 → 对抗 agent 找漏洞。

## 10 条铁律详解

### 铁律 1 · 激进多智能体

> "Use multiagents aggressively and dynamically. Do not use a fixed assignment such as 'N agents for strategy X.' Instead, manage the search using the following heuristics."

**实操**：
- 不预设"N 个 agent 走 N 条路径"
- 按问题难度动态调整：
  - 简单问题：3-5 个 agent
  - 中等问题：5-10 个 agent
  - 极难问题：10-20 个 agent + 多轮次
- 每个 agent 完成后，root agent 决定：
  - 哪条路径继续？
  - 哪条路径 block？
  - 是否需要新方法族？

### 铁律 2 · 多样性优先

> "Do not tell most agents the currently favored approach. Preserve independence during early rounds so that agents do not all converge to the same attractive but incomplete reduction."

**实操**：
- 早期轮次：每个 agent **不知道**其他人在干什么
- 只在综合阶段（root agent）才看到全部输出
- 如果某个 agent 太强，**人为隐藏**它的结果给其他 agent
- 后期轮次：可以有部分共享，但要标记"已成功路径"

### 铁律 3 · 方法族注册表

> "Maintain an explicit registry of approach families. Group agents by the mathematical idea they are using, not by superficial wording."

**实操**：维护 `approach-registry.md`：

| 思路族 | 代表性方法 | 当前状态 | 主要 agent | 备注 |
|---|---|---|---|---|
| 代数重构 | 矩阵分解 / 同构映射 | active | A1, A3 | 进度 60% |
| 几何 | 凸性 / 紧性 / Cauchy 估计 | blocked | A2 | 缺引理 X |
| 拓扑 | 紧化 / 谱分解 | active | A4 | 进度 30% |
| 计算 | 数值验证 / 反例搜索 | active | A5 | 反例已排除 |
| 简化策略 | 辅助基简化 / 仿射扰动 | active | A6 | 新提出 |

**关键**：分组按**思路族**而非表面措辞 —— "代数重构"和"矩阵分解"虽然文字不一样，可能属于同一个思路族。

### 铁律 4 · 防止过早收敛

> "Do not allow one approach to dominate merely because it gives elegant reductions. A route that ends at a lemma equivalent in strength to the original problem is not close to completion unless it supplies a genuinely new proof of that lemma."

**实操**：
- 一个方案即使"简化漂亮"，如果终点是等价强度的引理 → **不算进展**
- root agent 必须识别"虚假进展"——简化但没突破
- 当一条路径"看起来很优雅"时，**反而要警惕**：
  - 它可能简化到了原问题
  - 它可能漏掉了关键约束

### 铁律 5 · 标记阻塞路径

> "When an approach stalls at a theorem-strength missing lemma, mark that route as blocked. Only continue assigning agents to it if someone proposes a materially new mechanism, invariant, or construction."

**实操**：
- 当一个 agent 报"我需要引理 X 但 X 还没证明" → **block 该路径**
- 只在有人提出**新机制 / 不变量 / 构造**时重新激活
- 不允许"再试试"型 block 循环
- 不允许"我有预感这是对的"型复活

### 铁律 6 · 多路径存活

> "Keep several incompatible proof routes alive through multiple rounds. Cross-pollinate ideas only after independent agents have developed them far enough to expose their real strengths and gaps."

**实操**：
- 至少保持 3-5 条**不兼容**路径活跃多轮
- 路径不兼容 = 它们不能同时为真（或不能同时存在）
- 交叉授粉只在每条路径独立发展足够深度后才做
- 不允许"我希望这条路径对，所以优先它"

### 铁律 7 · 对抗审计全程

> "Use adversarial agents throughout: every candidate proof must be checked for gaps, conditionals, handwavings, and circular uses of an equivalent statement."

**实操**：
- 每个候选证明都过对抗审计
- 对抗 agent 找 4 类问题：gaps / conditionals / handwavings / circular
- 对抗审计从 v1 开始就进行，不只在最后
- 详见 `03-adversarial-audit.md`

### 铁律 8 · 要求具体产出

> "Require agents to return concrete lemmas, constructions, equations, or counterexamples to proposed sublemmas. Reject status reports, vague optimism, and claims that an unproved statement is 'routine.'"

**实操**：agent 必须返回**具体东西**，不能是状态报告：

| 类型 | 具体产出 | 不合格产出 |
|---|---|---|
| 引理 | "引理 X：若 A，则 B" + 完整证明 | "我觉得 X 是对的" |
| 构造 | 显式构造 + 验证 | "应该存在一个构造" |
| 方程 | 完整公式 + 推导 | "应该满足某方程" |
| 反例 | 显式反例 + 验证 | "可能存在反例" |

**root agent 必须拒绝**：模糊乐观、"显然"、"routine"、"standard"。

### 铁律 9 · 持续轮次

> "The root agent should repeatedly synthesize, challenge, redirect, and launch new rounds. Do not stop after the first wave fails."

**实操**：
- root agent 是中心指挥
- 每轮结束要做 4 件事：
  1. **综合**：把这一轮所有 agent 的输出整理成当前状态
  2. **挑战**：质疑已有结论（即使看起来已证）
  3. **重定向**：调整下一轮 agent 的任务
  4. **新轮次**：启动新一批 agent（基于综合结果）
- 不允许"一轮失败就停下"

### 铁律 10 · 完成才停止

> "Return only when a complete affirmative proof has been found and survives adversarial audit."

**实操**：
- root agent **不能**因"看起来差不多了"而返回
- 必须满足"完整证明 + 通过对抗审计"才返回
- 返回时附带证据：
  - 主证明文件
  - 形式化验证文件
  - 审计报告
  - 公理依赖图

## 多智能体路由示例

### Crouzeix 任务的实际多智能体分工（推测）

基于 commit history 反推：

| 阶段 | agent 数 | 主要思路族 |
|---|---|---|
| 初版 v1 | ~5-8 个 | 代数重构 / 几何 / 拓扑 / 计算 / 简化 |
| v2 简化 | ~3-5 个 | 辅助基简化 / 仿射扰动 / Cauchy |
| v3 简化 | ~3 个 | 直接归约 / 紧化 |
| v4 最终 | 2 个 | 合并最优 + 对抗审计 |
| Lean 形式化 | 1-2 个 | 与数学 agent 紧密协作 |

### 我的实战建议（中小型任务）

对于日常工作流（不是数学证明），可以把 5-10 个 agent 减到 2-3 个：

- **1 个主执行 agent** —— 写主稿
- **1 个对抗审计 agent** —— 找漏洞
- **1 个方法族注册 agent** —— 维护思路清单

但**核心心法不变**：独立探索 + 综合 + 审计。

## 下一步

- 对抗审计机制 → `03-adversarial-audit.md`
- 形式化验证 → `04-formalization.md`
- 迭代协议 → `05-iteration-protocol.md`