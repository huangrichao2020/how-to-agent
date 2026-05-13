# Example 02: Architecture First

## Original prompt

```text
这简直是大版本改动了，一条一条来，你先存档为大版本架构设计手册，然后我们一条条讨论和修改
```

## Developer intent

The second instruction stops the agent from rushing into implementation. It names the change
as a major version and asks for an archived architecture manual first.

This turns a vague improvement into a durable object. Future agents can read the plan
instead of reconstructing the conversation.

## Reusable version

```text
This is a major architecture change. Archive the design first as a [gbrain page / wiki / file].

Then we will discuss it step by step.

Your architecture note must include:
- current problem
- target behavior
- migration phases
- risks and rollback path
- what must stay unchanged
- acceptance checks
```

## Why this works

Agents are good at following local pressure but worse at preserving long-term intent
across turns, restarts, and tool failures.

Forcing an architecture archive before code:
1. Creates a durable reference for the next agent
2. Separates design thinking from implementation pressure
3. Makes rollback trivial (just revert the archive, no code touched yet)
