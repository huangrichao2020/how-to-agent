# Methodology 04 · 形式化验证

> 来源：Crouzeix 任务的 Lean 4 + Mathlib 形式化（千行级代码）

## 为什么需要形式化

自然语言证明的两个根本问题：
1. **gaps 无** — 人类读者会"自动补全"小跳跃
2. **条件不严格** — "显然成立"在不同人眼里是不同东西

**形式化**（Formalization）把证明写成机器可检查的代码：
- 每一个声明（lemma/theorem）都必须机器验证
- 每一个推理步骤（tactic）都必须机器接受
- 没有任何"显然" —— 一切都必须显式

## 何时用形式化

| 任务类型 | 形式化工具 | 适用场景 |
|---|---|---|
| 数学证明 | Lean 4 + Mathlib | 高（数学的核心就是形式化）|
| 算法正确性 | Coq / Dafny | 高（算法证明）|
| 协议/系统 | TLA+ / Isabelle | 中-高（分布式系统）|
| 软件架构 | Alloy / TLA+ | 中（架构约束）|
| 物理定理 | Lean 4 / Isabelle | 高（数学物理）|
| 论文写作 | 不适用 | 低（自然语言就够）|

**原则**：如果任务的关键输出是"证明"或"系统正确性"，形式化是高 ROI。

## Lean 4 核心心法

### 1 · 信任边界（Trust Boundary）

只允许使用最基础的公理：

```lean
-- 唯一允许的公理
axiom propext : ∀ {a b : Prop}, a ↔ b → a = b
axiom Classical.choice : ∀ {α : Sort u}, nonempty α → α
axiom Quot.sound : ∀ {α : Sort u} {r : α → α → Prop} {a b : α},
                   r a b → Quot.mk r a = Quot.mk r b
```

**禁止**：
- `sorry` —— 占位证明
- `admit` —— 接受未证
- 自定义 `axiom` —— 跳过证明
- `unsafe` 构造
- native-decision 捷径
- 编译器信任捷径
- 警告抑制
- 循环端点别名

### 2 · 公理审计（AXIOM_AUDIT.md）

每个主要定理都必须报告公理依赖：

```
- `holomorphicCrouzeixBound` A f:
  Assume exactly `U ⊇ W(A)` and `DifferentiableOn ℂ f U`.
  Result: `‖holomorphicMatrixEval A f‖ ≤ 2 * maxFunctionModulusOnSet (numericalRange A) f`
  Audit: depends only on propext, Classical.choice, Quot.sound
```

### 3 · 形式化映射（FORMALIZATION_MAP.md）

源文件（LaTeX）的每一行声明，对应到 Lean 命名：

```
| Source | Claim | Lean declaration(s) | Status |
|---|---|---|---|
| lines 94-129 | 主定理 | holomorphicCrouzeixBound | proved |
| lines 104-129 | 紧性 | isCompact_numericalRange | proved |
| lines 131-138 | Jordan 见证 | jordanNilpotentTwo_attains_two | proved |
```

**Status 定义**：
- `proved` —— 机器验证过的完整证明
- `defined` —— 目标已编码（结构/接口）
- `proved reduction` —— 已证蕴含关系（用端点调用）

### 4 · 构建链

```sh
# 编译所有
lake build

# 审计公理依赖
lake env lean AxiomAudit.lean
```

**注意**：必须**串行**运行，避免内存/磁盘竞争。

### 5 · 信任短路 vs 完整证明

**完整证明**（好）：
```lean
theorem crouzeixConjecture : ∀ (A : SquareMatrix n) (p : Polynomial ℂ),
  ‖polynomialEval p A‖ ≤ 2 * maxPolynomialModulusOnNumericalRange A p := by
  intro A p
  exact holomorphicCrouzeixBound _ _ (polynomialEval A p) _ ...
```

**信任短路**（坏）：
```lean
axiom crouzeixConjecture : ∀ (A : SquareMatrix n) (p : Polynomial ℂ),
  ‖polynomialEval p A‖ ≤ 2 * maxPolynomialModulusOnNumericalRange A p
```

