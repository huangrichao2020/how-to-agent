---
name: ga-implementation-map
description: 当需要把 how-to-agent 的架构原则映射到 GenericAgent 真实源码、测试、运行证据和缺口时使用。
---

# GA 架构实施映射

这个 skill 用来防止架构停留在口号层。

它把 `how-to-agent` 的原则落到 GA 的真实肉身：

```text
架构原则 -> 源码模块 -> 运行插手点 -> 测试/日志证据 -> 缺口 -> 下一步最小改动
```

## 工作流

1. 先确认最高参考来自 `/Users/tingchim2pro/Desktop/how-to-agent`。
2. 找到对应原则所属层级：天道、人道、存在道、注意力治理、反堆砌、skill 工程化、肉身/法器、万物择优。
3. 到 `/Users/tingchim2pro/Desktop/GenericAgent` 找真实源码落点。
4. 标出触发时机：任务开始、中途、工具后、结束、cron/dream 旁路、重启恢复。
5. 查测试、日志、报告、Feishu 命令或用户反馈证据。
6. 如果没有证据，只能记为缺口，不宣称完成。
7. 给出下一步最小源码改动，而不是再加一层抽象流程。
8. 需要快速盘点时，运行 `scripts/score_ga_architecture.py` 生成只读评分。

## 判断标准

- 有源码落点，才算进入肉身。
- 有测试或运行证据，才算初步落地。
- 有反馈反写，才算进入修炼。
- 有统计、回放和自动修正，才算接近成熟。

## 禁忌

- 不要把 `how-to-agent` 当作 GA 项目里的普通技能文档来整本塞给模型。
- 不要用 skill 替代源码改造。
- 不要把理论口径一致当成架构完成。
- 不要为了显得完整而新增无验证流程。

## 相关文件

- `../../examples/33-ga-implementation-map.zh-CN.md`：完整实施映射。
- `scripts/score_ga_architecture.py`：只读扫描 GA 源码、测试和运行证据的评分脚本。
- `../agent-final-architecture-outline/`：最终架构总纲。
- `../agent-attention-governance/`：注意力治理。
- `../agent-anti-bloat-context-engineering/`：反堆砌与上下文工程。
- `../agent-skill-creator/`：skill 工程化。
