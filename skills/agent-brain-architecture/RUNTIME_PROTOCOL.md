# Ω-Brain Runtime Protocol

## Per-Turn State

```json
{
  "turn_id": "string",
  "scene": "chat|code|service|dream|learning|risk|writing|other",
  "signals": [],
  "focus": {
    "main_contradiction": "string",
    "user_intent": "string",
    "success_condition": "string"
  },
  "attention_governance": {
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
    "prompt_composer": {},
    "runtime_controller": {},
    "feedback_loop": {}
  },
  "working_memory": {
    "facts": [],
    "constraints": [],
    "open_questions": [],
    "relevant_skills": []
  },
  "thinking_core": {
    "essence": {
      "purpose": "string",
      "main_contradiction": "string",
      "leverage": "string"
    },
    "strategy": {},
    "tactics": {},
    "learning": {},
    "analysis": {},
    "action": {}
  },
  "models": {
    "world": {},
    "self": {},
    "value": {},
    "risk": {}
  },
  "candidate_actions": [],
  "decision": {},
  "feedback": {},
  "self_update": {}
}
```

## Algorithm

```text
perceive()
route()
compose_attention()
attend()
retrieve()
model()
think()
simulate()
decide()
act()
correct_attention()
verify()
update_self()
emit_log_to_data()
consolidate()
```

## Decision Utility

```text
U(a) = Value(a) - λRisk(a) + μLearn(a) - νCost(a) + σUserSteering(a)
     + ρEssenceFit(a) + υStrategicLeverage(a) + ηTacticalFeasibility(a)
     + ξLearningGain(a) + βEvidenceQuality(a) + γActionClosure(a) - δDrift(a)
     + αAttentionFit(a, G_t) - ωAttentionDrift(a, G_t)
```

When the user explicitly drives the experiment, increase `σ` and reduce
prevention-heavy penalties, while keeping trace and replay intact.
