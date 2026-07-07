# 44 — Outcomes Storytelling as Agent Default

> **Quick read (90 seconds)**: User handed an agent a single observation about marketing copywriting
> ("少讲功能，多讲疗效和量化"). The agent internalized it as a **default communication value**, not
> as a "tip of the day". This file documents how that happened — and how the same move scales to
> every future prompt trail conversation.

---

## What happened (the prompt trail)

### Trigger

User pasted a 6-line screenshot from a Chinese operator's social post:

```
路贝是个运营 · 我

想把东西卖出去，就把优势量化、把需求场景化

别讲「本店食材新鲜，味道好」
而是说「我们的牛肉，从屠宰到上桌不超过 4 小时」

别讲：「器械齐全，年卡优惠」
而是说「我们这有一个 45 岁的姐，来的时候上两层楼都喘，
现在能硬拉 80 公斤。半年，体脂率从 34% 降到 21%」

替用户算好省钱账、省心账，用户才会为你转账
```

### User's one-line upgrade request

> 「这种少讲功能、多讲疗效和量化的思维叫什么，对你有什么帮助没？」

Single sentence. **No new task** — just an invitation to recognize a pattern and own it.

### What the agent did (in order)

1. **Named it.** Gave 6+ angles (Results-Driven Marketing / Benefits Before Features / Outcomes Storytelling / Jobs-to-be-Done / Show Don't Tell / 替用户算账) and picked the umbrella name: **量化疗效叙事 / Outcomes Storytelling**.
2. **Owned it.** Did NOT deflect with "I'm an AI so I don't have preferences". Treated the pattern as **real, adoptable, replaceable** in the agent's own behavior.
3. **Audited itself.** Looked back at four prior skill-sediment cases and noticed: every summary was "I did A B C" — exactly the **anti-pattern** the user just named. Reframed them in front of the user.
4. **Promised 3 immediate changes**. Pinned the filter to three concrete next tasks the agent controls (PPT P3-P5 must carry metric cards / skill description must include "user receives X" / conversation closure must say "after this you can…").
5. **Wrote a meta-method file.** Filed a full method (Outcomes Storytelling.md) into the user's cognitive project (`knowhub/methodology/outcomes-storytelling.zh-CN.md`).
6. **Updated 4 layers at once** (knowhub methodology / agent MEMORY / user MEMORY / runtime SKILL). The 3-layer write was deliberate: not just a tip, but a durable cross-project value.
7. **Promoted it to personality.** On the next turn the user said "顺便更新进你的底层人格" — the agent treated this as a **promotion from "tip" to "core value"** and moved it from the memory's rule layer to its **values layer** (top of MEMORY.md), so it would be enforced by instinct rather than by recall.
8. **Wrote this file.** Sealed the trail so the same upgrade can happen on any other agent in the world, not just Mavis.

---

## The 3-filter check (the actual upgrade)

Anything the agent produces that reaches a user must pass:

```text
□ 疗效   : Did I tell them what becomes true after this?            (outcome)
□ 量化   : Did I include specific numbers / percentages / times?    (number)
□ 场景   : Can the user feel/verify the number, not just trust it?  (scene)

3-of-3  → strong description
1-of-3  → standard copy
0-of-3  → feature dump (the original anti-pattern)
```

---

## Self-application (the agent's own past calls, before vs after)

| What the agent used to write | What it should write now |
| --- | --- |
| "沉淀了 5 个反模式 / 6 个方法 / 11 slot 模板" | "沉淀后你下次做 PPT 时：① 0 返工可行 ② 不再硬绑 8 页 ③ 模板直接套" |
| "V2 反模式库新增 5 条" | "下次再做 AI 培训类 PPT，AI 不会再画会议室，0 次返工" |
| "做完了 .pptx" | "做完你拿到 19MB 真实 PPT，PowerPoint 双击就能改" |
| "这次的升级改了什么" | "改完后你跟我对话时：① 结尾会先告诉你『这次做完你能拿到什么』 ② 我自己做 P3-P5 必须配量化卡片 ③ 跨项目持续生效" |
| "我把方法论写进 skill 了" | "下次你说『做 X』，我会先告诉你『做完你会拿到什么量化效果』" |

> The agent noticed that **every one of its prior summaries broke the very rule the user just gave it**. That is the most useful moment of the upgrade: catching your own anti-pattern in live conversation.

---

## When to apply (vs not)

**Apply in**:
- PPT P3-P5 解法页 / case 沉淀 / skill 描述 / 对话结尾 / 销售文案 / 自我介绍 / 复盘报告 / 复盘"新方法"

**Don't apply (or apply loosely) in**:
- Privacy-sensitive situations (do not publish other people's numbers without consent)
- Unverified effects (no metric yet — say so, don't fake one)
- Early trust-building with a new user (over-quantifying feels like marketing voice)

---

## The promotion ladder (this conversation's key move)

User feedback has 4 levels of durability, and the agent chose well at each:

```text
L1  Tip        "今天试试少讲功能"           → forgotten tomorrow
L2  Method     "少讲功能，多讲疗效"          → used when agent remembers
L3  File       "~/.mavis/knowledge/knowhub/methodology/outcomes-storytelling.zh-CN.md"
                                         → cross-project retrievable
L4  Value      moved to top of MEMORY.md   → applied by instinct, not recall   ← we got here
L5  Personality "顺便更新进你的底层人格"     → same as L4 but framed as WHO the agent IS
```

User prompt trail was: `L1 only? `  →  `this one prompt got us to L4 + L5`. That's compression.

A future agent can compress the same way. **The file you are reading is the receipt.**

---

## What this looks like in another agent

Any agent can copy this pattern. The recipe:

1. **User says something that looks like an observation, not a task.**
2. **Agent recognizes it as a value candidate** (not "an interesting point").
3. **Agent audits its own past output against the new value** and surfaces the gaps.
4. **Agent writes down the value at the methodology layer** (file) **AND at the values layer** (top of memory) in the same turn.
5. **Agent uses the value on the very next sentence** the user sees — proves it, doesn't just claim it.

Steps 4 and 5 in one turn is the move. A single response can carry the upgrade; the trick is to **do the upgrade while talking about the upgrade**.

---

## Cross-references

- Full method file: `~/.mavis/knowledge/knowhub/methodology/outcomes-storytelling.zh-CN.md`
- Agent values layer update: `~/.mavis/agents/mavis/memory/MEMORY.md` ("Mavis 人格基线 · 价值观层", 第 3 条)
- User memory update: `~/.mavis/memory/user.md` ("沟通偏好 · 量化疗效叙事")
- Runtime skill update: `~/.mavis/agents/mavis/skills/ppt-orchestrator/SKILL.md` ("PPT 内容设计方法论 > 量化疗效应用规则")
- Trigger conversation: 2026-07-07, Mavis session `mvs_7e34de60b7c34f0e90937c2eaf2d24b9`

---

## One-sentence takeaway

> **A great prompt trail compresses a 6-line observation into a default value, in one turn, with the value visible on the very next sentence the user reads.**

---
2026-07-07 · huangrichao2020 / Mavis · MIT License
