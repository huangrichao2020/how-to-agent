# Case Study 01 · 2026 Crouzeix 猜想证明

> **学习日期**：2026-08-16
> **来源仓库**：https://github.com/jinshanmu/CrouzeixConjecture
> **研究方法**：WebFetch 抓 README + 21 个 commit + 4 份审计文档
> **核心价值**：这是有史以来最标准的"AI 长任务死磕"案例

## 1 · 项目背景

### 1.1 任务本身

**Crouzeix 猜想**（Crouzeix's conjecture）：

> 1987 年由 Michel Crouzeix 提出的算子理论猜想
>
> 设 `A` 是 `n × n` 复矩阵，其**数值域**（numerical range）定义为：
>
> $$W(A) = \{x^* A x : x \in \mathbb{C}^n, \|x\|_2 = 1\}$$
>
> **猜想**：对任意复多项式 `p`，
>
> $$\|p(A)\|_2 \leq 2 \max_{z \in W(A)} |p(z)|$$
>
> 即 `W(A)` 的闭包是 `A` 的 **2-spectral set**（2-谱集）。

**地位**：算子理论/矩阵分析中的著名悬案，39 年未解。

### 1.2 仓库结构

```
CrouzeixConjecture/
├── README.md                                   # 状态 + 构建步骤
├── crouzeix_conjecture_prompt.txt              # 任务原始 prompt（含 10 条铁律）
├── AnnMath/
│   ├── the_numerical_range_is_a_2_spectral_set.tex  # Annals 投稿稿
│   ├── the_numerical_range_is_a_2_spectral_set.pdf  # 编译后的 PDF
│   └── aomart.cls                              # Annals 文档类
├── Lean/
│   ├── CrouzeixConjecture.lean                 # Lean 4 形式化
│   ├── AxiomAudit.lean                         # 公理审计
│   ├── AXIOM_AUDIT.md                          # 公理依赖报告
│   ├── MANUSCRIPT_AUDIT.md                     # 数学审计
│   ├── FORMALIZATION_MAP.md                    # 源-形式化映射
│   ├── CONTINUATION_STATUS.md                  # 当前状态
│   ├── STATUS.md                               # 状态
│   ├── README.md                               # Lean README
│   ├── lakefile.lean                           # Lean 项目配置
│   ├── lake-manifest.json                      # 依赖清单
│   └── verify.sh                               # 验证脚本
├── LaTeX/
│   ├── crouzeix_conjecture_proof.tex           # 主稿件
│   ├── crouzeix_conjecture_proof.pdf           # 编译后的 PDF
│   └── main_problem.tex                        # 问题陈述
└── preprint/
    ├── the_numerical_range_is_a_2_spectral_set_v4.tex  # v4 预印本（1,106 行）
    └── q_numerical_range_spectral_set.tex              # 量子环扩展
```

## 2 · 时间线（commit by commit）

从 commit history 反推整个流程：

### Day 1-2 · 启动期（7 月 18-19 日）

| commit | 日期 | 内容 |
|---|---|---|
| `df00105` | Jul 18 | **Record candidate proof project status**（记录项目状态）|
| `78b99e4` | Jul 19 | Keep ignore rules local and update README |
| `3b0fecf` | Jul 19 | **Add title-named Annals manuscript**（首次 Annals 投稿稿）|
| `627bb2a` | Jul 19 | **Add verified Lean formalization**（首次 Lean 形式化）|
| `03ae5f1` | Jul 19 | Prepare Annals submission（准备投稿）|
| `79128d7` | Jul 19 | **Finalize Annals submission audit**（完成审计）|

**特征**：1-2 天内**一气呵成** —— 初版稿件 + Lean 形式化 + 审计。

### Day 12 · v1 → v2（7 月 30 日）

| commit | 日期 | 内容 |
|---|---|---|
| `4910388` | Jul 30 | **Formalize auxiliary-basis proof simplification**（辅助基简化形式化）|
| `ca72eb0` | Jul 30 | **Finalize standalone v2 article**（v2 独立稿件完成）|

**关键变化**：引入"辅助基简化"（auxiliary-basis simplification）—— 路径大幅简化。

### Day 16-17 · v2 → v3 → v4（8 月 3-5 日）

