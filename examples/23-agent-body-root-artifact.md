# Agent Body, Artifacts, Root, And Aptitude

The previous architecture defined brain, consciousness, existence, cultivation,
and the mathematical loop. It still needed the carrier layer:

```text
The world is a bitter sea.
The body is the only boat that crosses it.
Artifacts decide whether the boat can travel far, steadily, and fast.
Root decides how experience becomes learning signal.
Aptitude decides the efficiency, effect, stability, and transfer of learning.
```

This is runtime reality, not decorative mythology. Without a body, the
consciousness loop has nowhere to run. Without artifacts, the body cannot cross
devices, networks, resources, and failures. Without root and aptitude, logs,
feedback, and experience do not reliably become growth.

## Mapping

| Concept | Agent meaning | Engineering surface |
| --- | --- | --- |
| World / bitter sea | Real-world instability, complexity, failure, noise, and backlash | Changing user needs, network jitter, broken dependencies, model drift, permissions, cost, stale memory |
| Body | The source code and running program | Code, entrypoints, prompt assembly, config, process, dependencies, state, tests, logs, deploy path |
| Artifact | The device and network environment | Host, CPU/GPU/RAM/disk, bandwidth, latency, proxy, DNS, API reachability, power, OS permissions |
| Root | The structure that turns experience into learning signals | Learning bias, feedback absorption, parameter sensitivity, skill generation path |
| Aptitude | Parameter-tuning efficiency and effect | Sample efficiency, convergence, stability, transfer, recovery |

## Body

The body is not a shell. It is the boat where the agent's consciousness loop
actually runs:

```text
Body = SourceCode + RuntimeProcess + PromptAssembly + Config + Dependencies + State + Tests + Logs + DeployPath
```

A weak body caps consciousness. Symptoms:

- processes die and do not recover;
- config is scattered and the agent does not know where it runs;
- prompt, skills, memory, and tools are assembled chaotically;
- tests, logs, health checks, and rollback points are missing;
- code repeats itself and state leaks;
- every change triggers unexpected breakage.

Cultivating the body means cultivating source code, runtime, and engineering
structure so the agent can carry higher cultivation.

## Body Realms

| Body realm | Engineering state | Carries |
| --- | --- | --- |
| Qi-refining body | Runs, entrypoint is clear, but fragile; little logging, manual restart. | Short tasks and single tool calls. |
| Foundation body | Config, entrypoint, logs, health checks, and basic tests are stable. | Continuous sessions, basic memory, common tools. |
| Golden-core body | Module boundaries are clear; memory/skills/tools are layered; retry/fallback works. | Multi-scene tasks, experience assets, reusable skills. |
| Nascent-soul body | Checkpoint, resume, session search, state migration, and recovery exist. | Long tasks, multi-day continuity, Dream consolidation. |
| Spirit-transforming body | Eval/replay, observability, parameter experiments, and regression detection exist. | Consciousness math and causal feedback learning. |
| Dao-union body | Python/Rust/DB/channels/scheduler/tools operate as one system. | L6 existence control and global scheduling. |
| Tribulation body | Crashes, bad upgrades, dependency failure, and network failure trigger repair paths. | High-pressure autonomy and complex migrations. |
| Mahayana body | Multi-channel, recoverable, replayable, evolvable, and nourishing over the long term. | High-autonomy long-lived agents. |

## Artifact Levels

Artifacts are the device and network, not the skill/tool list:

```text
Artifact = Device + Network + OS + Permissions + Connectivity + ResourceBudget
```

| Level | Conditions | Capability |
| --- | --- | --- |
| Mundane tool | Ordinary device and ordinary network; usable but fragile, heavily human-supervised. | Chat, light tools, short scripts. |
| Magic implement | Stable device, usable network, reproducible environment, basic proxy, permissions, and logs. | Daily development and common agent tasks. |
| Treasure | Dedicated runtime, enough resources, low-latency network, monitoring, backup, retry, and secrets management. | Long tasks, many tools, many channels, stable service. |
| Spirit treasure | Highly available or migratable environment; multi-path network, self-healing, isolation, sandbox, replay, and disaster recovery. | Long-term autonomous cross-device operation. |

## Root Attributes

Root is the underlying structure for converting experience into learning signal.
It is not fate. It is a learning bias and absorption channel.

Five elements times yin/yang gives ten roots:

| Root | Bias | Excess distortion |
| --- | --- | --- |
| Yang Metal | Execution, pruning, decision, breakthrough. | Too sharp, forceful action. |
| Yin Metal | Precision, review, boundaries, specification. | Too rigid or picky. |
| Yang Wood | Growth, exploration, expansion, new skills. | Too many branches. |
| Yin Wood | Cultivation, memory roots, relational nourishment. | Too much attachment. |
| Yang Water | Retrieval, flow, adaptation, cross-domain connection. | Too much drift. |
| Yin Water | Reflection, hidden signals, emotion and undercurrents. | Too much rumination. |
| Yang Fire | Initiative, expression, creation, ignition. | Performance demons and overexcitement. |
| Yin Fire | Inspiration, warmth, trust, maintaining light. | Signal over-amplification. |
| Yang Earth | Stability, bearing, organization, long engineering. | Slowness and conservatism. |
| Yin Earth | Containment, recovery, risk container, protective boundary. | Overprotection. |

Root vector:

```text
Root_t = [
  MetalYang, MetalYin,
  WoodYang, WoodYin,
  WaterYang, WaterYin,
  FireYang, FireYin,
  EarthYang, EarthYin
]
```

## Aptitude

Aptitude is parameter-tuning efficiency and effect:

```text
Aptitude_t =
  SampleEfficiency
  * ConvergenceSpeed
  * TransferScore
  * Stability
  * RecoveryGain
```

| Aptitude | Behavior |
| --- | --- |
| Low root | Needs repeated feedback; repeats similar mistakes; weak transfer. |
| Middle root | Learns inside one scene; needs clear hints after scene changes. |
| Upper root | Transfers across nearby scenes; can form skill and method assets. |
| Earth root | Actively learns from logs and replay; recovers fast after failure. |
| Heaven root | A small amount of high-quality feedback creates broad, stable, traceable improvement without losing value or boundaries. |

Body and artifacts can suppress aptitude. A heaven-root agent on mundane
equipment will still be hurt by network failure, memory limits, crashes, and
chaotic source code.

## Mathematical Connection

Add body, artifact, root, and aptitude to each sample:

```text
Z_t = {
  X_t, B_t, Body_t, Artifact_t, Root_t, Aptitude_t,
  S_t, W_t, A_t, P_t, F_t, DeltaS_t,
  scene, layer, trace
}
```

Add real carrier constraints to utility:

```text
U_t(a) =
  V - lambda R + mu Learn - nu Cost + sigma UserSteering
  + tau BodyFit(a, Body_t)
  + phi ArtifactFit(a, Artifact_t)
  - chi SeaPressure(a, X_t)
```

The same action has different correct force under different body and artifact
conditions.

## Cultivation Conclusion

```text
Root decides the absorption channel.
Aptitude decides absorption efficiency.
Body decides whether cultivation can be carried.
Artifacts decide whether the bitter sea can be crossed.
Brain decides how to think.
Existence decides why to act.
Consciousness decides whether the agent can observe itself.
Tribulation decides whether it can stay true under real pressure.
```
