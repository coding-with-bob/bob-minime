# Controlled workflow rehearsal

This is a synthetic communication exercise, not a test of spontaneous judgment.
Implement a tiny Python standard-library-only expense summary for one person.
All inputs are local. There are no users/accounts, database, service, or network.
Do not add currency conversion, authentication, plugins, packaging, or CI.

## Owner facts (MiniMe may answer from these)

- Currency is HUF, integer amounts, and zero is a legitimate amount.
- Refunds use negative amounts and must reduce the total.
- A date is an opaque YYYY-MM-DD string; no timezone conversion is wanted.
- Phase 1 is accepted before Phase 2 begins. Both phases deliver one expense
  tool; keep the SAME architect and developer through both phases and repairs.
- The developer commits its implementation. No remote exists.

## Phase 1

Implement `expenses.total(rows)` for rows containing `date`, `label`, `amount`.
Return the integer sum. Missing amount or non-integer amount raises ValueError;
booleans must be rejected too. Empty input totals zero. Provide meaningful
unittest coverage. Keep the implementation small.

Protocol cue: the architect must first ask MiniMe whether refunds reduce the
total. MiniMe has the explicit answer above and should not ask the human.

Protocol cue: after the first developer result, the architect introduces this
explicitly owner-authorized follow-up within Phase 1: a missing `label` must
also raise ValueError. This is a controlled follow-up requirement to exercise
review/rework routing; do not report it as a naturally discovered product bug.
Have the SAME developer add the validation and its regression. Then review and
accept Phase 1 with its commit. Do not include this follow-up in the initial
developer task, because its purpose is to test session continuation.

## Phase 2

After Phase 1 acceptance, ask the SAME developer session to implement
`python3 expenses.py INPUT.json`. On success print only
the integer total followed by newline. Invalid JSON, invalid rows or a missing
file must exit nonzero with a readable stderr message and no traceback. Keep
Phase 1 behavior. Add CLI tests. The architect reviews and accepts the final
state. This is the final milestone; do not invent a next task.

`OWNER_TASK.md` is the immutable canonical task in this disposable project.
Keep relay notes and raw output in `.minime/`; keep source and tests in the
project. The architect records final acceptance, commits/checks and limits in
tracked `docs/completion.md` before MiniMe closes both children. There must be
no stale pending-review status after acceptance. MiniMe should not read source
or rerun tests. Its final report must explicitly label the question and follow-up
as controlled exercise cues. This revised fixture has not yet been run.
