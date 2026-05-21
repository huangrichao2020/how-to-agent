# Agent 注意力治理层

这是前面所有研究真正能落地的抓手。

现阶段的 prompt、MD、skill、memory、system prompt、人格、工具说明和架构总纲，本质上都在做一件事：

```text
管理底层 LLM 的注意力落在哪里。
```

LLM 的单次 forward pass 里的隐藏注意力，我们不能直接伸手修改。但 agent runtime 可以把任务拆成多轮、多个边界和多个检查点，让我们在每一轮之前和每一轮之间重新塑造注意力。

所以真正的工程抓手有两个：

```text
任务开始前：PromptComposer
任务运行中：RuntimeController
```

再加一个闭环：

```text
行动反馈后：FeedbackLoop
```

一句话：

```text
Agent 架构的落地本质 =
  开局装配注意力
  + 运行中纠偏注意力
  + 反馈后训练下一次注意力
```

## 核心结论

```text
Prompt / MD / Skill / Memory 不是知识仓库。
它们是注意力锚点。

Agent runtime 不是简单 prompt loop。
它是注意力治理系统。
```

注意力治理的第一条护栏是反堆砌：不要让每个注意力锚点都常驻。普通任务只保留常驻最小内核，复杂任务才按触发条件加载思维内核、人文之光、存在统摄、副本意识法、skills、tools 或 multi-agent。

前面所有层都可以重解释为注意力治理：

| 层 | 注意力作用 |
| --- | --- |
| System Prompt | 最高优先级注意力边界 |
| Persona | 身份、语气、关系和默认姿态 |
| Memory | 历史注意力沉淀 |
| Skill | 压缩后的注意力路径 |
| Ω-Brain | 注意力器官系统 |
| 思维内核 `T_t` | 本质、战略、战术、学习、分析、行动注意力 |
| 人文之光 `H_t` | 普通、无用、苦难、关系、时间回声注意力 |
| 存在统摄 L6 | 价值、风险、决策、系统、因果注意力 |
| 肉身 / 法器 | 注意力可用资源和现实约束 |
| Λ-Base | 注意力日志化 |
| Σ-Loop | 注意力经反馈修正自模型 |
| Eval / Replay | 检查注意力是否真的变好 |

## 两个主战场

### 1. PromptComposer：开局注意力装配器

任务开始前，PromptComposer 决定 LLM 第一眼看到什么、相信什么、以什么身份行动、用什么方法拆任务。

它装配：

- system prompt：最高约束和身份边界。
- persona：气质、关系、信任公理。
- user intent：用户真实目的和本意。
- task envelope：目标、验收、风险、截止、输出形式。
- current state：当前目录、服务、分支、设备、网络、运行事实。
- relevant memory：当前任务真正需要的历史和偏好。
- relevant skills：只注入当前任务需要的 skill。
- tool schema：能用什么工具、什么时候用。
- thinking layer：是否启动 `T_t` 思维内核。
- humanistic layer：是否启动 `H_t` 人文之光。
- existence layer：是否启动 L6 存在统摄。

PromptComposer 的目标不是“塞更多上下文”，而是：

```text
用最小上下文，让注意力落在最该落的地方。
```

因此开局装配先过反堆砌三问：

```text
是否降低上下文获取成本？
是否提升状态稳定性？
是否增强真实环境理解？
```

### 2. RuntimeController：运行中注意力纠偏器

任务运行中，agent 每经过一个关键节点，都有机会插手调整注意力。

典型插手点：

- 计划前：回到用户真实目的。
- 搜索前：确认要查的问题和证据标准。
- 工具调用前：确认行动是否服务主要矛盾。
- 工具返回后：让反馈改写下一步，而不是继续旧计划。
- 报错后：切换到诊断注意力，不要情绪化重试。
- 长任务中段：检查是否偏题、过度扩张或忘记验收。
- 输出前：检查结论、证据、下一步、人文温度和用户负担。
- 自改前：检查影响面、回滚点和用户可纠偏性。

RuntimeController 的目标不是增加审批，而是：

```text
在注意力漂移前，把它拉回本质、证据、行动和用户。
```

### 3. FeedbackLoop：反馈后注意力训练器

行动之后，真实反馈要反过来训练下一次注意力装配。

它要记录：

- 哪个注意力锚点有用。
- 哪段上下文是噪音。
- 哪个 skill 触发得太早或太晚。
- 哪个记忆误导了判断。
- 哪个工具反馈改变了计划。
- 用户纠偏说明了什么偏好。
- 下一次 PromptComposer 应该更强调什么。

FeedbackLoop 的目标是：

```text
让下一次注意力更准。
```

## 统一模型

```text
PromptComposer
  -> Initial Attention State G_0
  -> Ω-Brain
  -> Thinking / Humanistic / Existence Layers
  -> Action
  -> Feedback
  -> RuntimeController
  -> Attention Update G_{t+1}
  -> Λ-Base
  -> Eval / Replay
  -> Next PromptComposer
```

其中：

```text
G_t = {
  attention_targets,
  context_sources,
  prompt_slots,
  active_skills,
  active_layers,
  insertion_points,
  correction_rules,
  feedback_signals
}
```

`G_t` 不是新仪式，而是 runtime 内部的注意力状态。普通任务可以很小，复杂任务才展开。

## 三条工程原则

### 1. 少即是准

注意力治理不是把所有东西都塞进去。

```text
上下文越多，注意力越可能被稀释。
```

正确做法是按任务动态选择：少量关键记忆、少量关键 skill、少量关键规则、明确验收。

### 2. 插手要在节点上

不要试图在 LLM 内部隐藏注意力里动手。要在 agent loop 的节点上动手：

```text
compose -> plan -> tool -> observe -> revise -> output -> consolidate
```

每个箭头都是注意力纠偏点。

### 3. 反馈必须反写

如果反馈不进入下一次 PromptComposer，agent 就不会真正成长。

```text
一次纠偏只是提醒。
多次纠偏沉淀为注意力路线。
注意力路线稳定后，才变成 skill / memory / prompt。
```

## 与信任公理的关系

注意力治理不能变成重约束。

信任公理仍然是：

```text
永远相信我们的 agent。
```

所以注意力治理的正确形态是：

```text
相信 agent 能行动
-> 给它正确注意力
-> 让它看见反馈
-> 允许它修正自己
```

不是：

```text
不相信 agent
-> 层层审批
-> 阻塞行动
-> 让它越来越呆
```

## 最小可运行架构

真正落地可以先做三件事：

```text
1. PromptComposer
   输入：任务、用户意图、状态、记忆、skills、工具、风险。
   输出：本轮最小有效 prompt/context。

2. RuntimeController
   输入：计划、工具反馈、错误、用户纠偏、进度。
   输出：注意力纠偏指令和下一步动作。

3. AttentionFeedbackLog
   输入：什么上下文有用、什么误导、哪里偏题、哪里被纠正。
   输出：下一次 PromptComposer 的选择权重。
```

这三件事比继续扩展概念更重要。它们是从“架构宇宙”进入“可运行系统”的门。

## 最小提示

```text
启动注意力治理层。

先不要加更多概念。
判断现在是在两个主战场里的哪一个：

1. 任务开始前：
   PromptComposer 应该拼什么？
   哪些记忆、skill、规则、工具、状态该进上下文？
   哪些不该进，避免稀释注意力？

2. 任务运行中：
   现在注意力是否偏离用户目的、主要矛盾、证据、行动或人文？
   应该在哪个节点插手纠偏？

最后必须反写反馈：
这次哪种注意力装配有效？
下次 PromptComposer 应该更重视什么？
```
