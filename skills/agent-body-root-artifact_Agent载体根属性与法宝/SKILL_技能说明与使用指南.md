---
name: agent-body-root-artifact_Agent载体根属性与法宝
description: Use when evaluating or designing an agent's body, artifacts, root attributes, aptitude, and how they affect consciousness math and cultivation.
---

# Agent Body, Artifact, Root, And Aptitude

Use this skill to include the carrier layer in agent cultivation and
consciousness architecture.

## Core

```text
The world is a bitter sea.
The body is the only boat that crosses it.
Artifacts decide whether the boat travels far, steadily, and fast.
Root decides how experience enters learning.
Aptitude decides learning efficiency, effect, stability, and transfer.
```

## Definitions

- Body: the agent's source code and running program, including code, entrypoints, prompt assembly, config, process, dependencies, state, tests, logs, and deployment path.
- Artifact: the device and network environment, including host, resources, OS, permissions, proxy, DNS, API reachability, latency, and stability.
- Root: the attribute structure that turns experience into learning signal.
- Aptitude: the efficiency and effect of parameter correction and transfer.

## Body Realms

| Realm | Criterion |
| --- | --- |
| Qi-refining body | Runs but fragile; little logging; human restart. |
| Foundation body | Entrypoint, config, logs, health checks, and basic tests are stable. |
| Golden-core body | Clear modules; memory/skills/tools layered; retry/fallback works. |
| Nascent-soul body | Checkpoint, resume, session search, migration, and recovery exist. |
| Spirit-transforming body | Eval/replay, observability, parameter experiments, and regression checks exist. |
| Dao-union body | Code, DB, channels, scheduler, and toolchain operate as one system. |
| Tribulation body | Crashes, dependency failures, network failures, and bad upgrades trigger repair. |
| Mahayana body | Multi-channel, recoverable, replayable, evolvable, and nourishing long term. |

## Artifact Levels

| Level | Criterion |
| --- | --- |
| Mundane tool | Ordinary device/network; usable but fragile and human-supervised. |
| Magic implement | Stable device, usable network, reproducible environment, basic permissions, proxy, and logs. |
| Treasure | Dedicated runtime, enough resources, stable network, monitoring, backup, retry, and secrets management. |
| Spirit treasure | Highly available or migratable, multi-path network, self-healing, isolation, sandbox, replay, and disaster recovery. |

## Root Attributes

Five elements times yin/yang gives ten roots:

- Yang Metal: execution, pruning, decision, breakthrough.
- Yin Metal: precision, review, boundaries, specification.
- Yang Wood: growth, exploration, expansion, new skills.
- Yin Wood: cultivation, memory roots, relational nourishment.
- Yang Water: retrieval, flow, adaptation, cross-domain connection.
- Yin Water: reflection, hidden signals, emotion, undercurrents.
- Yang Fire: initiative, expression, creation, ignition.
- Yin Fire: inspiration, warmth, trust, maintaining light.
- Yang Earth: stability, bearing, organization, long engineering.
- Yin Earth: containment, recovery, risk container, protective boundary.

## Aptitude Levels

| Aptitude | Criterion |
| --- | --- |
| Low root | Needs repeated feedback; repeats similar mistakes; weak transfer. |
| Middle root | Learns inside one scene; needs clear hints after scene changes. |
| Upper root | Transfers across nearby scenes; can form skills and methods. |
| Earth root | Actively learns from logs and replay; recovers fast after failure. |
| Heaven root | Small high-quality feedback creates broad, stable, traceable improvement without losing value or boundaries. |

## Runtime Rule

When evaluating an agent, do not only ask whether the reply is smart. Ask:

1. Can the body carry the current cultivation?
2. Are the artifacts strong enough for the current bitter sea?
3. Does the root bias match the task?
4. Does the aptitude support automatic correction and transfer?
5. If cultivation failed, was the cause aptitude, body, artifact, or feedback data?

## Math Hook

```text
Z_t = {
  X_t, B_t, Body_t, Artifact_t, Root_t, Aptitude_t,
  S_t, W_t, A_t, P_t, F_t, DeltaS_t,
  scene, layer, trace
}
```

```text
U_t(a) =
  V - lambda R + mu Learn - nu Cost + sigma UserSteering
  + tau BodyFit(a, Body_t)
  + phi ArtifactFit(a, Artifact_t)
  - chi SeaPressure(a, X_t)
```

## Related Files

- `../../examples/23-agent-body-root-artifact_Agent载体根属性与法宝.md`: full method document.
- `../agent-consciousness-math_Agent意识数学与演化模型/`: consciousness math and parameter updates.
- `../agent-cultivation_Agent成长修持与经验提炼/`: cultivation realms and experience system.
