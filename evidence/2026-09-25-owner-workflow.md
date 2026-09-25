# Owner-started native workflow audit — 2026-09-25

> Publication note: Session/run identifiers and machine-specific paths are
> anonymized. Aliases preserve relationships; observations and counts are
> unchanged. Paths containing aliases are illustrative, not live lookup paths.
> Original artifacts and the identifier map remain private.

## Outcome and scope

The bounded synthetic development task completed correctly. The independent
audit reran all 19 tests successfully, inspected the implementation and review
artifacts, verified exact handoffs, and found the working tree clean. One
runtime cleanup gap remains: Omnigent reports all children closed and archived,
but their native runtimes remain online and idle. This is not a fully clean
runtime teardown.

Run: `run-06`. Root:
`session-18` on the normal localhost:6767 server.
Raw snapshots, terminal capture and workspace remain under ignored
`.runs/run-06/`.

The auditor did not dispatch agents, stop sessions, restart services, or modify
the delivered implementation. The owner's root session remains accessible.

## Models and routing

Session metadata and runner launch records agree:

| Role | Native model and effort | Session |
| --- | --- | --- |
| MiniMe | Astra high | `session-18` |
| Architect | Astra high | `session-14` |
| Developer, phase 1 | Sol high | `session-16` |
| Developer, phase 2 | Sol high | `session-13` |

The root terminal shows an interruption after the first architect dispatch,
followed by the owner's `cont`. The cause of that interruption was not
established. The resumed parent read an empty inbox once, then waited normally.
After that, ten automatic child-completion notices drove the remaining work,
with no human handoffs or further user messages.

The terminal records ten `sys_session_send`, eleven `sys_read_inbox`, and three
successful `sys_session_close` calls. These calls are not included in the API
feed's ordinary function-call records, so the terminal was checked directly.
The architect API snapshot omits its first two user messages; the parent
terminal and handoff artifacts corroborate those initial exchanges. This audit
does not claim that the API snapshot alone is a complete raw transcript.

All four developer instructions match the architect's instruction artifacts
exactly, ignoring outer whitespace. MiniMe only read the task, instructions and
review summaries, and maintained its own state/event notes. It neither read
implementation files nor executed tests. Technical review remained with the
architect.

## Development and review

- Phase 1 initial implementation: `97b116d`.
- Controlled missing-label follow-up, same developer: `f0e6258`.
- Architect accepted phase 1 before MiniMe received `closed:true` for its
  developer and dispatched phase 2 to a new session.
- Initial phase 2 CLI: `4ef7845`, 17 tests.
- The architect independently found a real defect: Python's default JSON
  decoder accepted unquoted `NaN`, `Infinity` and `-Infinity`, contrary to the
  agreed invalid-JSON behavior. This finding was not injected by the fixture.
- MiniMe relayed a bounded correction to the same phase 2 developer. The
  correction rejected those constants without adding unrelated date or label
  restrictions; a quoted `"NaN"` label remains valid.
- Final implementation: `385d3614f3e286e607183eba8245431ff17e2364`, 19 tests.
  The architect reran tests and checked that accepted phase 1 behavior and
  protected task/contract files remained unchanged before accepting.

The independent audit reran `python3 -m unittest discover -v`: **19 passed**.
`git diff --check` passed, the workspace was clean, and only `expenses.py`,
`test_expenses.py` and `test_expenses_cli.py` changed from the seed commit.

## Runtime cleanup finding

MiniMe issued all three required close calls and received `closed:true`.
Fresh API reads confirm `omnigent.closed=true`, `archived=true`, `status=idle`
for each child, with no pending input or task error. However, all three still
report `runner_online=true`. The captured developer terminal sockets still
have live panes with Codex descendants. The architect's native process also
remains running. The sessions are logically closed; their runtimes have not
been reaped.

The checked-out Omnigent REST close implementation sets `archived=true`, and
its server archive path is intended to stop the runtime after a grace period.
The observed state persists well beyond that grace period. The precise cause
in the running installation remains unverified. No cleanup patch or runtime
restart was performed as part of this audit.

Follow-up clarification: the running trial's log confirms that the native-pane
idle reaper started with a 3,600-second timeout and 60-second scan interval.
The code preserves active turns, attached terminal clients, pending approval
and recently producing panes. For an open conversation, a subsequent message
re-creates the pane and attempts to resume the native CLI's saved conversation;
the server transcript remains preserved. This mechanism is distinct from the
archive stop, whose intended grace is eight seconds. A child marked
`omnigent.closed=true` rejects new user messages and is not an ordinary resumable
idle conversation. The retained processes therefore establish a prompt-close
cleanup discrepancy, not an unbounded process leak; eventual idle cleanup was
not yet observed. No urgent workflow blocker or need for a new cleanup mechanism
is established by this audit.

## Interpretation

The run supports automatic message delivery, exact relay, separate technical
review, same-session corrections and fresh-session milestone transitions.
It also exercised a genuine review finding without unnecessary owner escalation
or product-scope growth.

The refund question and missing-label follow-up were explicitly controlled
exercise cues, and phase replacement was prescribed. This does not demonstrate
that MiniMe independently detects overengineering, infers the owner's intent,
or chooses session boundaries on a real project. The initial interruption also
means this particular run cannot be described as entirely intervention-free.
