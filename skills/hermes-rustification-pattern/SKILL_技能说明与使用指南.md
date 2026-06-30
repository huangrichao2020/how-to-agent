---
name: hermes-rustification-pattern
description: Methodology for gradually Rustifying the Hermes Agent runtime (hermesd) without breaking Python agent logic. Focuses on workspace restructuring, lifecycle migration, and shadow-mode tool execution.
---

# Hermes Rustification Pattern

Use this skill when evolving the Hermes Agent's Rust sidecar (`hermesd`) from a monolith into a structured, multi-crate workspace while maintaining backward compatibility with the Python agent brain.

## Core Principles

1. **Python stays the brain**: Do not rewrite `run_agent.py`, provider adapters, or gateway platform logic in Rust. Keep Python for fast iteration and API integration.
2. **Rust owns the substrate**: Move deterministic runtime primitives (lifecycle, process execution, event logging) into Rust crates.
3. **Shadow mode first**: Before switching primary execution to Rust, run it in parallel with Python and compare results.
4. **Workspace modularity**: Split `hermesd` into focused crates to improve build times and maintainability.

## Phase 8: Workspace Restructuring

### Target Layout
```
crates/
  hermes-common/      # Shared types (GatewayState, HealthReport, etc.)
  hermes-lifecycle/   # Gateway status, health checks, restart/stop logic
  hermes-events/      # JSONL event append, query, and session compaction
  hermes-tool-exec/   # Deterministic subprocess engine (process groups, timeouts)
  hermesd/            # CLI binary (thin dispatcher)
```

### Migration Steps
1. **Create skeleton crates**: Add `Cargo.toml` for each new crate.
2. **Extract shared types**: Move `GatewayState`, `HealthReport`, etc., to `hermes-common`.
3. **Migrate lifecycle logic**: Move `read_gateway_state`, `evaluate_health`, `restart`, and `stop` to `hermes-lifecycle`.
4. **Implement event compaction**: Add `hermesd compact` command to aggregate per-session summaries.
5. **Fix scope defaults**: Ensure `hermesd` defaults to `--system` if the gateway runs as a system service (common for root users).

## Phase 9: Tool Execution Shadow Mode

### Implementation
1. **Add `hermesd exec`**: A new CLI command that wraps `hermes-tool-exec::run_command`.
   - Features: Process group isolation (`libc::setpgid`), precise timeouts, SHA256 fingerprinting.
2. **Python Bridge**: Create `hermes_cli/tool_exec.py` to call `hermesd exec --json`.
3. **Integrate into `terminal_tool.py`**:
   - Add `_terminal_shadow_compare()` function.
   - Trigger it for local, foreground, non-pty commands when `HERMESD_SHADOW_MODE=1`.
   - Normalize output (strip trailing newlines) before comparing Python vs Rust results.

### Verification
Run `scripts/hermesd-exec-shadow-test.py` to verify 10+ standard commands produce identical exit codes and output in both backends.

## Common Pitfalls

- **Scope Mismatch**: `hermesd` defaulting to `--user` when the gateway is a `system` service causes "service unknown" errors. Always detect or default to the correct systemd scope.
- **Output Normalization**: Python's `subprocess` often strips trailing newlines while Rust captures raw stdout. Normalize both sides before comparison in shadow mode.
- **Monolithic main.rs**: Don't try to refactor all 3000+ lines at once. Extract one logical module (e.g., `restart`) at a time and verify compilation.
- **Fail-Soft Bridge**: The Python bridge to `hermesd` must never crash the agent. Wrap all subprocess calls in `try/except` and return `None` on failure so the caller can fall back to Python.

## Success Criteria

- `cargo check --workspace` passes for all 5 crates.
- `hermesd health --json` reports `"ok": true`.
- `hermesd compact` produces valid session summaries.
- Shadow mode shows < 1% mismatch rate in production traffic.
- Binary size remains under 1.5MB.