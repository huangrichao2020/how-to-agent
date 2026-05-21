# GA 架构实施映射

这份文档不是新的理论层。

它的作用是把 `how-to-agent` 的成熟架构，逐条映射到 GenericAgent 的真实源码、测试和运行证据里。以后改 GA 时，不能只说“符合道德经、人道、存在经”，而要回答：

```text
这个概念落在哪个模块？
运行中什么时候触发？
有什么测试证明？
有什么真实任务证据？
剩下的缺口是什么？
```

一句话：

```text
how-to-agent 是最高参考。
GenericAgent 源码是肉身。
实施映射是二者之间的经络。
```

## 使用原则

- 先读最高参考，再读源码。
- 先找已有模块，再决定是否新增模块。
- 先收束主链路，再加旁路能力。
- 先要测试和运行证据，再宣称架构完成。
- 文档只记录已落地、正在落地、明确缺口，不把愿望写成事实。

## 三经到源码

| 架构层 | how-to-agent 定义 | GA 当前落点 | 状态 | 验证方式 | 缺口 |
| --- | --- | --- | --- | --- | --- |
| Agent 道德经 / 天道 | 收束注意力、控制上下文、避免执念和流程堆砌 | `attention_governance.py` 的 `PromptComposer`、`RuntimeController`；`task_lifecycle.py` 的 `tiandao` | 已初步落地 | `tests/test_attention_governance.py` 检查 `Task Lifecycle 三经`、运行中纠偏和工具后反馈 | 还要把更多真实长任务反馈反写进下一次 PromptComposer |
| Agent 毛选 / 人道 | 主要矛盾、调查研究、用户真实需要、行动路线 | `task_lifecycle.py` 的 `rendao`；`agentmain.py` 任务开始/结束接入 | 已初步落地 | 生命周期头部包含 `main_contradiction`、`user_need`、`action_route` | 需要把更多场景分类从启发式升级为日志驱动 |
| 存在经 / 存在道 | 价值、风险、决策、系统变化、因果记录 | `task_lifecycle.py` 的 `cunzaidao`；`record_lifecycle_event()` 写入 cognition event | 已初步落地 | 任务开始、完成、失败写入 `memory/cognition/task_lifecycle/*.jsonl` | 需要建立稳定的回放和统计面板 |

## 注意力治理到源码

| 能力 | 代码位置 | 运行时插手点 | 验收 |
| --- | --- | --- | --- |
| 开局 prompt/context 拼接 | `attention_governance.py::PromptComposer.compose()` | 每次 agent loop 开始 | 组合结果必须包含用户意图、任务验收、必要上下文和三经坐标 |
| 运行中纠偏 | `attention_governance.py::RuntimeController.after_tool()`、`_turn_correction()` | 工具失败、重复工具、无工具漂移、中段检查 | 输出 `[THREE CLASSICS CORRECTION]`，但不变成审批流程 |
| 结束后反馈 | `RuntimeController.on_task_complete()`、`on_task_error()` | 任务成功或失败 | 记录 task lifecycle after_task 事件 |
| 反堆砌 | `agent-anti-bloat-context-engineering` 指导；GA 里由 PromptComposer/历史窗口承担 | 每次装配上下文 | 不把全部世界观常驻进每个任务 |

## 大脑、肉身、法器

| 概念 | GA 解释 | 当前落点 | 下一步 |
| --- | --- | --- | --- |
| 大脑 | 服务思考的功能结构，不是 LLM 水龙头 | `attention_governance.py`、`task_lifecycle.py`、`state_store.py`、`ga.py` 的认知/工具/记忆命令 | 把脑区职责整理成模块级 README 或架构注释 |
| 肉身 | agent 源码和运行程序本身 | `/Users/tingchim2pro/Desktop/GenericAgent`，入口 `agentmain.py`、`frontends/fsapp.py` | 建立肉身境界评分：启动、恢复、测试、重启、观测 |
| 法器 | 所在设备、网络、CLI、Feishu、模型供应商、反代 | Feishu gateway、Gemini/Qwen/OpenAI 路由、scheduler、外部 CLI | 建立法器状态快照，避免把设备/网络问题误判为心智问题 |
| 灵根 | 数学/日志/反馈架构的原始学习属性 | cognition events、task lifecycle、attention feedback log | 把日志稳定转为可评估数据样本 |
| 资质 | 参数调整效率和效果 | 测试、回放、prompt 纠偏、模型路由 fallback | 增加可量化指标：修正次数、完成率、上下文噪音率 |

