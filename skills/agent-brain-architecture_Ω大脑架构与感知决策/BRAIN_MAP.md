# Ω-Brain Map

| Region | Input | Output | Runtime responsibility |
| --- | --- | --- | --- |
| Perception cortex | user text, code, logs, files, tools | typed signals | Preserve source, time, scene, and raw evidence. |
| Thalamus/router | typed signals | main path + side evidence | Decide what must affect the current turn and what can be logged. |
| Attention governance | task + state + feedback | `G_t` | Compose prompt/context and correct runtime attention at loop nodes. |
| Attention system | task, signals, history | focus vector | Identify main contradiction and salience. |
| Working memory | focus, constraints, plan | turn state | Hold active evidence, plan, open questions, and success criteria. |
| Hippocampus | session/project history | timeline | Rebuild recent and episodic context. |
| Neocortex | docs, skills, repeated cases | abstractions | Provide methods, concepts, and reusable patterns. |
| Thinking core | focus + models + abstractions | `T_t` | Extract essence, strategy, tactics, learning, analysis, and action shape. |
| Prefrontal cortex | state + options | decision frame | Plan, prioritize, inhibit, and choose scope. |
| Basal ganglia | decision frame | action choice | Pick reply, ask, search, tool, edit, delegate, wait, or stop. |
| Limbic/value system | user state + L6 | value/risk weights | Maintain nourishment, relation, value, and risk signals. |
| Cerebellum | predicted + actual outcome | error signal | Compute correction and parameter deltas. |
| Motor cortex | action choice | external action | Execute tools, edits, calls, deployment, or messages. |
| Immune system | traces + anomalies | repair signal | Detect hallucination, context bleed, loops, stale facts, regressions. |
| Default mode network | day ledger + errors | consolidation | Dream, replay, self-narrative, durable learning. |

## Data Flow

```text
Raw signal
-> typed signal
-> attention governance G_t
-> working-memory state
-> thinking core T_t
-> candidate actions
-> chosen action
-> feedback
-> error signal
-> self-model delta
-> durable asset
```