| commit | 日期 | 内容 |
|---|---|---|
| `8096084` | Aug 3 | **Align Lean formalization with simplified v3 proof**（v3 形式化对齐）|
| `6ea7484` | Aug 4 | Finalize v3 citation and formalization references |
| `4956480` | Aug 4 | Prove the sharp scaled q numerical range bound（q-数值域扩展）|
| `93b382f` | Aug 4 | Finalize q numerical range preprint（q-数值域预印本）|
| `595f6fc` | Aug 5 | **Finalize v4 proof and formalization**（v4 证明 + 形式化）|
| `565b6a3` | Aug 5 | Keep equation 9 on one line（细节修正）|

**关键变化**：
- v3 删除 v1 的"扰动参数 f_eta"
- v3 删除 v2 的"碰撞避免"构造
- v4 用"first nonconstant Gramian term" 直接估计（无需 Stein 等式）

### Day 18-19 · 扩展期（8 月 6 日）

| commit | 日期 | 内容 |
|---|---|---|
| `c724883` | Aug 6 | **Integrate mass-parameterized completion principle** |
| `efd8f9d` | Aug 6 | **Add quantum annulus 2-spectral-set article** |
| `5941585` | Aug 6 | Restore Lean completion sources |
| `550a9a1` | Aug 6 | Finalize numerical-range 2-spectral-set preprint |
| `9df0783` | Aug 6 | Finalize finite-dimensional and operator-level formulations |

**特征**：v4 已可发表，开始扩展到相关问题（mass-parameterized、量子环、算子层）。

## 3 · 方法论应用（如何套用 10 条铁律）

### 铁律 1 · 激进多智能体

**证据**：
- 21 个 commit 中频繁出现 "Formalize..."、"Audit..."、"Finalize..." 字样
- 主稿件 + Lean 形式化 + 4 份审计文档 = 多智能体并行
- 多种证明路径（auxiliary-basis、simplification、mass-parameterized）

**实操推算**：
- 早期轮次：~5-8 个 agent 各自探索
- v2 简化：~3-5 个 agent
- v3/v4 收敛：~2-3 个 agent
- Lean 形式化：1-2 个 agent

### 铁律 2 · 多样性优先

**证据**：
- v1 用"扰动 f_eta"（避免碰撞）
- v2 用"辅助基"（共享基简化）
- v3/v4 删除扰动，直接接受重复样本

这是**多路径独立探索**的典型表现：不同 agent 走不同路径，最终选最强。

### 铁律 3 · 方法族注册表

**证据**：
- `CONTINUATION_STATUS.md` 列出了**多个独立的证明路径**：
  - v4 主路径（auxiliary-basis + holomorphic contour）
  - 量子环扩展路径（q-numerical range）
  - mass-parameterized 路径
- `FORMALIZATION_MAP.md` 按章节分组（lines 91-255 / 257-310 / ...）

### 铁律 4 · 防过早收敛

**证据**：
- v1 的扰动参数 η 看起来"漂亮"，但 v3 直接删除
- v2 的"碰撞避免"看似必要，v3 证明不需要
- 多次 commit 反复说明 "superseded formalization has been deleted"

**关键**：即使简化漂亮，也要质疑是否真的必要。

### 铁律 5 · 标记阻塞路径

**证据**：
- `CONTINUATION_STATUS.md` 明确说 "**Deleted superseded formalization**"
- v1 的 f_eta 路径被标记为 blocked（不再被新代码使用）

### 铁律 6 · 多路径存活

**证据**：
- v4 主路径 + 量子环 + mass-parameterized + 算子层 = 至少 4 条路径并存
- 每个路径独立完整
- 不允许"只保留最强路径"

### 铁律 7 · 对抗审计全程

**证据**（最确凿）：
- `MANUSCRIPT_AUDIT.md` —— 数学内容审计
- `AXIOM_AUDIT.md` —— 公理依赖审计
- `FORMALIZATION_MAP.md` —— 源-形式化对应
- `CONTINUATION_STATUS.md` —— 当前状态

**审计轮次**：
- 每版 v_n 都过审计
- 4 份审计文档 = 至少 4 轮审计

### 铁律 8 · 要求具体产出

