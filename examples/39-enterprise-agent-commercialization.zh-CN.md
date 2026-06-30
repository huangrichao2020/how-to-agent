# 示例 39：企业级 Agent 商业化

学习来源：
[hmy1990116/ai-training-methodology](https://github.com/hmy1990116/ai-training-methodology/tree/main)。

## 为什么重要

企业级 agent 不能被卖成"更厉害的 prompt"或"很酷的自动化"。它真正卖的是：
把企业的模糊焦虑翻译成可诊断、可交付、可复购的业务变化。

从源仓库里提炼出的关键链路是：

```text
企业痛点
  -> 业务流程地图
  -> AI 改造优先场景
  -> 原子级 Skill 设计
  -> 企业家/管理层内训
  -> 付费落地路径
  -> 证明效果、复购、转介绍
```

所以，一个企业级 agent 方案必须同时有两套系统：

1. 交付系统：把真实工作场景拆成 agent skill；
2. 转化系统：把客户注意力转成信任、购买、交付证明、续费和转介绍。

## 提炼出的方法

源仓库用"两层拆解法"处理企业 AI 落地：

| 层次 | 买方真正关心的问题 | Agent 交付物 |
| --- | --- | --- |
| 管理层 | 哪个业务流程最值得先改？ | 流程地图、痛点排序、优先场景 |
| 执行层 | 哪些具体动作能变成 AI skill？ | 原子动作清单、自动化等级、落地路径 |

映射到企业级 agent，就是：

| 企业对象 | Agent 翻译 |
| --- | --- |
| 业务流程 | 工作流边界和数据流 |
| 高频、高耗时、低价值、强规则任务 | 第一批自动化候选 |
| 原子动作 | skill 单元或工具调用 |
| 六维评估 | 自动化风险和人审策略 |
| A/B/C 三类 skill | 全自动、AI 主导、人类辅助决策 |
| 案例库 | 销售证明和交付模板 |

## 企业级 Agent 的产品形态

不要从模型选择开始卖。先卖诊断。

```text
诊断工作坊
  -> 业务流程地图
  -> Top 3-5 agent 场景
  -> quick-win skill 原型
  -> 30/60/90 天落地路径
  -> 管理层看板
  -> 陪跑或战略顾问
```

最强的第一产品通常不是"定制开发一个 agent"，而是一次能产出明确交付物的工作坊：

- AI 成熟度诊断；
- 工作流地图；
- 优先场景清单；
- 第一个 skill spec；
- 落地提案。

当客户已经在诊断里看见自己的业务被翻译成 agent 路线图，后续实施服务就不是硬推销，而是顺理成章的下一步。

## 售卖与转化闭环

源仓库把业务侧拆成四阶段闭环。放到企业级 agent，就是：

| 阶段 | 目标 | 企业级 agent 版本 |
| --- | --- | --- |
| 引流获客 | 让客户停下来 | 行业痛点、标杆数据、反直觉诊断 |
| 咨询转化 | 让客户信任 | 问出客户自己答不好的关键问题 |
| 课程交付 | 让客户感到进展 | 现场产出流程图、评分表、skill spec |
| 复购续费 | 让客户想买下一层 | 用 before/after 证明下一步杠杆 |

关键不是打折，而是在每个触点设计"下一步钩子"。

例子：

- 引流钩子：员工可能已经在用 AI，但公司没有拿到 ROI。
- 转化钩子：哪个重复任务消耗管理注意力，但又小到不值得传统软件项目立项？
- 交付钩子：今天结束前，把一个真实流程变成 agent skill spec。
- 复购钩子：第一个流程已经可见，下一步是把它变成可复制的组织系统。

## 课程与工作坊设计

对企业家和管理层，不要把课程做成工具操作教学。目标是：认知重塑 + 行动推动。

6 小时内训可以这样组织：

| 模块 | 目的 | 产出 |
| --- | --- | --- |
| 1. 认知重塑 | 打破浅层 AI 想象 | AI 成熟度自诊 |
| 2. 方法导入 | 教会两层拆解法 | 业务流程地图 |
| 3. 场景实战 | 套到学员自己的业务 | 优先场景和 skill 类型 |
| 4. 行动路径 | 把注意力转成行动 | 72 小时承诺和后续服务 |

每个模块都必须有 artifact。只有概念，转化很弱；有地图、评分表、skill spec，下一步服务就更容易成交。

## 可交付物

这些 artifact 同时是实施输入和销售证明：

| Artifact | 为什么能卖 |
| --- | --- |
| AI 成熟度地图 | 让管理层知道自己在哪 |
| 工作流痛点地图 | 让浪费可见 |
| 场景优先级矩阵 | 告诉客户先做什么 |
| Skill 类型组合 | 解释自动化边界和人审节点 |
| 30 天 quick-win 计划 | 降低购买风险 |
| Before/After 复盘报告 | 形成续费和转介绍证据 |

## 反模式

- 还没说清客户流程痛点，就开始卖"AI agent"。
- 给管理层讲 prompt 技巧，而不是组织级杠杆。
- 第一次咨询把方案全讲完，没有下一步钩子。
- 用假稀缺制造紧迫感。
- 把交付当结束，而不是复购起点。
- 一个付费流程都没跑通，就急着做完整平台。

## 可复用 Prompt

```text
像要售卖并落地一个企业级 agent 系统一样研究目标企业。

第一层，从管理层视角画业务流程：
- 核心流程
- 支撑流程
- 高频、高耗时、低价值、强规则痛点
- 最值得 AI 改造的 Top 3-5 场景

第二层，从执行层视角拆优先场景：
- 原子动作
- 每个动作的输入和输出
- 数据结构化程度
- 错误风险
- 是否需要人审
- A/B/C skill 类型

然后设计商业路径：
- 引流钩子
- 诊断问题
- 工作坊交付物
- quick-win 实施方案
- 30/60/90 天落地节奏
- 复购或顾问服务

不要从模型选择或工具选型开始。先从业务痛点、可见 artifact 和下一步付费转化开始。
```

## 来源索引

- 仓库总览：
  [README](https://github.com/hmy1990116/ai-training-methodology/tree/main)
- 两层拆解法：
  [methodology/two-layer-decomposition.md](https://github.com/hmy1990116/ai-training-methodology/blob/main/methodology/two-layer-decomposition.md)
- 业务闭环：
  [business-playbook/README_项目自述与概述.md](https://github.com/hmy1990116/ai-training-methodology/blob/main/business-playbook/README_项目自述与概述.md)
- 咨询转化：
  [stage-2-conversion.md](https://github.com/hmy1990116/ai-training-methodology/blob/main/business-playbook/stage-2-conversion.md)
- 课程体系：
  [course-system/README_项目自述与概述.md](https://github.com/hmy1990116/ai-training-methodology/blob/main/course-system/README_项目自述与概述.md)
- 企业案例：
  [social-ecommerce/skill-landing-report.md](https://github.com/hmy1990116/ai-training-methodology/blob/main/enterprise-cases/social-ecommerce/skill-landing-report.md)
