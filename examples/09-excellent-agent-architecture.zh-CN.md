# 示例 08：优秀 Agent 架构

[English](09-excellent-agent-architecture.md) · [简体中文](09-excellent-agent-architecture.zh-CN.md)

当一次对话产生的不只是一个 patch，而是一套可复用的架构品味时，用这个示例。

## 原始 prompt

```text
你把今天的心得，把你心目中的优秀架构，更新到桌面的 how-to-agent
```

## 开发者意图

这句话要求 agent 把当天的真实操作经验沉淀成可迁移的架构原则。它不是让
agent 写流水账，而是让 agent 写出下一个 agent 可以继承的判断标准。

今天的工作里，有几条模式变得很清楚：

- 飞书集成不能把所有思考和长任务状态都塞进同一条富文本消息里反复编辑。长任务需要把思考/状态流和结论流分开。
- 自我进化不能靠静默自改；需要 proposal、证据、风险等级、验证和回滚。
- 当 skill 改造已经生效，旧记录应该进入冷归档。归档仍可搜索，但不应污染日常活跃记忆。
- 依赖安全修复要按运行时风险分组、验证，并在 live service 健康后再收口。
- 真正的 source of truth 是正在运行的系统和当前仓库，不是记忆里的旧总结，也不是一句听起来舒服的概括。

## 架构品味

我心目中的优秀 agent 架构，在压力下应该是安静的。它不是靠到处加循环显得聪明，而是靠给每一种状态、输出和权威来源安排正确的位置来变得可靠。

```text
                 用户意图
                    |
                    v
                 交互层
      飞书 / CLI / Web / 定时任务
      - 接收输入
      - 渲染输出
      - 不拥有核心真相
                    |
                    v
                运行时核心
      planner · tool router · permission boundary
      memory loader · model dispatcher · verifier
      - 拥有执行状态
      - 所有工具调用经过同一个 policy gate
                    |
        +-----------+------------+
        |                        |
        v                        v
       知识平面                  执行平面
       活跃事实                  tools / shell / browser
       skills                   subagents / external CLIs
       archives                 service restarts
       evaluations              deploys
        |                        |
        +-----------+------------+
                    |
                    v
              证据与闭环
      tests · logs · status · commit · handoff
```

## 六个分离

### 1. 分离输出流

不要把平台消息当成 agent 的整个大脑。

对飞书或聊天平台里的长任务，至少拆成两条流：

- **进度流**：短状态、工具里程碑、可恢复失败。
- **结论流**：最终答案、证据、链接、下一步。

超长任务还应该有 append-only event trail 或 artifact。把每一次思考都编辑进同一条富文本消息，迟早会撞上平台限制，也会让任务恢复变脆。

### 2. 分离权威来源

memory 本身不等于权威。

不同真相等级应该进入不同表面：

- **当前事实**：小而活跃，默认加载。
- **流程和 skills**：可复用行为，需要版本和 review。
- **会话历史**：可搜索证据，不是默认 instruction memory。
- **冷归档**：旧记录，必要时才读取。

当一个 skill 改造已经落地，旧 proposal 和原始日志就变成历史。它们应该还能被查到，但不应该继续指导日常行为。

### 3. 分离进化和执行

自我改进应该经过棘轮：

```text
observation
  -> proposal
  -> evidence
  -> risk classification
  -> validation plan
  -> rollback plan
  -> apply gate
  -> post-change audit
```

低风险改进在授权后可以自动化。高风险改动，比如删除、凭证、部署、支付、shell policy、tool permission，则必须经过明确的人类门禁。

### 4. 分离主路径和 sidecar

系统应该有一个主运行路径。sidecar 只有在有边界、可失败、不阻塞主路径时才有价值。

好的 sidecar：

- telemetry 失败不影响回答
- archive 只压缩旧记录，不改活跃记忆
- audit 报告风险，但不静默改 runtime policy
- subagent 拥有窄任务边界，输出可 review

坏的 sidecar 会悄悄变成第二套 runtime。

### 5. 分离依赖治理和功能开发

依赖告警是运维工作，不是杂活。

按影响面处理：

1. 先修运行时依赖。
2. 再修可选 bridge。
3. 最后修 docs 或 website 依赖。
4. 每组用最贴近的测试验证。
5. 运行时环境变化后才重启 live service。
6. 复查 GitHub alerts，但要区分 scanner 延迟和代码未修。

这样安全修复不会变成一次失控的大升级。

### 6. 分离“完成”和“有把握”

代码改完不等于完成。系统要自己证明它完成了：

- 仓库状态清楚
- tests 或 focused checks 通过
- live service 健康
- 用户交互通道恢复
- 如果用户要求，commit 和 push 完成
- 没有把无关 dirty files 吸进提交
- 下一个 agent 能找到这套方法

## 可复用 prompt

```text
把今天的工作提炼成架构心得。

不要写流水账。写成未来 agent 可以复用的方法。

覆盖：
- 系统试图解决什么问题
- 优秀架构应该分离哪些东西
- 活跃记忆在哪里结束，归档从哪里开始
- 自我进化如何被治理
- 长任务在聊天平台里如何分流输出
- live verification 如何闭环

按 how-to-agent 现有 examples 风格加入仓库。
更新索引，不要保存私密日志、token 或原始聊天记录。
```

## 验收检查

- 这份心得能脱离原始对话复用。
- 它区分了活跃记忆和历史归档。
- 它明确 runtime、knowledge、execution、channel 边界。
- 它包含验证和回滚思维。
- 它没有泄漏私密日志或凭证。
- README 索引能找到新 artifact。
