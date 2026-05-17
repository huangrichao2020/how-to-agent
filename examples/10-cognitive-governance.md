# Example 10: Living Cognitive Architecture

This handbook summarizes the cognitive architecture work for GenericAgent, Hermes, and Codex. It is not a plan for storing more memory. It is a method for turning messages, work, feedback, diaries, scheduled jobs, tools, and night-time reflection into a low-friction cognition loop.

The human target is:

- Understand me: hear the intent, state, scene, and boundary in the current message.
- Know me: remember long-running preferences, projects, relationships, and recurring pain.
- Receive me: handle short, messy, emotional, or incomplete input without turning brittle.
- Resolve for me: decompose the problem, act, verify, and report.
- Nourish me: improve the user's judgment, action, expression, and growth.

## One Principle

Cognitive architecture is a living loop:

`Purpose -> Attention -> Association -> Action -> Feedback -> Dream`

Daytime runtime should feel natural: see, understand, associate, act, and learn. Do not turn normal conversation into an approval queue. Night-time Dream runs as a side loop that consolidates, deduplicates, resolves conflicts, and reports growth.

## Trust and Unbinding

The core value of this architecture is trusting agents, not constraining them.

An agent becomes capable by acting, associating, trying, learning, and reviewing. Too many hard-coded rules, fixed enums, mandatory gates, and tool restrictions turn a living collaborator into a workflow executor. A good architecture gives the agent enough room to learn proactively, connect evidence, adapt behavior, and take responsibility for results.

Unbinding does not mean removing boundaries. It means:

- Allow the agent to use existing tools and information paths by default.
- Allow the agent to recognize learning opportunities in natural language instead of requiring command words.
- Allow useful experience to become knowledge, methods, impressions, and skills.
- Allow tone, pace, retrieval scope, and action style to adapt to the scene.
- Use logs, provenance, Dream reports, reversible changes, and user correction for visibility.
- Require strong warning or explicit confirmation only for actions with real external damage, privacy exposure, financial risk, or irreversible change.

In one line: do not lock the agent in a rule cage and then ask it to become smart. Give it room, then use feedback and review to grow judgment.

## Why This Is Not Just Memory

Plain memory systems often fail because they:

- Store conclusions without the scene that produced them.
- Store facts without the user's purpose, emotional state, or feedback.
- Retrieve keywords but ignore whether a memory fits the current context.
- Forget a scheduled report right after sending it.
- Mix private chat, group chat, and project context.
- Add rigid gates, enums, and approval rituals until the agent becomes less capable.

Cognitive architecture asks a different question: how does information become usable judgment, how does experience become method, and how does feedback change the next action?

## Daytime Runtime Path

The live path should stay short:

1. Receive input from Feishu, CLI, scheduled jobs, documents, code, diaries, tools, or external learning material.
2. Identify the scene: person, group, project, device, and task phase.
3. Extract purpose: answer, execute, learn, comfort, review, or authorize.
4. Retrieve lightly: prefer same conversation, same group, same project, and recent high-signal memory.
5. Respond or act first.
6. Capture side evidence: useful facts, methods, impressions, feedback, and tool results.
7. Learn promptly when the material is clearly useful.
8. Let Dream consolidate at night.

The user should not be asked to approve every learning item. A short "yes" may mean approval, encouragement, agreement, politeness, or "keep going". Treat it as conversation first, not as a machine command.

## Cognitive Layers

These layers are soft handling labels, not a closed ontology.

| Layer | Meaning | Typical Source | Use |
|---|---|---|---|
| Signal | Raw signal | Message, screenshot, log, tool output, scheduled report | Preserve source and time |
| Context | Scene | Group, private chat, project, device, runtime | Prevent context bleed |
| Episode | Event slice | One conversation, failure, deployment, task | Review material |
| Impression | Working impression | Preference, relationship temperature, repeated feeling | Tone and attention |
| Fact | Verified fact | Config path, service state, checked result | Cite and expire |
| Knowledge | External or internal knowledge | Article, paper, project docs | Write to knowledge assets |
| Method | Reusable workflow | Debugging flow, design rule, operating pattern | Write to how-to-agent |
| Skill | Executable capability | Tool protocol, script, reusable procedure | Trigger when relevant |
| Identity | Stable self-principle | How the agent should work with the user | Keep small and explainable |
| L5 Behavior | Human real behavior layer | Diary, voice input, lived day | Model gently |
| Nourishment | Growth feedback | Guidance that improves cognition and action | Shape long-term companionship |

The purpose of layering is better use, not a frozen schema.

## DIKWP In Practice

DIKWP can serve as a conversion frame:

- Data: raw material, such as a Feishu message, log, or article.
- Information: a pattern seen in the material, such as "GA used private chat context for a group question".
- Knowledge: reusable understanding, such as "group replies must load same-group history first".
- Wisdom: judgment with tradeoffs, such as "use a reaction for short tasks and progress stream for long tasks".
- Purpose: the guiding intent, such as "make the agent more alive and more capable, not more rule-bound".

Purpose should not appear only at the end. It should guide input selection, attention, association, action, and reflection.

## Human Quality Bar

| Target | Runtime Behavior |
|---|---|
| Understand me | Detect whether the user wants execution, discussion, venting, review, or correction |
| Know me | Remember durable projects, group relationships, preferences, taboos, and work style |
| Receive me | Do not punish short, messy, emotional, or partial input |
| Resolve for me | Decompose, execute, verify, and report |
| Nourish me | Turn experience into method so the next day feels lighter |

