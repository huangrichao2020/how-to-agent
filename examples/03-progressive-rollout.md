# Example 03: Progressive Rollout

[English](03-progressive-rollout.md) · [简体中文](03-progressive-rollout_渐进式架构演进.md)

Use this when the agent wants to switch on a new architecture immediately.

## Original prompts

```text
方案A 肯定是要做的，方案 1 直接做的话 有什么风险和收益？
```

```text
就是说渐进运行一段时间后，再全面切换生效会更好？
```

```text
那这期间是不是得停掉对记忆系统的改造了，聚焦这一件事
```

## Developer intent

These prompts separate three ideas:

- the direction is approved
- the rollout strategy is not yet approved
- adjacent risky work should pause during migration

## A reusable version

```text
I agree with the target direction.

Before implementing the direct switch, compare:
- direct full switch
- progressive rollout
- shadow mode / parallel run

For each option, list:
- benefit
- failure mode
- how we would know it is working
- rollback cost

If progressive rollout is safer, freeze adjacent subsystems during this period.
Only touch them if the migration requires it.
```

## Good agent behavior

The agent should recommend a staged path when:

- the change touches memory, tools, routing, startup, or persistence
- old and new behavior can run side by side
- failures would be hard for the user to diagnose
- rollback requires knowing which state was produced by which version
