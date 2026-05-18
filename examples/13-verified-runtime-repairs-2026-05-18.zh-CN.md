# 示例 13：2026-05-18 已验证运行时修复

这份记录只写已经在 GA/Hermes 真实运行中验证过的修复，不把未验证的架构想法写成方法论。

今天的主线很清楚：主链路要干净，认知架构去维护记忆、方法、技能、印象和人格；输出层要把工具痕迹翻译成人能看的工作流。

## 已验证修复 1：把工具流翻译成工作总结

问题：

- GA 飞书卡片里几乎只有 raw tool calls。
- 卡片外壳已经有了，但内容还是 debug trace。
- 用户看到的是“它很忙”，不是“它做成了什么”。

修复：

- 把 `tool_results` 接进飞书任务流渲染层。
- 把工具调用翻译成人话动作，例如 `读取 USER.md`、`更新 USER.md`。
- 默认展示 `本轮动作`、`结果`、`Agent 输出`，不再倾倒 raw args。
- 原始 trace 只保留在显式 debug 开关后面。

验证：

```text
GA: 278 passed, 3 skipped
GA audit: score 100, finding_count 0
运行时: 本地 GA gateway 已重启并加载新版 Feishu app
```

可复用规则：

```text
长任务输出必须告诉用户发生了什么、改了什么，而不只是调用了哪个工具。
```

## 已验证修复 2：Hermes 工作台卡片降噪

问题：

- Hermes 飞书卡片直接暴露大段 `execute_code`、`delegate_task` JSON。
- loop warning、`original_result`、代码和子任务 envelope 全混在卡片里。
- 结构看起来更复杂，体感反而更糟。

修复：

- 长任务才用工作台卡片。
- 卡片结构改成 `任务规划`、`执行过程`、`动作`、`结果`、`结论`。
- 抑制 `_runtime_warning`、`original_result`、超长 JSON 和重复工具参数。
- `delegate_task` 只摘要子任务结论，不倒原始 envelope。

验证：

```text
Hermes Feishu tests: 198 passed
M1 runtime: 已同步 gateway 文件，py_compile 通过，Feishu 测试通过
运行时: M1 Hermes gateway 已重启并加载新版 adapter
```

可复用规则：

```text
频道渲染层负责翻译工具痕迹，不要让用户阅读内部事件格式。
```

追加修复：

- 兼容没有 `Turn N` 标题的旧工具流，例如 `🐍 execute_code(['code'])`
  和 `🔁 delegate_task(['tasks'])`。
- 这类旧流仍要进入工作台卡片，但用户只看任务、动作、结果和结论。
- 原始参数、`original_result` 和大段 JSON 必须停留在调试层。

## 已验证修复 3：闲聊不要卡片化

问题：

- Hermes 把普通闲聊也做成卡片。
- 短回复因此显得僵硬、正式、没有活人感。

修复：

- 闲聊和短回答保持普通文本。
- 中等结构回答用富文本/post。
- 工作台卡片只给工具密集任务、定时报告、重启报告和长任务。

验证：

```text
输出模式测试覆盖：多行闲聊、轻 Markdown、工作台 trace、
edit/update message 路径、紧凑报告行为。
GA Feishu 输出相关测试：37 passed
```

可复用规则：

```text
用能承载当前任务的最轻输出表面。
```

## 已验证修复 4：迁移后的运行时自我认知校准

问题：

- Hermes 已经从阿里云迁到 M1 Mac。
- 活跃语义记忆、wiki 自我页面和手册仍把当前运行时写成 Alibaba Cloud Linux 和阿里云网络限制。
- agent 因此老把当前网络问题按阿里云环境推理。

修复：

- 用 M1 当前事实替换活跃自我认知。
- 把阿里云经验降级成历史经验，只在 `ssh aliyun` 或 `ssh aliyun2` 任务里适用。
- 更新渲染记忆、wiki 自我页面和运行手册。
- 把临时备份移出活跃检索路径。
- 重启 gateway，清掉已加载的旧上下文。

验证：

```text
M1 事实: hostname tingchi-m1, macOS, arm64, 8GB RAM
活跃 memory/wiki 反搜: 旧阿里云当前宿主机描述已移除
运行时: M1 Hermes gateway 已重启
仓库手册: 已提交并 push
```

可复用规则：

```text
当前运行时事实，高于历史环境记忆。
```

## 共同教训

这些修复指向同一条架构规则：

```text
主循环保持直接。
认知架构维护记忆、方法、技能、印象和人格。
输出渲染层翻译工具痕迹。
运行时身份必须真实且当前。
```

不要用更多审批仪式、pending 队列或认知包装层解决体感变差的问题。如果一次“认知升级”之后 agent 反而更不好用，要优先检查是不是新增包装层挡在了用户输入和有效行动之间。

## 未来同类修复检查表

完成前必须确认：

1. 真实运行时进程确实加载了改动文件。
2. 为具体失败形态补了测试。
3. 跑过目标测试和相关范围测试。
4. 代码或记忆在启动时加载时，重启 live gateway。
5. 反向搜索活跃 memory/wiki/manual，确认旧污染词不再出现。
6. 只提交应该进仓库的代码/文档，不把用户个人 memory 混进 commit。
7. 向用户报告改了什么、验证了什么、哪些东西有意没碰。