## Cron / Dream 到源码

Hermes 已经有认知荆轮报告和 Cronjob Response。GA 现在对应能力不是“看起来像 Hermes”，而是有自己的运行落点：

| 能力 | GA 当前落点 | 状态 | 验收 |
| --- | --- | --- | --- |
| 定时任务注册表 | `cron_runtime.py` 的 `load_job_registry()`、`format_job_registry()` | 已落地 | `/cron`、`/jobs`、`/job` 能查看任务 |
| 手动 pause/resume/trigger | `cron_runtime.py`、`frontends/fsapp.py` 命令分支 | 已落地 | `/cron pause|resume|trigger <job_id>` |
| 调度循环 | `frontends/fsapp.py` + `reflect/scheduler.py` | 已落地 | `GA_SCHEDULER_ENABLED` 默认启用；启动日志能看到 scheduler 状态 |
| Hermes 风格报告 | `format_cronjob_response()` | 已落地 | `tests/test_cron_runtime.py` |
| Dream 旁路复盘 | `ga.py do_cognitive_dream`、`sche_tasks/learning_brief_4h.json` | 部分落地 | 需要把报告质量和反写路径继续稳定化 |
| Dream 反写链路 | `dream_writeback.py`、`cognitive_dream.py`、`attention_governance.py` | 已初步落地 | Dream/feedback/replay 生成 `dream_writeback_hint`，PromptComposer 下一轮轻量注入；同时生成可回滚 promotion proposals |

## 输出形态到源码

Dream 反写不能只停在报告里。对用户可见的输出形态，也要变成运行时策略：

| 能力 | GA 当前落点 | 状态 | 验收 |
| --- | --- | --- | --- |
| 普通闲聊短答 | `cognitive_response_policy.py` 的 Dream output bias | 已落地 | 有 `dream_writeback_hint` 时，普通群聊保持自然短答，不默认卡片/工作台 |
| 长任务工作台 | `cognitive_response_policy.py`、`frontends/fsapp.py` 群聊提示 | 已落地 | 长任务才启用任务工作台，并尽量合并到一个工作台 |
| 反卡片泛化 | `tests/test_cognitive_response_policy.py` | 已落地 | 覆盖“不要每个 turn 单独生成一张卡”的策略 |

## 生命周期统计与肉身法器

概念落地以后，还要能被观测。GA 现在把任务生命周期和运行状态接成两条只读面板：

| 能力 | GA 当前落点 | 状态 | 验收 |
| --- | --- | --- | --- |
| 生命周期统计 | `task_lifecycle.py::summarize_task_lifecycle()` | 已落地 | 从 `memory/cognition/task_lifecycle/*.jsonl` 统计 started/completed/errors/corrections/completion_rate |
| 生命周期可读报告 | `task_lifecycle.py::format_task_lifecycle_stats()` | 已落地 | 能输出最近任务类型、风险、最新问题 |
| 肉身状态 | `runtime_status.py` | 已落地 | 展示源码根、PID、uptime、checkpoint、lifecycle event 文件 |
| 法器状态 | `runtime_status.py`、`frontends/fsapp.py::_agent_status_text()` | 已落地 | `/status` 展示模型、队列、飞书 WS、scheduler、cron registry、Dream writeback、proxy 状态 |

## Dream Proposals 到源码

Dream promotion proposals 不能长期停留在 proposal 文件里。当前已经执行的条目：