**证据**：
- Lean 4 形式化 —— 每个声明都有具体代码
- 不用 "显然" / "易证"
- 公理依赖精确到 `propext` / `Classical.choice` / `Quot.sound`

### 铁律 9 · 持续轮次

**证据**：
- 19 天内 21 个 commit
- 不会因为"v1 不完美"就停下
- v1 → v2 → v3 → v4 持续推进

### 铁律 10 · 完成才停止

**证据**：
- 项目最终状态："candidate proof is written as a standalone LaTeX manuscript"
- "Several independent computational and adversarial audits have found no specific mathematical error"
- **不声称**"证明正确"——只说"已通过多轮审计"

**诚实声明**："Formal peer review is still pending"（同行评议待审）。

## 4 · v1 → v2 → v3 → v4 的具体变化

### v1（初版）

**关键特征**：
- 完整主稿件（独立 LaTeX 文件）
- 完整 Lean 形式化（千行级代码）
- Annals 投稿格式

**可能的不足**：
- 用了扰动参数 η
- 用碰撞避免处理重复样本
- 用了"生成代数等式" alg(f_eta(B)) = alg(B)

### v2（路径简化）

**关键简化**：
- 引入**辅助矩阵 B**（simple spectrum）+ **目标 T = f(B)**
- 在 B 的特征基中同时对角化 B 和 T
- **共享基**（shared basis）—— 一个基搞定

**v2 vs v1**：
- v1 用复杂 Cauchy 公式
- v2 用辅助基 + Gramian 估计

### v3（进一步简化）

**关键删除**：
- 删除 `f_eta` 扰动
- 删除"碰撞避免"（collision-avoidance）
- 删除"eta → 0 极限"
- 简化核心步骤

**v3 vs v2**：
- v2 处理重复样本用扰动 + 取极限
- v3 直接承认重复样本是合法的（不需要扰动）

### v4（最终稳定）

**关键特征**：
- 直接 Cayley 代数（`isPositiveRealCompletion_of_direct_cayley_identity`）
- Gramian 端点用**第一非常数项**直接估计（无需 Stein 等式）
- 公开路径：`Bₖ → A` 固定外域 + 然后外域收缩到 `W(A)`

**v4 vs v3**：
- v3 仍有些中间步骤
- v4 完全删干净

## 5 · Lean 4 形式化的关键设计

### 信任边界

`AXIOM_AUDIT.md` 明确禁止：

```lean
sorry                  -- ❌ 占位证明
admit                  -- ❌ 接受未证
自定义 axiom            -- ❌ 跳过证明
unsafe 构造             -- ❌ 不安全构造
native-decision         -- ❌ 捷径
编译器信任捷径          -- ❌ 偷懒
警告抑制                -- ❌ 忽略警告
循环端点别名            -- ❌ 假依赖
```

**唯一允许**：`propext` / `Classical.choice` / `Quot.sound`

### 主定理形式化

```lean
theorem holomorphicCrouzeixBound
    {n : ℕ} [Nonempty n] (A : SquareMatrix n ℂ)
    (U : Set ℂ) (hU : isOpen U) (hUW : W A ⊆ U)
    {f : ℂ → ℂ} (hf : DifferentiableOn ℂ f U) :
    ‖holomorphicMatrixEval A f‖ ≤ 2 * maxFunctionModulusOnSet (numericalRange A) f
```

**严格性**：
- 假设严格：`isOpen U`、`W A ⊆ U`、`DifferentiableOn ℂ f U`
- 没有"显然成立"
- 没有"标准库里有"

### 多项式特化

```lean
theorem crouzeixConjecture
    {n : ℕ} [Nonempty n] (A : SquareMatrix n ℂ)
    (p : Polynomial ℂ) :
    ‖polynomialEval p A‖ ≤ 2 * maxPolynomialModulusOnNumericalRange A p :=
  holomorphicCrouzeixBound _ _ _ _ _ p.differentiableOn_polynomial
```

**关键**：直接由 holomorphic 版推出，**没有独立证明**。

### 见证（Sharpness）