## 实战要点

### 1 · 形式化 vs 自然语言证明

| 维度 | 自然语言 | 形式化 |
|---|---|---|
| 读者 | 人类数学家 | 机器 |
| 推理跳跃 | 容忍（"显然"）| 不容忍 |
| 条件 | 模糊 | 严格 |
| 验证 | 同行评议 | 机器检查 |
| 表达力 | 强（可省略）| 弱（必须显式）|

**关系**：自然语言证明给"思想"，形式化给"严格"。

### 2 · 何时引入形式化

**推荐路径**：
1. 先用自然语言证明（v1、v2）
2. 找漏洞、简化（v3）
3. 引入形式化（v4）

**不要**：
- 一开始就形式化（路径可能错）
- 跳过 v1→v2 的简化（形式化早期版本会浪费大量时间）

### 3 · 形式化与简化迭代的互动

| 迭代 | 形式化状态 |
|---|---|
| v1 | 初次形式化（可能有冗余）|
| v2 | 形式化跟随简化（删除冗余 lemma）|
| v3 | 进一步简化形式化（合并证明）|
| v4 | 形式化稳定（Git 历史保留 v1/v2/v3）|

### 4 · Git history 保留所有版本

形式化的最大价值之一：**保留历史**。

```
git log
- v1: initial formalization (with redundancy)
- v2: simplified (deleted 30% lemmas)
- v3: simplified more (deleted 50% lemmas)
- v4: stable (kept only necessary)
```

**关键**：v1 的失败版本（带 `sorry`）可以在 git history 里保留，但不进入工作树。这让审计能追溯"曾走过的弯路"。

## Crouzeix 项目的形式化示例

### 主定理（Lean 4 代码）

```lean
theorem holomorphicCrouzeixBound
    {n : ℕ} [Nonempty n] (A : SquareMatrix n ℂ)
    (U : Set ℂ) (hU : isOpen U) (hUW : W A ⊆ U)
    {f : ℂ → ℂ} (hf : DifferentiableOn ℂ f U) :
    ‖holomorphicMatrixEval A f‖ ≤ 2 * maxFunctionModulusOnSet (numericalRange A) f :=
  ...
```

**关键设计**：
- 假设**严格**：`isOpen U`、`W A ⊆ U`、`DifferentiableOn ℂ f U`
- 没有"显然成立"
- 没有"标准库里有"

### 多项式特化（Lean 4）

```lean
theorem crouzeixConjecture
    {n : ℕ} [Nonempty n] (A : SquareMatrix n ℂ)
    (p : Polynomial ℂ) :
    ‖polynomialEval p A‖ ≤ 2 * maxPolynomialModulusOnNumericalRange A p :=
  holomorphicCrouzeixBound _ _ _ _ _ p.differentiableOn_polynomial
```

**关键**：直接从 holomorphicCrouzeixBound 推出，没有独立证明。

### 见证（Lean 4）

```lean
theorem crouzeixConstantTwo_isLeast_finTwo :
    ∀ K, (∀ (n : ℕ) [Nonempty n] (A : SquareMatrix n ℂ)
              (r : RationalFunc ℂ) (h : r.poles ⊆ W A^c),
              ‖rationalMatrixEval r A‖ ≤ K * maxRationalModulusOnNumericalRange A r) →
         K ≥ 2 := by
  ...
```

**关键**：用 2×2 Jordan 见证证明 K ≥ 2 是 tight 的。

## 工具链

| 工具 | 用途 |
|---|---|
| Lean 4 + Mathlib | 数学证明 |
| lake | Lean 项目管理 |
| Coq | 替代方案 |
| Dafny | 算法验证 |
| TLA+ | 分布式系统 |
| Isabelle/HOL | 替代方案 |

## 下一步

- 迭代协议 → `05-iteration-protocol.md`
- 完成检查清单 → `06-completion-checklist.md`