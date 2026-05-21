# Ω-Brain Data Schema

Ω-Brain depends on Λ-Base: logs become data, data becomes feedback, feedback
updates the self model.

## Canonical Sample

```json
{
  "sample_id": "string",
  "time": "ISO-8601",
  "scene": "chat|code|service|dream|learning|risk|writing|other",
  "layer": "L0|L1|L2|L3|L4|L5|L6",
  "X_t": {
    "input": "string",
    "context": {},
    "source": {}
  },
  "B_t": {
    "perception": {},
    "attention": {},
    "memory": {},
    "world_model": {},
    "self_model": {},
    "value": {},
    "risk": {},
    "decision_policy": {}
  },
  "G_t": {
    "attention_targets": [],
    "context_sources": [],
    "prompt_slots": [],
    "active_skills": [],
    "active_layers": [],
    "insertion_points": [],
    "correction_rules": [],
    "feedback_signals": []
  },
  "T_t": {
    "essence": {},
    "strategy": {},
    "tactics": {},
    "learning": {},
    "analysis": {},
    "action": {}
  },
  "A_t": {
    "type": "reply|ask|search|tool|edit|delegate|wait|stop",
    "content": {},
    "expected_outcome": {}
  },
  "F_t": {
    "tests": [],
    "logs": [],
    "user_reaction": {},
    "service_state": {},
    "external_result": {}
  },
  "loss": {
    "prediction_error": 0,
    "task_failure": 0,
    "risk_cost": 0,
    "user_negative_feedback": 0,
    "traceability_cost": 0
  },
  "delta_self": {},
  "trace": []
}
```

## Admission Rule

Raw logs may always be stored. Training samples require:

- traceable source;
- typed scene;
- layer label;
- comparable outcome;
- later correction path.
- attention-governance trace: what context entered, where correction happened,
  and what feedback should affect the next PromptComposer.

Weak constraints do not mean weak data. Bold action needs stronger trace.