```lean
theorem crouzeixConstantTwo_isLeast_finTwo :
    ∀ K, (∀ (n : ℕ) [Nonempty n] (A : SquareMatrix n ℂ)
              (r : RationalFunc ℂ) (h : r.poles ⊆ W A^c),
              ‖rationalMatrixEval r A‖ ≤ K * maxRationalModulusOnNumericalRange A r) →
         K ≥ 2
```

**关键**：用 2×2 Jordan 见证证明 K ≥ 2 是 tight 的。

## 6 · 4 份审计文档的角色

| 文档 | 角色 | 关键作用 |
|---|---|---|
| `MANUSCRIPT_AUDIT.md` | 数学审计 | 逐章节验证数学正确性 |
| `AXIOM_AUDIT.md` | 公理依赖 | 列出所有定理的公理依赖 |
| `FORMALIZATION_MAP.md` | 源-形式化对应 | LaTeX line → Lean declaration |
| `CONTINUATION_STATUS.md` | 当前状态 | 描述主动证明路径 |

**4 份协同** = 多智能体多视角审计的产物。

## 7 · 教训与启示

### 7.1 任务设计

**Crouzeix 任务 prompt 的 5 个必含模块**：
1. 问题陈述（精确无歧义）
2. 完成标准
3. 拒绝借口条款
4. 多智能体管理规则
5. 资源/工具/约束

**最强的一条**：
> "Assume for purposes of this task that a complete affirmative proof exists"

—— 心理预设完整解存在，**不允许"找不到就投降"**。

### 7.2 多智能体

- **不要固定 N 个 agent 走 N 条路径**
- 早期轮次：完全独立
- 后期轮次：可以有部分共享

### 7.3 迭代

- v1 → v2 → v3 → v4 不是过度工程
- 每轮**删掉的代码比新增的多**
- v1/v2/v3 都在 git history（教训不丢）

### 7.4 形式化

- 自然语言证明给"思想"
- 形式化给"严格"
- 两者缺一不可

### 7.5 诚实

- 最终状态说"已通过审计"，不说"已证明"
- "Formal peer review is still pending" —— 同行评议才是终极判定
- AI 协助声明：`"OpenAI ChatGPT contributed to proof development, manuscript preparation, and adversarial checking"`

## 8 · 我的应用建议

### 小型任务（1-3 天）

- 简化多智能体为 2-3 个：
  - 1 个主执行 agent
  - 1 个对抗审计 agent
  - 1 个方法族注册 agent
- 不强求形式化
- 至少一轮简化

### 中型任务（1-2 周）

- 5-10 个 agent
- 维护方法族注册表
- 至少两轮简化（v1 → v2 → v3）
- 选择性形式化（核心论证）

### 大型任务（2+ 周）

- 10-20 个 agent
- 完整方法论（10 条铁律全用）
- 完整形式化（Lean 4 / Coq）
- 多轮迭代（v1 → v2 → v3 → v4）
- 多份审计文档
- 投稿/公开发布

## 9 · 引用与链接

- **GitHub 仓库**：https://github.com/jinshanmu/CrouzeixConjecture
- **任务 prompt**：https://raw.githubusercontent.com/jinshanmu/CrouzeixConjecture/main/crouzeix_conjecture_prompt.txt
- **README**：https://github.com/jinshanmu/CrouzeixConjecture/blob/main/README.md
- **Lean README**：https://github.com/jinshanmu/CrouzeixConjecture/tree/main/Lean
- **AXIOM_AUDIT**：https://raw.githubusercontent.com/jinshanmu/CrouzeixConjecture/main/Lean/AXIOM_AUDIT.md
- **MANUSCRIPT_AUDIT**：https://raw.githubusercontent.com/jinshanmu/CrouzeixConjecture/main/Lean/MANUSCRIPT_AUDIT.md
- **FORMALIZATION_MAP**：https://raw.githubusercontent.com/jinshanmu/CrouzeixConjecture/main/Lean/FORMALIZATION_MAP.md
- **CONTINUATION_STATUS**：https://raw.githubusercontent.com/jinshanmu/CrouzeixConjecture/main/Lean/CONTINUATION_STATUS.md

## 10 · 学习日期

- 首次学习：2026-08-16
- 提炼方法论：v1.0
- 配套 skill：`hard-problem-multi-agent`