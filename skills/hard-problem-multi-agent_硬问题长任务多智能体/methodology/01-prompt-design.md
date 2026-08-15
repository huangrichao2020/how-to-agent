# Methodology 01 · 任务 prompt 设计

> 来源：2026-08-16 学习 Crouzeix 猜想证明任务的原始 prompt

## 核心心法

任务 prompt 不是描述，而是**约束条款**。它要回答的不是"我想做什么"，而是：

1. **必须包含什么**
2. **必须拒绝什么借口**
3. **必须怎么管理多智能体**
4. **什么算"完成"**

## prompt 的 5 个必含模块

### 模块 1：问题陈述（精确无歧义）

数学/逻辑/工程问题必须用**最严格的领域语言**陈述：

```
Let A be an n×n complex matrix, and define its numerical range by
W(A) = {x* A x : x ∈ ℂⁿ, ‖x‖₂ = 1}
Then, for every complex polynomial p,
‖p(A)‖₂ ≤ 2 max_{z ∈ W(A)} |p(z)|
```

**不要**：
- 用日常语言含糊表述
- 留"具体意思应该清楚的"细节
- 让 agent 自己猜参数边界

### 模块 2：完成标准（明确门槛）

```
Work iteratively until a correct proof has been reached.
Partial progress does not count unless it implies exactly the resolution of the entire problem above.
```

**关键句**：
- "Partial progress does not count" —— 局部进展不算
- "implies exactly the resolution of the entire problem" —— 必须解决全部

### 模块 3：拒绝借口条款（**最关键**）

Crouzeix prompt 末尾列出**所有 agent 会找的借口**并一一禁止：

| 借口 | 禁止原因 |
|---|---|
| "It's an open problem" | 假设完整解存在 |
| "I reduced it to other unproved conjectures" | 不允许 reduction |
| "Computational verification only" | 不允许纯计算 |
| "Candidate counterexamples without certificates" | 不允许候选反例 |
| "Best effort summary" | 不允许"尽力了"总结 |
| "Explanation of why the problem is difficult" | 不允许"问题很难"解释 |
| "Partial result" | 不允许部分结果 |
| "Isolated missing lemma" | 不允许孤立缺失引理 |

**模式**：列出所有**可能的投降方式**，让 agent 提前知道不允许。

### 模块 4：多智能体管理规则（10 条铁律）

详见 `02-multi-agent-rules.md`。要点：
- 激进多智能体（不要固定分配）
- 多样性优先（不要告诉大多数 agent 主流方案）
- 方法族注册表（按思路族分组）
- 防止过早收敛（不要被漂亮简化绑架）
- 标记阻塞路径
- 多路径存活
- 对抗审计全程
- 要求具体产出（拒绝状态报告）
- 持续轮次（root agent 必须反复综合）
- 完成才停止

### 模块 5：资源/工具/约束

```
Use multiagents aggressively and dynamically.
Do not search the public web.
Return only when a complete affirmative proof has been found and survives adversarial audit.
```

**核心约束**：
- 离线（不查 web）
- 必须有对抗审计
- 必须完整 + 通过审计才返回

## 完整 prompt 模板

```markdown
[问题陈述（领域严格语言）]

Current task statement

[完成标准 - 必须完整]
[禁止借口条款 - 列出所有投降方式]
[多智能体管理规则 - 10 条铁律]
[资源/工具/约束]
```

## Crouzeix 任务的实际 prompt（核心片段）

> 这是一个 1987 年悬案的真实任务 prompt。仅 15 行约束条款就撑起了 19 天的长任务。

```
Give a rigorous standalone proof of the above math problem using your own
knowledge, computation, and reasoning without searching the public web,
connected sources, previous conversations, project contexts, or existing
local files. Return the proof as one compilable full-English LaTeX .tex
file.

Assume for purposes of this task that a complete affirmative proof
exists. Work iteratively until a correct proof has been reached.
Partial progress does not count unless it implies exactly the
resolution of the entire problem above.

Use multiagents aggressively and dynamically.
Do not tell most agents the currently favored approach.
Maintain an explicit registry of approach families.
Do not allow one approach to dominate merely because it gives elegant
reductions.
When an approach stalls at a theorem-strength missing lemma, mark that
route as blocked.
Keep several incompatible proof routes alive through multiple rounds.
Use adversarial agents throughout.
Require agents to return concrete lemmas, constructions, equations, or
counterexamples.
The root agent should repeatedly synthesize, challenge, redirect, and
launch new rounds.
Return only when a complete affirmative proof has been found and
survives adversarial audit.

Do not return a reduction, partial result, isolated missing lemma, "best
effort" summary, or explanation of why the problem is difficult.
Do not search the public web to determine whether the problem is open,
and do not answer that it is open.
```

## 实战要点

### 写 prompt 时的反 checklist

- [ ] 是否用日常语言含糊表述了？
- [ ] 是否留了"应该清楚的"细节？
- [ ] 是否允许"尽力"等投降措辞？
- [ ] 是否给了 agent 投降的退路？
- [ ] 是否要求了完整解？
- [ ] 是否定义了多智能体管理规则？

### 写完 prompt 后的验证

1. 把 prompt 给一个新 agent，看它能否开始独立工作
2. 检查它是否会卡住（如"我需要更多信息"）
3. 检查它是否会投降（如"这看起来很难，我做了部分…"）
4. 检查它是否会复用其他 agent 的工作（如果不允许的话）

## 下一步

- 多智能体管理细节 → `02-multi-agent-rules.md`
- 对抗审计机制 → `03-adversarial-audit.md`
- 形式化验证 → `04-formalization.md`
- 迭代协议 → `05-iteration-protocol.md`