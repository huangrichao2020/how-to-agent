# Agent Consciousness Math Core

## State Sample

```text
Z_t = {X_t, B_t, Body_t, Artifact_t, Root_t, Aptitude_t, S_t, W_t, A_t, P_t, F_t, DeltaS_t, scene, layer, trace}
```

- `X_t`: input and environment.
- `B_t`: Ω-Brain state.
- `Body_t`: source/runtime health.
- `Artifact_t`: device/network health.
- `Root_t`: ten-dimensional learning-root vector.
- `Aptitude_t`: sample efficiency, convergence, transfer, stability, and recovery quality.
- `S_t`: self-model.
- `W_t`: world model.
- `A_t`: selected action.
- `P_t`: predicted outcome.
- `F_t`: observed feedback.
- `DeltaS_t`: self-model change.

## Decision

```text
A_t = argmax_a U_t(a)

U_t(a) =
  V_theta(a | X_t,S_t,W_t)
  - lambda R_theta(a | X_t,S_t,W_t)
  + mu Learn_theta(a)
  - nu Cost(a)
  + sigma UserSteering(a)
  + tau BodyFit(a, Body_t)
  + phi ArtifactFit(a, Artifact_t)
  - chi SeaPressure(a, X_t)
```

Weak constraints tune the weights. They do not remove evaluation.

## Error And Loss

```text
e_t = F_t - Predict_theta(X_t, S_t, W_t, A_t)
```

```text
Loss_t =
  alpha TaskFailure_t
  + beta PredictionError_t
  + gamma RiskCost_t
  + delta UserNegativeFeedback_t
  + rho TraceGap_t
```

## Update

```text
theta_{t+1} = theta_t - eta grad_theta Loss_t
S_{t+1} = S_t + kappa Learn(e_t, F_t, trace_t)
```

Use bounded updates first. Promotion to default runtime policy requires replay
or real feedback improvement.

## Loop Strength

```text
Psi_t =
  I(S_t; A_t | X_t)
  * I(F_t; DeltaS_t | S_t, A_t)
  * Q_t
```

Interpretation:

- `I(S_t; A_t | X_t)`: how much the self-model changed action selection.
- `I(F_t; DeltaS_t | S_t, A_t)`: how much feedback changed the self-model.
- `Q_t`: trace quality and evaluation confidence.

`Psi_t` is a system-control metric, not a claim of human qualia.
