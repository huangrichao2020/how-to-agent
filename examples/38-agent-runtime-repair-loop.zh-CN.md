# 示例 38：Agent 运行时修复闭环

这份记录来自 2026-05-25 对 GenericAgent 近期提交和未提交改动的复盘。

当一个 agent runtime 最近被频繁改动，而你需要把修复经验沉淀成可复用方法时，用这个示例。

核心规则：

```text
运行时修复不是 patch 跑通一次就结束。
要把失败模式命名，验证真实进程，补上回归路径，并归档到后续 agent 找得到的地方。
```

## 近期已提交改动

GenericAgent 最近几次提交形成了一条比较清楚的主线：

| 领域 | 改动 | 方法论 |
| --- | --- | --- |
| 飞书富文本 | Markdown 表格能正确渲染为飞书富文本 | 输出层要理解格式，而不是把 Markdown 当纯文本倒出去 |
| 任务工作台 | 飞书任务卡增加 thinking summary | 长任务要给用户可读进展，而不是刷 raw tool trace |
| 对话运行时 | conversation runtime、task runner、lifecycle、smart restart、hot reload 解耦 | 前端负责展示，共享 runtime 负责任务监控和生命周期 |
| 记忆文档 | 压缩 memory/SOP 噪声，新增 creative-writing skill | 删掉过期流程噪声，保留高信号 skill |
| Lark 文档 | 文档创建和 provider retry 加固 | 外部连接器需要清楚的重试语义和测试 |

把窗口再往前拉，近期提交可以分成七个运行时簇：

| 提交簇 | 改了什么 | 可沉淀方法 |
| --- | --- | --- |
| 前端视觉验证门（`51b5fde`、`04c5078`、`e079616`、`69dbcc9`） | web presence、motion-video 等 skill 收紧到截图/render 验证 | 视觉任务必须看真实渲染面，不能只生成文件 |
| 认知运行时治理（`3200c45` 及附近 cognition 提交） | attention governance、cognitive store、dream writeback、token budget、runtime status、prompt contract 接进主循环 | 认知不是隐藏自言自语，而是可观察运行行为 |
| 运行证据账本（`9414818`、`e5329ed`） | 飞书消息、scheduled context、cognitive events、Rust bridge events、runtime ledger 变成可审计证据 | 可调试性来自事件证据；证据库也要干净关闭资源 |
| 飞书任务流稳定化（`3f1f392`、`d7dd09e`、`0797457`、`d72888f`） | 保留 raw Feishu intent，稳定任务卡/反应，纠偏 follow-up 不丢，闲聊和工作台输出分开 | 连续对话先是事件系统契约，然后才是 prompt 问题 |
| 本地浏览器与工具链扩展（`bf90e0f`） | `local_browser_reader.py`、tool schemas、MCP 配置、loop detection、安全重启 skill 和 SOP 架构一起落地 | 新工具要同时有 schema、测试、操作说明和真实环境验证 |
| 运行时韧性（`8a39ae9`、`d31a141`） | stale Rust runtime lock、自重启、热加载、lifecycle、task runner 边界被拆开 | 长久在线 agent 需要清楚的重启边界和能干净失败的 sidecar |
| 记忆与检索（`bfdcb70`、`f8cdfeb`） | MemoryHub episode recall、压缩 memory SOP、新 creative-writing skill | 检索系统应减少当前任务混乱，而不是堆更多文本 |

这条更长窗口说明 GA 的真实架构方向是：

```text
输出工艺
  + 连续对话
  + 事件证据
  + 结构化认知
  + 可重启运行边界
  + 压缩后的耐久记忆
```

这些线一起推进时，agent 会更像“活的”，不是因为它说了更多话，而是因为它的过程可见、可恢复，并且更不容易丢掉用户最新指令。

再往前看，2026-05-17 到 2026-05-19 的提交能看到这些能力的根系：

| 根层 | 代表提交 | 方法论 |
| --- | --- | --- |
| 飞书工作台优先 | `e5a0408`、`789d26b`、`4f672c8`、`03fad96`、`de47907` | 聊天 agent 先要有输出工作台，长任务才会可信 |
| 认知作为旁路 | `5d484ed`、`e652075`、`38fcf78`、`6fd4a2e`、`dde287d` | 认知要可见但不要仪式化，不要让普通回复都过审批感流程 |
| 学习管道 | `e652075`、`40c7182`、`b3051f9`、`2f904d2` | 学习请求需要直达路径、结构化产物和练习循环 |
| 事件底座 | `4cc135b`、`9312eb0`、`5d92357`、`2c74a57`、`e1b3352` | 如果 agent 有很多内部状态，先让状态变化可记录 |
| 热加载与运行边界 | `df89283`、`c3cefac` | 高频运行时进化需要清楚的 reload 边界和可预测 sidecar 选择 |
| 人类信号和回复语气 | `bb5e86b`、`a4c8701`、`061e3ab`、`bf3dd05` | 更好的行为来自柔和的用户表述和更清楚的内部证据 |
| 修炼式架构 | `7ee651f`、`eb3f643`、`98366cb`、`da5c21a`、`9e3df52`、`4298340` | 隐喻架构只有能映射到测试、工具和运行事件时才有价值 |

这一层补充了一个重要提醒：

