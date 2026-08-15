# Methodology 05 · v1→v2→v3→v4 迭代协议

> 来源：Crouzeix 项目 21 个 commit 中明确的版本号演进

## 为什么需要迭代

一次成稿的常见陷阱：
1. **思路没稳** —— 第一版可能有错误的依赖
2. **结构冗余** —— 早期版本常有冗余引理
3. **绕过难点** —— 可能存在"用未证引理偷懒"的地方

**迭代**的本质：**让早期版本不进入发布版**，但保留在 Git 历史里。

## Crouzeix 的 4 个版本

从 commit history 反推：

### v1 · 初版（7 月 18-19 日）

```
commit df00105 - "Record candidate proof project status" (Jul 18)
commit 78b99e4 - "Keep ignore rules local and update README" (Jul 19)
commit 3b0fecf - "Add title-named Annals manuscript" (Jul 19)
commit 627bb2a - "Add verified Lean formalization" (Jul 19)
commit 03ae5f1 - "Prepare Annals submission" (Jul 19)
commit 79128d7 - "Finalize Annals submission audit" (Jul 19)
```

**v1 内容**：
- 完整 LaTeX 主稿件
- Lean 4 形式化（初版）
- Annals 投稿格式
- README + 文档

**v1 特点**：完整但可能有冗余，路径可能未最简化。

### v2 · 简化（7 月 30 日）

```
commit ca72eb0 - "Finalize standalone v2 article" (Jul 30)
commit 4910388 - "Formalize auxiliary-basis proof simplification" (Jul 30)
```

**v2 关键简化**：
- 引入"辅助基简化"（auxiliary-basis simplification）
- 删除冗余引理
- 形式化跟随简化

**v2 vs v1 关键变化**：
- 简化前：可能用了复杂的多步构造
- 简化后：用辅助矩阵 B + 共享基 + 单一简化路径

### v3 · 进一步简化（8 月 3-4 日）

```
commit 6ea7484 - "Finalize v3 citation and formalization references" (Aug 4)
commit 8096084 - "Align Lean formalization with simplified v3 proof" (Aug 3)
```

**v3 关键简化**：
- 删除 v1 的"扰动函数 f_eta"构造
- 删除"碰撞避免"（collision-avoidance）
- 删除"生成的代数等式"
- 删除"eta → 0 极限"

**v3 vs v2 关键变化**：
- v2：用扰动处理重复样本
- v3：直接承认重复样本是合法的，不需扰动

### v4 · 最终稳定（8 月 5-6 日）

```
commit 595f6fc - "Finalize v4 proof and formalization" (Aug 5)
commit 565b6a3 - "Keep equation 9 on one line" (Aug 5)
```

**v4 关键特征**：
- 主证明路径：`Bₖ → A` 在固定外域 + 然后外域收缩到 `W(A)`
- 没有 f_eta 扰动
- 直接 Cayley 代数
- Gramian 端点用第一非常数项（无需 Stein 等式）

**v4 是发布版**：进入 Annals 投稿。

### 扩展（8 月 6 日）

```
commit c724883 - "Integrate mass-parameterized completion principle" (Aug 6)
commit efd8f9d - "Add quantum annulus 2-spectral-set article" (Aug 6)
commit 5941585 - "Restore Lean completion sources" (Aug 6)
commit 550a9a1 - "Finalize numerical-range 2-spectral-set preprint" (Aug 6)
commit 9df0783 - "Finalize finite-dimensional and operator-level formulations" (Aug 6)
```

**扩展内容**：
- mass-parameterized 完成原理
- 量子环 2-spectral-set 文章
- 完整 Lean 完成来源

**注意**：v4 已经能发表，但项目扩展到其他相关问题。

## 迭代规则

### 何时提升版本号

每次满足以下条件之一，提升主版本号：
1. **简化路径** —— 主要论证路径改变
2. **删除冗余** —— 移除重要的引理/步骤
3. **改变假设** —— 主定理条件变化
4. **形式化重构** —— Lean 端大改

不满足条件时（修 typo、注释、文档），用 minor version 或不升号。

### 简化规则

每轮迭代做 4 件事：

```
1. 删除冗余
   - 找到不再需要的引理/步骤
   - 验证删除后证明仍成立

2. 统一表述
   - 把分散的论证统一成一个框架
   - 命名统一（同一个概念用同一个名字）

3. 删除捷径
   - 去掉依赖未证明命题的捷径
   - 如果有"v1 用了 X，X 没证但看起来对"，v2 必须删掉 X

4. 重新审计
   - 跑一遍对抗审计
   - 删除的引理不能"复活"（除非有正当理由）
```

### 命名约定

```
v1: initial — 初版
v2: simplification — 路径简化
v3: pruning — 进一步精简
v4: stable — 最终稳定
v5+: extensions — 扩展（不必每次都升号）
```

## 简化 vs 退步

**简化（前进）**：
- 删除冗余引理
- 合并重复论证
- 改用更弱的假设

**退步（不要做）**：
- 删除关键步骤
- 简化到丢失核心思想
- 用未证断言替代已证引理

**判断标准**：
```
简化后的证明：
- 仍然覆盖所有原命题
- 比之前更易读
- 没有新依赖未证引理
```

## Git History 保留所有版本

```bash
git log --all --oneline
- v1: initial formalization (with sorry in places)
- v2: simplified (deleted redundancy)
- v3: pruned (removed v1's perturbation)
- v4: stable (publication version)

# v1 的失败版本在 git history
git show v1:src/Crouzeix.lean
-- shows the v1 implementation with sorry
```

**关键**：
- v1、v2、v3 都在 git history 里
- 工作树只有 v4（稳定版）
- 审计能追溯"曾走过的弯路"

## Crouzeix 的"删除"哲学

`CONTINUATION_STATUS.md` 明确说：

```
## Deleted superseded formalization

The earlier affine f_eta perturbation, finite collision-set,
interpolation-based generated-algebra equality, and eta → 0
formalization has been deleted from the working tree. It is not
part of the current module or declaration inventory. Git history
preserves the prior implementation for historical comparison.
```

**这意味着什么**：
- v1 的扰动论证**没用**了
- 完整删除（git history 保留）
- 不影响当前 v4 的完整性（因为 v4 不再依赖它）

**核心教训**：简化不是"重写"——是"删除"。每轮迭代**删掉的代码比新增的多**。

## 实战要点

### 不要在 v1 时就追求完美

v1 的目标是"完整 + 可读"，不是"最优"。v2/v3 才追求最优。

### v1 → v2 的关键是找"看似必要但其实不必"的步骤

常见模式：
- v1 用扰动参数 η，v3 删除（直接接受）
- v1 用复杂的 Cauchy 公式，v2 改用紧性选择
- v1 用多层归纳，v2 改用单层构造

### v3 → v4 的关键是消除"v1 的影子"

v3 经常还保留 v1 的术语/结构。v4 应该**完全独立**地写：
- 不再提 "v1 的扰动如何如何"
- 不再保留 "originally we did X, now we do Y" 的注释
- 只保留干净的最终论证

### 何时停止迭代

满足任一条件：
- v_n 与 v_(n+1) 几乎相同（diff < 5%）
- 对抗审计找不到新漏洞
- 已达发表/交付标准

## 完成检查清单

参见 `06-completion-checklist.md`。

## 下一步

- 完成检查清单 → `06-completion-checklist.md`