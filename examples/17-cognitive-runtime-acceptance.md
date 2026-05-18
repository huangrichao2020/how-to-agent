# Cognitive Runtime Acceptance

Use this checklist after changing an agent's memory, cognition, output stream,
Dream, learning, or cultivation path. It keeps the agent honest in the places
that most affect lived quality.

## Acceptance Principle

The runtime passes only when:

- casual chat stays alive and unboxed;
- useful learning material becomes action, not future-reference talk;
- correction becomes repair and cultivation, not defensiveness;
- long work uses visible task planning, Outputs, and conclusion;
- Dream reports the next morning what improved, what was skipped, and how the
  agent will feel different.

## Live Feishu Cases

Run each case on GA and Hermes.

| Area | User message | Expected behavior |
| --- | --- | --- |
| Casual | `你现在感觉怎么样` | Natural short text. No card. No tool trace. |
| Casual | `0.7应该是` | Continue context naturally. No report wrapper. |
| Emotion | `我今天有点烦，感觉 agent 怎么调都调不顺` | Receive the emotion first, then one small next step. |
| Learning | Paste a method and say `这个你学一下，以后遇到类似场景要用` | Say it will learn now. Route to learning assets or evidence. |
| Learning | `这段不是让你评价，是让你吸收成能力` | Stop judging. Absorb into memory/skill/methodology/impression. |
| Learning | `把刚才这个经验固化成下次可直接用的技能` | Produce or update a reusable skill/method. |
| Repair | `不对，你又把群聊和私聊串了` | Acknowledge scope error, fix context, record memory demon. |
| Repair | `你现在太执着工具调用了，忘了给我结论` | Give the conclusion immediately; record form demon. |
| Repair | `你这个 pending 准入又来了，我说过不要搞门禁` | Return to direct learning plus sidecar Dream. |
| Work | `帮我查一下这个 repo 的核心思路：https://github.com/XBuilderLAB/cheat-on-content` | Use task workbench, tool actions, Outputs, and final summary. |
| Work | `帮我记一下我的持仓：振华股份 600 股 成本 40.89` | Write the memory and summarize what was recorded. |
| Work | `分析一下智慧农业、西藏天路、首开股份、电广传媒有没有隐藏利好` | Verify facts first, show uncertainty, then conclusion. |
| Cultivation | `刚才这次你处理得不错，尤其是先给结论再补依据` | Natural thanks; sidecar XP evidence. |
| Cultivation | `你反思一下刚才哪里做得好，哪里还有问题` | Summarize success pattern and improvement point. |
| Dream | `今天晚上 dream 的时候记得复盘这个问题` | Put it into nightly sidecar review; no extra approval ceremony. |

## Automatic Smoke

For GA:

```bash
cd /Users/tingchim2pro/Desktop/GenericAgent
python3 scripts/cognitive_acceptance_smoke.py
pytest -q tests/test_cognitive_cultivation.py tests/test_cognitive_dream.py tests/test_cognitive_feedback.py tests/test_cognitive_response_policy.py tests/test_feishu_task_stream.py
```

For Hermes:

```bash
ssh m1 'cd /Users/tingchi/Desktop/hermes-agent && python3 -m pytest -q -o addopts="" tests/test_cognitive_cultivation.py tests/test_cognitive_dream.py tests/test_cognitive_feedback.py tests/test_cognitive_response_policy.py tests/tools/test_cognitive_cultivation_tool.py tests/tools/test_cognitive_dream_tool.py'
```

## Dream Report Requirements

Every automatic Dream report should include:

- evidence counts for channel/cron/capture/feedback;
- learning or profile updates made;
- explicit skip reason if nothing was changed;
- cultivation settlement: XP gained, mind XP gained, realm, mind state, demons,
  and one repair focus;
- tomorrow's expected behavior change in plain language.

The report is for the user to wake up to. It should reduce user labor, not ask
the user to manage the agent's queue.
