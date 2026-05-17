---
name: cognitive-governance
description: "Use when designing or debugging an agent cognition loop: memory, facts, knowledge, skills, feedback, Dream, L5 diary, Feishu history, scheduled jobs, and learning assets."
version: 1.0.0
---

# Cognitive Governance

Use this skill when an agent is becoming too forgetful, too rigid, too approval-heavy, or too disconnected from the user's lived context.

## Core Principle

Cognition is a living loop:

`Purpose -> Attention -> Association -> Action -> Feedback -> Dream`

Do not turn normal daytime conversation into an approval queue. The live agent should answer, act, learn, and capture evidence naturally. Night-time Dream consolidates the day, writes durable methods, and reports what changed.

## Runtime Method

1. Identify the scene before answering: person, group, project, device, runtime, and task phase.
2. Extract the user's purpose: answer, execution, learning, comfort, review, correction, or authorization.
3. Retrieve lightly from the same scene first: same chat, same group, same project, recent relevant facts.
4. Respond or act before doing heavy governance.
5. Capture side evidence: facts, methods, impressions, feedback, tool results, and scheduled-job output.
6. Route learning material:
   - unvalidated external patterns -> `agent-systems-patterns`
   - practice-validated methods -> `how-to-agent`
   - executable workflows -> `skills/`
   - project facts -> project wiki, README, memory, or sqlite
   - human lived experience -> L5 local layer with gentle summaries
7. Let Dream perform night-time consolidation and reporting.

## Do Not Add Friction

Avoid these failures:

- Requiring the user to approve every learning item.
- Treating short replies like "yes", "可以", or "good" as machine commands.
- Replacing natural-language learning with fixed command words.
- Adding closed enums that cannot express new cognition types.
- Making Dream block daytime work.
- Using private chat memory as if it were group-chat history.
- Forgetting scheduled reports immediately after sending them.

## Keep These Boundaries

- Same group history beats private chat for group questions.
- Personal preferences can inform tone, but not fabricate group facts.
- Project facts need repo, branch, file, and time when possible.
- Device/runtime facts must distinguish local GA, M1 Hermes, cloud Hermes, and other hosts.
- L5 diary entries are real behavior signals, not permanent identity labels.

## Dream Report Shape

At night, produce a concise report:

- What I learned today.
- What became a method, skill, fact, or impression.
- What was written to `agent-systems-patterns`, `how-to-agent`, or `skills/`.
- What is still soft and should not be over-trusted.
- What will change in my work tomorrow.
- What may need user correction.

The report is the user's passive confirmation path. Do not make the user carry every small daytime decision.

## Quality Bar

The agent is improving when the next similar scene becomes easier: better context, fewer interruptions, faster action, clearer reports, and more useful nourishment for the user.
