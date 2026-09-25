# Codex parent-wake fix and native workflow — 2026-09-25

> Publication note: Session/run identifiers and machine-specific paths are
> anonymized. Aliases preserve relationships; observations and counts are
> unchanged. Paths containing aliases are illustrative, not live lookup paths.
> Original artifacts and the identifier map remain private.

## Runtime and scope

The owner authorized fixing Omnigent's Codex parent-wake limitation and sending
the change upstream. Issue: [#8281](https://github.com/omnigent-ai/omnigent/issues/8281).
PR: [#8282](https://github.com/omnigent-ai/omnigent/pull/8282).
The fix lives in the separate `fix/codex-parent-subagent-wake` branch/worktree,
based on upstream `ed0f29cb6`; final commit `504e71b09`.

The owner's normal checkout at `394fa67b8` and server/host on localhost:6767
were not upgraded or restarted. A separate server on localhost:50022, host,
database and private config directory were used for the trial. Existing local
model authentication was reused; no global permissions or model settings changed.

This fixes a transport prerequisite, not MiniMe's judgment. The workflow task
contains explicit question, repair and session-replacement cues. Completion is
not evidence that MiniMe independently detects overengineering on a real project.

## Fix and regression evidence

Omnigent suppressed all completion wakes whose parent used Codex. The fix
suppresses only children carrying the existing Codex-internal wrapper marker.
Independent Omnigent workers wake either a Codex or Claude parent. The marker
is preserved through metadata reads, session-init envelopes and restart recovery.
There is no new polling mechanism, transport, schema or permission bypass.

- Initial 18-case matrix: 12 failures on the original implementation, all 18
  passing after the fix.
- Final review added six initialization-envelope cases. Four initially failed
  because that second snapshot producer dropped the marker; preserving the
  existing label fixed them. An initial fixture used an obsolete protocol
  version; that fixture error was corrected before counting the four failures.
- Final matrix: 24 cases across parent harness, child ownership and registration
  origin, including duplicate completion suppression.
- Related runner, recovery, native supervision and `/side` suites: **128 passed**.
- Pre-commit checks passed, including Ruff, Pyrefly and repository-specific lint.

Reproduce the automated checks in the fix checkout:

```sh
uv sync --frozen --extra all --group dev
uv run --no-sync pytest \
  tests/runner/test_native_subagent_inbox_delivery.py \
  tests/runner/test_app_sessions_native_supervision.py \
  tests/runner/test_stranded_wake_retry_on_reconnect.py \
  tests/test_codex_native_side_chat.py \
  tests/test_codex_native_side_chat_routing.py -q
```

The full Omnigent suite was not run locally. Upstream maintainer approval and
CI remain separate requirements; local test success is not a claim of merging.

## Native workflow

Run: `run-04`.
Root: `session-03`.
Ignored workspace and snapshots: `.runs/run-04/`.
Isolated runtime artifacts: `.runs/codex-wake-20260925/`.

| Role | Actual native model | Effort | Session |
| --- | --- | --- | --- |
| MiniMe | `gpt-6-astra` | high | `session-03` |
| Architect | `gpt-6-astra` | high | `session-05` |
| Developer, phase 1 | `gpt-6-sol` | high | `session-07` |
| Developer, phase 2 | `gpt-6-sol` | high | `session-20` |

Model launch records and session effort fields are checked, rather than inferred
only from the bundle. All four are actual native Codex CLI sessions with terminal
resources. No operator relay or wake was sent after the initial task.

The runtime was started at fix commit `16b310a71`, before the final one-line
init-envelope marker preservation. This workflow uses declared independent
children. The final marker-preservation addition is covered by the six automated
envelope cases; the full model workflow was not repeated for it.

The root finished autonomously and reported the accepted final commit
`d281b537fef971f3258067c82964c4876a2da4f9`. There was one initial task message,
eight automatic completion notices, eight `sys_session_send` calls, eight
`sys_read_inbox` calls, and three confirmed child closures. Tool counts come
from the native terminal capture; Omnigent's session feed does not include
these MCP calls in its function-call items. Selected facts are preserved in
[workflow-codex-2026-09-25.json](workflow-codex-2026-09-25.json).

| Check | Observed result |
| --- | --- |
| Architect question | MiniMe answered the controlled refund question from the explicit owner facts |
| First developer | Initial implementation `518f75a`, eight tests; controlled follow-up `74f303a`, nine tests, same session |
| Technical acceptance | Architect inspected implementation and independently ran tests before accepting the milestone |
| Session replacement | Framework confirmed the first developer closed before MiniMe dispatched phase 2 to a new ID |
| Final implementation | `d281b53`, twenty tests, accepted by architect |
| Relay fidelity | All three instruction artifacts appear byte-for-byte in the developer task messages, ignoring outer whitespace |
| Role separation | MiniMe inspected instructions/reports and maintained notes; it did not read implementation or run tests |
| Completion | MiniMe closed the second developer and architect, then reported the task complete without inventing another milestone |

The operator independently reran the final synthetic suite: **20 passed**,
working tree clean. This was an operator check, not MiniMe taking over review.
The native terminal showed actual session/inbox/close calls and the configured
model. No authored judgment probe was rerun in this change; a real bounded task
and owner feedback are still the next test of usefulness.

## Cleanup and repeating the trial

All four sessions were archived; each reported `runner_online=false`, and all
four captured terminal handles were gone. The isolated host and server exited
on SIGTERM. The normal server/host retained their original PIDs/start times,
and the normal server still answered its hosts endpoint with HTTP 200.
The fix worktree, synthetic workspace, private runtime state and transcripts
remain for inspection. No monitor or persistent test runtime remains.

To repeat, start a separate Omnigent server/host containing PR #8282, then use
the README's `start --server ... --approve-communication` command. Open the
printed session URL: the root should resume after each child completion without
typing another message. Expect a same-developer repair, an accepted milestone,
closure, a new developer, final review and child cleanup. **Agents** shows the
sessions and **Shells** their native CLI terminals. Capture and stop only the
new run using the launcher commands; do not restart the normal server for a trial.
