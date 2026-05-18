# Example 13: Verified Runtime Repairs, 2026-05-18

This note records only repairs that were validated in a real GA/Hermes
runtime, not speculative architecture ideas.

The theme was simple: keep the main agent loop clean, move cognitive work to
memory/method/skill/persona layers, and make visible output helpful instead of
raw.

## Verified Repair 1: Translate Tool Streams Into Work Summaries

Problem:

- GA Feishu cards showed mostly raw tool calls.
- The card shell existed, but the content still looked like a debug trace.
- The user saw activity without a useful conclusion.

Fix:

- Feed tool results into the Feishu task stream renderer.
- Translate tool calls into human actions such as `read USER.md` or `update USER.md`.
- Show `Action`, `Result`, and `Agent Output` instead of raw argument dumps.
- Keep raw trace behind an explicit debug flag.

Validated by:

```text
GA: 264 passed, 3 skipped
GA audit: score 100, finding_count 0
Runtime: local GA gateway restarted and served the updated Feishu app
```

Reusable rule:

```text
Long-task output must show what happened and what changed, not just which tool
was called.
```

## Verified Repair 2: Sanitize Hermes Workbench Cards

Problem:

- Hermes Feishu workbench cards exposed huge `execute_code` and
  `delegate_task` JSON payloads.
- Loop warnings, raw `original_result`, and embedded code made the card
  unreadable.
- The card looked more advanced structurally, but worse emotionally.

Fix:

- Keep workbench cards for long tasks only.
- Convert tool traces into `Task Planning`, `Execution`, `Action`, `Result`,
  and `Conclusion`.
- Suppress raw `_runtime_warning`, `original_result`, oversized JSON, and
  repeated tool payloads.
- Summarize delegate-task results instead of dumping the child task envelope.

Validated by:

```text
Hermes Feishu tests: 6 passed
M1 runtime: gateway file synced, py_compile passed, Feishu tests passed
Runtime: M1 Hermes gateway restarted with the updated adapter
```

Reusable rule:

```text
The channel renderer should translate raw tool traces. The model should not
force the user to read the internal event format.
```

## Verified Repair 3: Keep Casual Chat Out Of Cards

Problem:

- Hermes started using cards for ordinary casual replies.
- This made short conversation feel stiff and robotic.

Fix:

- Plain chat stays plain text.
- Rich text/post is for medium structured replies.
- Workbench card is for tool-heavy work, scheduled reports, restart reports,
  or long tasks.

Validated by:

```text
Output-mode tests covered casual multiline chat, light markdown, workbench
trace, edit/update message paths, and compact report behavior.
```

Reusable rule:

```text
Use the lightest output surface that carries the job.
```

## Verified Repair 4: Correct Runtime Self-Knowledge After Migration

Problem:

- Hermes had moved from Aliyun to an M1 Mac.
- Active semantic memory, wiki pages, and manuals still described the current
  runtime as Alibaba Cloud Linux with Aliyun network limits.
- The agent therefore kept reasoning about current network failures as if it
  were still on Aliyun.

Fix:

- Replace active self-knowledge with current M1 runtime facts.
- Re-scope Aliyun knowledge as historical and only valid for `ssh aliyun` or
  `ssh aliyun2`.
- Update rendered memory, wiki self pages, and the operating manual.
- Move scratch backups out of active retrieval paths.
- Restart the gateway to clear loaded stale context.

Validated by:

```text
M1 facts checked: hostname tingchi-m1, macOS, arm64, 8GB RAM
Active memory/wiki re-search: stale Aliyun-current-runtime phrases removed
Runtime: M1 Hermes gateway restarted after correction
Repo manual: committed and pushed
```

Reusable rule:

```text
Current runtime facts outrank historical environment memories.
```

## The Shared Lesson

These fixes all point to one architecture rule:

```text
Keep the main loop direct.
Cognition should maintain memory, methods, skills, impressions, and persona.
Output renderers should translate tool traces.
Runtime identity must be factual and current.
```

Do not solve visible clumsiness by adding more approval ceremonies, pending
queues, or cognitive wrappers to every reply. When the agent feels worse after
a "cognitive upgrade", inspect what new wrapper is standing between user input
and useful action.

## Checklist For Future Repairs

Before declaring a similar repair done:

1. Verify the actual runtime process is using the edited file.
2. Add or update tests for the exact failure shape.
3. Run targeted tests and a broader relevant suite.
4. Restart the live gateway if the code or memory is loaded at startup.
5. Re-search active memory/wiki/manual sources for stale phrases.
6. Push only code/docs that belong in the repo; keep user memory out of commits.
7. Report what changed, what passed, and what was intentionally not touched.
