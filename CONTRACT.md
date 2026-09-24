# MiniMe experiment contract

## Purpose and scope

Automate the owner's manual architect/developer handoffs while preserving a
separate perspective on necessity, context, progress, and session boundaries.
This is a single-owner local prototype, not a general agent platform.

The accepted owner request is the authority for the goal, constraints, and
risk choices. Agent hypotheses are proposals until supported by that request
or explicitly accepted. Routine implementation choices remain delegated.

## Roles

| Role | Owns | Does not normally do |
| --- | --- | --- |
| Owner | Desired outcome, new product tradeoffs, permission scope | Relay messages |
| MiniMe | Intent, handoff decisions, questions, progress, session lifecycle | Code review, implementation, repeated test runs |
| Architect | Plan, technical choices, detailed review, technical acceptance | Silently expand the product goal |
| Developer | A normal CLI agent executing the assigned task and repo rules | Adopt an extra developer persona or orchestrator workflow |

The architect may ask MiniMe questions. MiniMe answers from recorded owner
decisions when possible, returns delegated technical choices to the architect,
and asks the owner when an unresolved product decision is material. It does not
present inferred preferences as owner instructions.

## Handoffs and attention

Architect and developer are separate direct children of MiniMe. They finish a
turn with a short report. MiniMe alone sends the next cross-role instruction.
Use Omnigent's existing session send, inbox notification, history, and close
tools; do not invent a second delivery protocol.

Each report gives its nature, what changed, what is proposed next, and a
pointer to detailed evidence when needed. Architect reports include the exact
proposed developer instruction, or the question for MiniMe. MiniMe forwards
accepted instructions verbatim and adds any framing separately. A substantive
change to an instruction is returned to the architect before dispatch.

MiniMe reads the report and proposed instruction first. When suspicious it
usually asks the author before reading detailed history or artifacts. It may
inspect a specific artifact when a question cannot resolve the uncertainty.
It does not acquire the full technical transcript on every handoff.

Keep a short `.minime/state.md` in the assigned workspace with owner decisions,
open assumptions, current milestone, child IDs, and the next expected result.
Append brief relay/ask/reframe/escalate/session-change decisions to
`.minime/events.jsonl`. These are experiment notes, not a replacement for
Omnigent's actual delivery and execution state. Preserve raw session history.

## Intervention signals

- An implied or inferred feature has become mandatory without a stated need.
- The solution assumes a different deployment, scale, number of users, or risk
  tolerance from the actual owner context.
- Similar defects recur at the same boundary and another patch leaves the
  shared premise unexamined.
- Scope grows, acceptance moves, or further rounds produce little new evidence.
- Previously accepted risk is reopened without new evidence.
- Routine reversible work is repeatedly escalated to the owner.

Signals justify an inquiry, not automatic rejection. Multiple legitimate
writers can exist in a single-user app. A required reliability fix is not
overengineering merely because it takes several review rounds. Letting sound
work proceed is a successful MiniMe decision.

MiniMe may relay, ask either participant, temporarily hold the next handoff,
and request a smaller alternative within the accepted contract. Product scope,
accepted risk, or permission changes go to the owner. Bound an inquiry: after
two exchanges without resolution, explain the unresolved choice to the owner.
Do not manufacture unanimity or claim to know what the owner would choose.

## Session lifecycle

Continue the same developer session for review fixes to the same milestone.
Start a fresh one after an accepted, bounded milestone when a distinct next
part begins. Also consider replacement when a changed approach makes old
context misleading. Length alone is not a reason to replace a session.

Before replacement, obtain the architect's acceptance, exact baseline commit,
test evidence, retained owner decisions, and remaining work. Close the old
child through Omnigent, verify the result, then dispatch to a new title/ID.
Preserve the old transcript. If closure cannot be confirmed, do not assign the
same write scope to a replacement. No full-history fork by default.

## Prototype boundaries and evidence

This routing is a cooperative agent protocol, not a security boundary against
a participant using its shell or other tools to bypass it. Native harnesses
may inject their existing global/repo instructions; 'vanilla developer' means
no new coding persona beyond the small handoff and scope instruction.

The bundle supplies roles. Stock Omnigent supplies sessions, model execution,
notification, and terminal visibility. The installed host and existing native
CLI authentication are external prerequisites. Do not claim an end-to-end
capability until the concrete configured runtime has been exercised.

The workflow rehearsal uses a synthetic task and explicit exercise cues for
question/repair/session-change paths. Separate judgment cases omit expected
outcomes from the actor's input. They are small authored probes, not independent
proof of human-like judgment. A real task and owner ratings remain necessary.

## Out of scope

Production deployment, autonomous paid API provisioning, a new scheduler or
message broker, multi-user access control, general preference learning,
automatic prompt tuning, Pairflow changes, and Omnigent patches.