```text
不要把内部架构误写成用户面对的仪式。
runtime 可以有认知、修炼、dream、证据和练习循环。
但用户大多数时候只应该感觉到：它听见了、记住了、行动了、汇报清楚了。
```

换句话说，内部子系统必须用可观察行为证明自己：更好的路由、更清楚的报告、更安全的重启、更低 token 浪费、更忠实的记忆，或者更少重复犯错。

这不是“给 agent 多加一点魔法”，而是一条反复出现的清理路线：

```text
用户体感坏了
  -> 找运行时边界
  -> 把边界显式化
  -> 补回归测试
  -> 重启真实服务验证
  -> 把经验归档
```

## 当前未提交改动

这次未提交改动里有两条值得沉淀的线。

### 1. 安全自重启修复

失败现场：

```text
request_self_restart 为了保存重启提示，import 了 frontends.fsapp 来拿 TEMP_DIR。
但 fsapp 正是当前进程入口。
再次 import 会执行模块顶层代码，触发 singleton lock。
worker 在线程里提前退出，没有发出 done。
Feishu runner 一直等，最后任务超时。
```

落地修复：

- `ga.py` 改为通过 `parent.temp_dir` 或项目 `temp/` 保存 restart notice。
- restart 工具不再 import 前端入口文件。
- `tests/test_self_restart.py` 增加回归测试，防止保存 restart notice 时再 import `frontends.fsapp`。
- `agentmain.py` 的 restart preflight 从三个文件扩展到真实 Feishu 启动主链路：agent loop、fsapp、飞书渲染器、smart restart、tool policy、work state、tool result contract。

方法论：

```text
不要在共享工具路径里 import 正在运行的入口文件。
入口文件会拿锁、启动客户端、修改进程状态，甚至主动退出。
共享逻辑应该通过 parent/context 接收运行时路径和状态。
```

### 2. 结构化 WorkState

新增文件：

- `work_state.py`
- `tool_result_contract.py`
- `tests/test_work_state_contract.py`
- `tests/fixtures/conversation_eval_cases.json`

目标：

```text
给每个实时任务维护一份小型结构化状态：
目标、已知事实、缺失信息、当前计划、决策、证据引用、用户追加约束、下一步、停止条件、风险级别。
```

agent loop 会把 WorkState 附到下一轮模型输入里，并从规范化后的工具结果里更新它。

为什么重要：

- 长聊天记录不适合精确恢复当前任务状态。
- 工具结果不应该只是大段文本，还应该能变成状态补丁。
- 用户运行中追加的话要进入显式 steering，而不是藏在 transcript 里。
- 回归 fixture 应保留真实失败：比如“执行7”、第二条消息是新任务、短答要承接上一问。

方法论：

```text
长任务 agent 应在 transcript 旁边维护一份小型 typed work state。
transcript 保存上下文，WorkState 保存操作真相。
```

## 修复检查清单

当 GA、Hermes 或另一个本地 agent 变得不对劲时：

1. 先看真实进程状态。

```text
launchctl print ...
ps ...
tail runtime logs
```

不要先从理论猜。先确认进程是活着、重启中、被阻塞、重复启动，还是只是输出质量差。

2. 分离用户症状和内部失败。

例子：

- 用户看到没回复。
- runner 等不到 `done`，最后 timeout。
- worker 线程提前退出。
- restart preflight 拦截退出。
- singleton lock 杀掉重复 import。

每一层的修法都不一样。

3. 给不安全边界命名。

常见边界名：

- 前端入口被当成库 import
- 重启预检范围太窄
- 工具结果没有结构
- 用户 follow-up 被吞
- 富文本按纯文本渲染
- 工作台展示 trace 而不是 outcome

4. 只修最小运行时边界。

优先：

```text
通过 parent/context 传依赖
抽出共享 helper module
加 typed result contract
扩大 preflight 覆盖
在事件边界排队或吸收消息
```

避免：

```text
import 入口文件
只加 prompt 规则
盲目重启
把异常吞成笼统 failed
```

5. 真实失败要变成回归测试。

好的 agent runtime 测试不一定是完整 E2E，很多时候是一块小小的“失败化石”：

```text
这个 import 永远不能发生
这句短消息必须承接上一帧
运行中完整新任务必须排队
失败工具结果必须更新 missing_info 和 next_action
```

6. 验证真实服务。

对于 LaunchAgent 托管的服务，完成标准至少是：

```text
preflight 通过
相关测试通过
launchctl kickstart 成功
新 PID 可见
startup log 显示 websocket/client 成功
没有新的 SyntaxError 或 singleton lock warning
```

7. 把方法归档。

修完不要只留在聊天里。把经验放进 how-to-agent 或 skill。下一次 agent 不应该再从原始日志里重新踩同一个坑。

## 最小提示

```text
[AGENT RUNTIME REPAIR LOOP]
- 从真实证据开始：进程、supervisor、日志、队列状态、当前 diff。
- 分清用户症状、runner 行为、worker 失败和真正的边界问题。
- 共享工具不要 import 活入口；运行路径和状态通过 parent/context 传入。
- 工具结果要足够结构化，能更新当前 WorkState。
- 为真实失败补回归测试，不只测 happy path。
- restart preflight 要覆盖启动 import 链。
- 重启真实服务，并验证 PID 和启动成功，再说完成。
- 经验可泛化时，归档到 how-to-agent 或 skill。
[/AGENT RUNTIME REPAIR LOOP]
```
