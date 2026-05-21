#!/usr/bin/env python3
"""Score GenericAgent against the how-to-agent implementation map.

This script is intentionally lightweight and read-only. It checks whether the
main architecture concepts have source, test, and runtime-evidence landing
points in a local GenericAgent checkout.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass, asdict
from pathlib import Path


DEFAULT_GA_ROOT = Path("/Users/tingchim2pro/Desktop/GenericAgent")


@dataclass
class CheckResult:
    name: str
    layer: str
    status: str
    evidence: list[str]
    gaps: list[str]


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except Exception:
        return ""


def exists(root: Path, rel: str) -> bool:
    return (root / rel).exists()


def contains(root: Path, rel: str, needle: str) -> bool:
    return needle in read_text(root / rel)


def glob_any(root: Path, pattern: str) -> bool:
    return any(root.glob(pattern))


def result(name: str, layer: str, evidence: list[str], gaps: list[str]) -> CheckResult:
    if evidence and not gaps:
        status = "PASS"
    elif evidence:
        status = "PARTIAL"
    else:
        status = "MISSING"
    return CheckResult(name=name, layer=layer, status=status, evidence=evidence, gaps=gaps)


def score(root: Path) -> list[CheckResult]:
    checks: list[CheckResult] = []

    evidence, gaps = [], []
    if exists(root, "task_lifecycle.py"):
        evidence.append("task_lifecycle.py exists")
    else:
        gaps.append("task_lifecycle.py missing")
    for needle in ("tiandao", "rendao", "cunzaidao", "format_task_lifecycle_correction"):
        if contains(root, "task_lifecycle.py", needle):
            evidence.append(f"task_lifecycle.py contains {needle}")
        else:
            gaps.append(f"task_lifecycle.py lacks {needle}")
    checks.append(result("Three Classics lifecycle", "dao/human/existence", evidence, gaps))

    evidence, gaps = [], []
    for rel, needle in (
        ("attention_governance.py", "class PromptComposer"),
        ("attention_governance.py", "class RuntimeController"),
        ("tests/test_attention_governance.py", "Task Lifecycle 三经"),
    ):
        if contains(root, rel, needle):
            evidence.append(f"{rel} contains {needle}")
        else:
            gaps.append(f"{rel} lacks {needle}")
    if contains(root, "attention_governance.py", "format_task_lifecycle_correction") or contains(
        root, "attention_governance.py", "THREE CLASSICS CORRECTION"
    ):
        evidence.append("attention_governance.py wires three-classics correction")
    else:
        gaps.append("attention_governance.py lacks three-classics correction wiring")
    checks.append(result("Attention governance", "heavenly way", evidence, gaps))

    evidence, gaps = [], []
    for rel, needle in (
        ("cron_runtime.py", "format_job_registry"),
        ("cron_runtime.py", "pause_job"),
        ("frontends/fsapp.py", "GA_SCHEDULER_ENABLED"),
        ("frontends/fsapp.py", "/cron pause|resume|trigger"),
        ("tests/test_cron_runtime.py", "format_cronjob_response"),
    ):
        if contains(root, rel, needle):
            evidence.append(f"{rel} contains {needle}")
        else:
            gaps.append(f"{rel} lacks {needle}")
    if glob_any(root, "sche_tasks/*.json"):
        evidence.append("sche_tasks/*.json exists")
    else:
        gaps.append("no sche_tasks/*.json found")
    checks.append(result("Cron and Dream sidecar", "sidecar runtime", evidence, gaps))

    evidence, gaps = [], []
    for rel, needle in (
        ("dream_writeback.py", "ga.dream_writeback.v1"),
        ("dream_writeback.py", "dream_writeback_prompt_hint"),
        ("cognitive_dream.py", "build_dream_writeback"),
        ("attention_governance.py", "dream_writeback_hint"),
        ("tests/test_cognitive_dream.py", "dream_writeback"),
        ("tests/test_attention_replay.py", "dream_writeback_hint"),
    ):
        if contains(root, rel, needle):
            evidence.append(f"{rel} contains {needle}")
        else:
            gaps.append(f"{rel} lacks {needle}")
    if exists(root, "memory/cognition/dream_writeback/latest.json"):
        evidence.append("dream_writeback/latest.json exists")
    else:
        gaps.append("dream_writeback/latest.json missing")
    if contains(root, "dream_writeback.py", "ga.dream_writeback_promotion.v1"):
        evidence.append("dream_writeback.py contains promotion proposal schema")
    else:
        gaps.append("dream_writeback.py lacks promotion proposal schema")
    if exists(root, "memory/cognition/dream_writeback/promotion-proposals.json"):
        evidence.append("dream_writeback/promotion-proposals.json exists")
    else:
        gaps.append("dream_writeback/promotion-proposals.json missing")
    checks.append(result("Dream writeback loop", "feedback correction", evidence, gaps))

    evidence, gaps = [], []
    for rel, needle in (
        ("cognitive_response_policy.py", "Dream writeback output policy"),
        ("cognitive_response_policy.py", "natural short chat reply"),
        ("cognitive_response_policy.py", "one task workbench/card"),
        ("frontends/fsapp.py", "不要每个 turn 单独生成一张卡"),
        ("tests/test_cognitive_response_policy.py", "test_dream_writeback_keeps_ordinary_chat_short_without_workbench"),
        ("tests/test_cognitive_response_policy.py", "test_dream_writeback_consolidates_long_task_workbench"),
    ):
        if contains(root, rel, needle):
            evidence.append(f"{rel} contains {needle}")
        else:
            gaps.append(f"{rel} lacks {needle}")
    checks.append(result("Output shape policy", "response stream", evidence, gaps))

    evidence, gaps = [], []
    for rel, needle in (
        ("task_lifecycle.py", "ga.task_lifecycle_stats.v1"),
        ("task_lifecycle.py", "summarize_task_lifecycle"),
        ("task_lifecycle.py", "format_task_lifecycle_stats"),
        ("tests/test_attention_governance.py", "test_task_lifecycle_stats_aggregate_events"),
    ):
        if contains(root, rel, needle):
            evidence.append(f"{rel} contains {needle}")
        else:
            gaps.append(f"{rel} lacks {needle}")
    checks.append(result("Task lifecycle statistics", "existence metrics", evidence, gaps))

    evidence, gaps = [], []
    for rel, needle in (
        ("runtime_status.py", "ga.body_artifact_status.v1"),
        ("runtime_status.py", "format_body_artifact_status"),
        ("frontends/fsapp.py", "format_body_artifact_status"),
        ("tests/test_runtime_status.py", "test_body_artifact_status_reports_runtime_and_lifecycle"),
    ):
        if contains(root, rel, needle):
            evidence.append(f"{rel} contains {needle}")
        else:
            gaps.append(f"{rel} lacks {needle}")
    checks.append(result("Body artifact status panel", "body/artifact", evidence, gaps))

    evidence, gaps = [], []
    for rel, needle in (
        ("attention_governance.py", "BOUNDARY CHECK"),
        ("attention_governance.py", "boundary_preflight"),
        ("agent_loop.py", "preflight_correction"),
        ("tests/test_attention_governance.py", "test_runtime_controller_records_boundary_preflight"),
    ):
        if contains(root, rel, needle):
            evidence.append(f"{rel} contains {needle}")
        else:
            gaps.append(f"{rel} lacks {needle}")
    checks.append(result("Boundary preflight correction", "runtime pattern", evidence, gaps))

    evidence, gaps = [], []
    if exists(root, "state_store.py"):
        evidence.append("state_store.py exists")
    else:
        gaps.append("state_store.py missing")
    for rel, needle in (
        ("agentmain.py", "load_checkpoint"),
        ("agentmain.py", "save_checkpoint"),
        ("frontends/fsapp.py", "load_checkpoint"),
        ("tests/test_codex_runtime.py", "save_checkpoint"),
    ):
        if contains(root, rel, needle):
            evidence.append(f"{rel} contains {needle}")
        else:
            gaps.append(f"{rel} lacks {needle}")
    checks.append(result("Body resume and checkpoint", "body", evidence, gaps))

    evidence, gaps = [], []
    lifecycle_dir = root / "memory" / "cognition" / "task_lifecycle"
    if lifecycle_dir.exists() and list(lifecycle_dir.glob("*.jsonl")):
        evidence.append("task lifecycle jsonl events exist")
    else:
        gaps.append("no task lifecycle jsonl runtime events found")
    if (root / "temp" / "cron_job_registry.json").exists():
        evidence.append("cron_job_registry.json exists")
    else:
        gaps.append("cron_job_registry.json missing")
    if glob_any(root, "sche_tasks/done/*.md"):
        evidence.append("scheduled done reports exist")
    else:
        gaps.append("no scheduled done reports found")
    checks.append(result("Runtime evidence ledger", "existence way", evidence, gaps))

    return checks


def format_markdown(checks: list[CheckResult], root: Path) -> str:
    lines = [
        f"# GA Architecture Score",
        "",
        f"- GA root: `{root}`",
        "",
        "| Check | Layer | Status | Evidence | Gaps |",
        "| --- | --- | --- | --- | --- |",
    ]
    for item in checks:
        evidence = "<br>".join(item.evidence) if item.evidence else "-"
        gaps = "<br>".join(item.gaps) if item.gaps else "-"
        lines.append(f"| {item.name} | {item.layer} | {item.status} | {evidence} | {gaps} |")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ga-root", default=str(DEFAULT_GA_ROOT), help="GenericAgent checkout path")
    parser.add_argument("--json", action="store_true", help="emit JSON instead of Markdown")
    args = parser.parse_args()

    root = Path(args.ga_root).expanduser().resolve()
    checks = score(root)
    if args.json:
        print(json.dumps([asdict(item) for item in checks], ensure_ascii=False, indent=2))
    else:
        print(format_markdown(checks, root))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
