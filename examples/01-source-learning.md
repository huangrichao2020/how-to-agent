# Example 01: Source Learning

## Original prompt

```text
深度研究一下 open-design 的平面设计能力 和 agentic-stack 的 .agent/结构，看看对你有什么帮助
```

## Developer intent

The instruction asks for comparative learning, not implementation. The agent should inspect
how each project works, then translate the useful parts into patterns that fit the current agent.

## Reusable version

```text
Study [project A] and [project B].

For each project:
- read the structure, not only the README
- identify the core capability
- identify what is reusable for our agent
- identify what should not be copied

Return a short adaptation memo:
- useful patterns
- incompatible parts
- smallest safe experiment
- files or modules that would be affected
```

## Good output shape

```text
Pattern:
  [what the other project does well]

Why it matters here:
  [current weakness in our agent]

Adaptation:
  [smaller local version]

Do not copy:
  [heavy dependency, wrong abstraction, project-specific behavior]

First experiment:
  [one small change or one design document]
```