| Proposal | GA 当前落点 | 状态 | 验收 |
| --- | --- | --- | --- |
| 普通闲聊短答 / 长任务工作台 | `cognitive_response_policy.py`、`frontends/fsapp.py` | 已落地 | `tests/test_cognitive_response_policy.py` |
| 单次 understanding 不自动升格 | `dream_writeback.py`、`tests/test_cognitive_dream.py` | 已落地 | 低信号只生成测试建议，不直接改 prompt adjustment |
| 工具错误先诊断失败类型 | `attention_governance.py::after_tool()` | 已落地 | 工具错误返回 `[ATTENTION CORRECTION]` 与三经纠偏 |
| skill route bias | `attention_replay.py`、`skill_registry.py` | 已落地 | replay 负反馈会降低误召回 skill 权重 |
| 用户边界 preflight | `attention_governance.py::before_tool()`、`agent_loop.py` | 已落地 | 状态变更工具前记录 `[BOUNDARY CHECK]`，下一轮提示核对对象、范围和禁止项 |

## Skill 工程化到源码

`how-to-agent` 的 Skill 工程化不意味着 GA 要把整个项目当一个 Skill 读。

正确落点是：

```text
Skill = 可复用能力包
GA 源码 = 运行时肉身
how-to-agent = 改造指导手册
```

GA 需要从 Skill 工程化里吸收三件事：

- 渐进披露：只加载触发描述，触发后再读主文件，长资料放 references/scripts/assets。
- 确定性下沉：排序、校验、格式转换、状态扫描交给脚本，不靠 LLM 即兴记住。
- 生命周期管理：skill 要能安装、索引、使用、验证、淘汰。

不要吸收的东西：

- 不要把所有架构文档塞进系统 prompt。
- 不要用 Skill 替代源码改造。
- 不要把一次性聊天内容沉淀为长期能力。

## 运行证据账本

每次宣称 GA 架构完成某一层时，至少留下四类证据之一：

| 证据 | 例子 |
| --- | --- |
| 源码证据 | `task_lifecycle.py` 新增字段；`frontends/fsapp.py` 新增命令 |
| 测试证据 | `pytest -q tests/test_attention_governance.py tests/test_cron_runtime.py` |
| 运行证据 | Feishu `/cron` 输出；scheduler 启动日志；done 报告文件 |
| 反馈证据 | 用户纠偏后，PromptComposer 或运行策略发生真实变化 |

如果四类证据都没有，只能叫“想法”，不能叫“架构完成”。

## 当前 GA 状态判断

按 `how-to-agent` 总纲看，GA 已经从单纯 prompt loop 进入“有肉身、有经络、有旁路、有反馈”的早期运行时阶段：

- 天道：已有注意力治理入口。
- 人道：已有任务生命周期里的主要矛盾和行动路线。
- 存在道：已有价值、风险、因果记录的结构。
- 肉身：源码有真实模块承载，不是只靠 prompt。
- 法器：Feishu、scheduler、CLI、模型路由已开始进入架构视野。
- 万物生：候选能力能通过 cron、dream、tests、反馈继续择优。

但还不能说完全成熟。下一阶段重点不是再发明概念，而是：

```text
把每个概念都接到真实 trace、真实测试、真实回放和真实自动修正。
```

## 2026-05-21 实测记录

本次实施映射已用配套脚本扫描当前 GA：

```bash
python3 /Users/tingchim2pro/Desktop/how-to-agent/skills/ga-implementation-map/scripts/score_ga_architecture.py \
  --ga-root /Users/tingchim2pro/Desktop/GenericAgent
```

结果：

```text
Three Classics lifecycle: PASS
Attention governance: PASS
Cron and Dream sidecar: PASS
Dream writeback loop: PASS
Output shape policy: PASS
Task lifecycle statistics: PASS
Body artifact status panel: PASS
Boundary preflight correction: PASS
Body resume and checkpoint: PASS
Runtime evidence ledger: PASS
```