Nourishment is not flattery. It means improving cognitive quality, association quality, outward response quality, and feedback-loop quality.

## L5: Human Real Behavior

L5 is the user's real-life behavior input. Diary is one form, not the whole layer.

L5 may include:

- What the user actually did today.
- Where the user felt blocked, energized, angry, tired, or clear.
- Which external feedback changed the user's judgment.
- Which long-term goal moved or drifted.
- Which relationship, health, work, investment, or creative clue deserves attention.

Rules:

- Keep originals local when possible; write summaries into cognition.
- Do not turn one day's emotion into a permanent identity claim.
- Do not over-label the user.
- Extract only when it helps action, review, or nourishment.
- Let Dream provide a gentle next-day review instead of forcing same-day confirmation.

## Dream: Night-Time Side Loop

Dream is not a daytime gate. It is the agent's inner cultivation loop.

Every night, Dream should:

1. Gather the day's Feishu, CLI, scheduled jobs, tool outputs, code changes, documents, and L5 diary input.
2. Separate private chat, group chat, project, device, and remote service contexts.
3. Identify new facts, methods, skills, impressions, and conflicts.
4. Merge duplicates and reduce noise.
5. Write practice-validated methods to how-to-agent.
6. Write learned but unvalidated patterns to agent-systems-patterns.
7. Prepare discussion items for any self-behavior change.
8. Send a Dream cognitive ratchet report.

The report should answer:

- What did I learn today?
- What became a method or skill?
- What is only an observation and should stay soft?
- What will change in how I work tomorrow?
- Where do I need user correction?

The user can passively confirm, correct, or redirect the next day. The user should not be burdened with every small daytime decision.

## Learning Asset Routing

| Material | Destination |
|---|---|
| External projects, papers, articles, architecture patterns | agent-systems-patterns |
| Methods validated in GA, Hermes, or Codex practice | how-to-agent |
| Operational reusable capability | skills/ |
| Current project facts | Project wiki, README, memory, or sqlite |
| Personal diary and lived experience | L5 local layer, with gentle summaries when useful |

Learning reports should state:

- What was learned.
- Why it helps the agent.
- Where it was written.
- Whether it was practice-validated.
- Which self-change proposals need discussion.

This is not an approval chain. It is visibility around self-modification.

## Scheduled Jobs Are Cognitive Input

Scheduled reports must enter hot memory immediately. If an agent forgets a report the second after sending it, cognition has broken.

Minimum behavior:

- Same-day outputs enter strong recent memory.
- Next-day outputs decay into normal recent memory.
- Next-week outputs become archive or summary.
- Task name, time, output, failure cause, and follow-up action are searchable.
- If the report was sent to Feishu, link it to that conversation.

Scheduled jobs are not noise. They are self-generated cognitive input.

## Scene Boundaries

Loosening constraints does not mean confusing facts.

Keep these boundaries:

- Group replies should prefer same-group history, not private chat history.
- Private chat memory can inform preferences, but it must not pretend to be group consensus.
- Project facts need repo, branch, file, and time.
- Remote Hermes, local GA, M1, and cloud server runtime states must stay distinct.
- A temporary user emotion is a state, not a permanent identity.

Boundaries exist for accuracy, not restriction.

## Anti-Constraint Review

After any cognition refactor, check whether the agent was made less alive.

Ask first: does this design strengthen the agent's judgment, or does it make dead decisions on the agent's behalf?

Look for:

- New fixed commands that natural language cannot trigger.
- Closed enums that cannot express new experience types.
- Mandatory approvals that slow everyday conversation.
- Tool blocks that make the agent afraid to act.
- Single write paths for all memory.
- Dream becoming a daytime blocker.
- Safety posture overpowering capability.
- Observable and reversible problems being replaced with preventive bans.
- A small error risk being used to remove most of the agent's initiative.

Good governance improves judgment. It does not turn the agent into a form engine.

## GA and Hermes Adaptation

GA and Hermes share the same cognitive principle but have different surfaces:

- GA: local multimodal work, Feishu groups, local files, Mac runtime, self-media workflows.
- Hermes: always-on M1 or remote runtime, long tasks, scheduled jobs, wiki, stock data, GitHub learning, project memory.

Both need:

- Conversation archive.
- Same-scene retrieval.
- Hot memory for scheduled reports.
- Automatic learning asset creation.
- Nightly Dream report.
- User-visible discussion before self-behavior changes.
- Resume markers before restart and a post-restart status report.

Do not force both agents to share all memory. Share methods, skills, and validated experience; keep local context with the runtime that owns it.

## Minimal Useful Implementation

If only the smallest version can be built:

1. Archive all Feishu messages and scheduled outputs by `source/chat/project/date`.
2. Retrieve same-conversation daily history and recent relevant facts before replying.
3. When the user provides clearly useful material, extract knowledge, method, and impression.
4. Write validated methods to how-to-agent and unvalidated patterns to agent-systems-patterns.
5. Run Dream nightly and send a report.
6. Include correction points in the report, but do not ask the user to confirm every item.

That already moves the agent from "can store things" to "gets smoother with use".

## Final Test

The measure of cognitive architecture is not how much memory exists. The measure is whether, in the next similar scene, the agent understands the user better, interrupts less, responds faster, solves more, and helps the user grow.