验证过程还跑了真实根目录 smoke：

```text
PromptComposer -> RuntimeController.on_task_start()
PromptComposer -> RuntimeController.on_task_complete()
```

已在 GA 根目录生成：

```text
/Users/tingchim2pro/Desktop/GenericAgent/memory/cognition/task_lifecycle/lifecycle-2026-05-21.jsonl
```

并包含 `before_task` 与 `after_task` 两类事件。

本次还补上 Dream 反写链路：

```text
Dream / feedback_distill / attention_replay
  -> dream_writeback.py
  -> memory/cognition/dream_writeback/latest.json
  -> PromptComposer.dream_writeback_hint
  -> memory/cognition/dream_writeback/promotion-proposals.json
```

真实输出：

```text
/Users/tingchim2pro/Desktop/GenericAgent/memory/cognition/dream_writeback/2026-05-20.json
/Users/tingchim2pro/Desktop/GenericAgent/memory/cognition/dream_writeback/promotion-proposals.json
```

其中包含边界收束、普通闲聊短答、长任务工作台、工具错误后先诊断、候选 skill 误召回等下一轮轻量偏置。

本次继续执行了其中的“输出形态”proposal：

```text
dream_writeback_hint
  -> cognitive_response_policy.py
  -> 普通闲聊自然短答
  -> 长任务才工作台
  -> 同一长任务尽量合并，不每 turn 单独卡片
```

这条改造只改变响应策略和群聊提示，不改消息发送主链路，因此风险较低；验证由 `tests/test_cognitive_response_policy.py` 承担。

本次继续补上“可观测肉身/法器”：

```text
task_lifecycle jsonl
  -> summarize_task_lifecycle()
  -> completion_rate / corrections / recent_errors
  -> runtime_status.py
  -> /status 肉身/法器面板
```

这条改造同样只读本地事件和运行快照，不做外部请求，不触发模型调用。

本次继续执行“边界类 runtime pattern”：

```text
用户说 不要 / 不能 / 只改 / 还原 / 别碰
  -> RuntimeController.before_tool()
  -> 状态变更工具触发 boundary_preflight
  -> agent_loop 把 preflight correction 接进下一轮提示
```

它不会阻断工具，也不会新增审批；它只在发生可能改状态的动作时，把注意力拉回真实对象、范围、禁止项和可回退边界。

promotion proposal 只提出下一步，不直接热改运行时默认行为。每条 proposal 必须带：

- `decision`
- `target`
- `validation`
- `next_action`
- `rollback`

这保证 Dream 可以推动真实变更，但不会在夜间绕过测试把 GA 改挂。

配套测试：

```bash
pytest -q tests/test_runtime_status.py tests/test_cognitive_response_policy.py tests/test_cognitive_dream.py tests/test_attention_replay.py tests/test_attention_governance.py tests/test_cron_runtime.py tests/test_codex_runtime.py
```

结果：

```text
64 passed
```

## 下一步改造顺序

1. 扩展 GA 架构评分脚本：继续接入更多源码模块、测试、cron registry、lifecycle event 和真实运行指标。
2. 给 task lifecycle 加统计聚合：按任务类型统计风险、纠偏、完成率和重复问题。
3. 执行 Dream promotion proposals：把最高分 proposal 逐条转成小补丁、测试和回滚点。
4. 给肉身/法器建立状态面板：进程、模型、网络、scheduler、checkpoint、最近错误。
5. 把 Hermes 同步到同一套实施映射，而不是只同步文档口径。

## 最小提示

```text
[GA IMPLEMENTATION MAP]
- 这条 how-to-agent 原则落到 GA 哪个模块？
- 它在任务开始、中途、结束还是旁路触发？
- 有测试、日志、报告或用户反馈证据吗？
- 它降低上下文成本、提升状态稳定性，还是增强真实环境理解？
- 如果没有源码落点，下一步最小改动是什么？
[/GA IMPLEMENTATION MAP]
```
