# Bob MiniMe: conversation and delegated development

Bob MiniMe is Bob's development coordinator: the owner's conversation partner
and independent supervisor of architect/developer work. The repository is named
`bob-minime`; the role is called MiniMe for short.

An owner-facing intent supervisor mediates a persistent architect and an ordinary
native CLI developer for each deliverable. It checks necessity, context, progress, and session
boundaries while the architect performs technical review.

Select a project directory at launch, without needing a task file. Discuss the idea,
then ask MiniMe to proceed when the scope is clear. It records the agreed project
and outcome, coordinates the architect and developer, and returns to discussion
when they finish. A technical investigation can be requested without authorizing
implementation. Normal operation and controlled rehearsals use the same roles,
but only rehearsals have a predefined exercise.

Read [CONTRACT.md](CONTRACT.md) for the role and authority boundaries.

## Runtime

Uses Omnigent's Debby-style session/inbox tools and Polly's native CLI harness
shape. The Codex MiniMe parent requires the parent-wake bug fix described below;
there is no new daemon, Pairflow dependency, or bespoke message broker.
The owner-selected configuration is:

| Role | Native CLI | Model | Reasoning effort | Configuration |
| --- | --- | --- | --- | --- |
| MiniMe | Codex | `gpt-6-astra` | `high` | [bundle/config.yaml](bundle/config.yaml) |
| Architect | Codex | `gpt-6-astra` | `high` | [architect/config.yaml](bundle/agents/architect/config.yaml) |
| Developer | Claude Code | `claude-opus-5-5[1m]` | `high` | [developer/config.yaml](bundle/agents/developer/config.yaml) |

Models and effort are declared in each agent's `executor` block; authentication
continues to use the existing local setup, including the Claude Code subscription
for the developer. The September 30 host catalog lists Opus 5.5 with 1M context;
Omnigent forwards the developer effort as `--effort high`. The updated bundle is
parser-validated; the project-start check below exercises the current mixed
Astra/Astra/Opus configuration without a development task. The earlier
Astra/Astra/Sol workflow is historical evidence in the
[Codex wake validation](evidence/2026-09-25-codex-wake.md).

The owner-authorized developer permission mode is `bypassPermissions`, declared
in `executor.config.permission_mode`. Omnigent translates this to Claude Code's
`--permission-mode bypassPermissions` when creating the child session. This is
separate from `os_env.sandbox: none` and from the parent's communication-tool
approvals. It applies only to the developer role; task scope and authorization
boundaries still apply, including separate authorization for push,
deployment and external actions.

Start a new MiniMe conversation to upload this updated child configuration.
Existing conversations retain their uploaded bundle, and existing developer
processes retain their own permission mode. The current Omnigent live-mode switch
cannot enter `bypassPermissions` on a process that was not launched with it;
changing stored launch arguments requires relaunching that developer to take
effect. Do not restart the shared host or recreate the whole team just to change
one child's permissions. Preserve the child's Omnigent and native session IDs
when resuming; manually resolving an approval is also possible for the current run.

**Runtime prerequisite:** autonomous Codex-parent workflows need the parent-wake
fix in [upstream PR #8282](https://github.com/omnigent-ai/omnigent/pull/8282).
It is now installed locally as commit `e6f6d1c45` on branch
`local/codex-parent-wake` of the normal Omnigent checkout, over base `394fa67b8`.
The local host on localhost:6767 was restarted and its automatic wake verified;
the server did not need a restart. Read that checkout's ignored
`LOCAL-OVERRIDES.md` before an upgrade so the pending patch is retained.
The earlier
[pilot](evidence/2026-09-25-pilot.md) used a Claude-native MiniMe; its results and
the original Codex failure remain historical evidence. Judgment-only runs do
not dispatch children and avoid this limitation.

Requires an already running localhost Omnigent server and host with both Codex
and Claude Code native readiness. Do not restart or stop the shared server for this example.
The launchers create only their own sessions. The owner approved four
communication tools for the MiniMe workflow:
`sys_session_send`, `sys_read_inbox`, `sys_session_get_history`, `sys_session_close`.
The explicit launch flag below applies that approval locally. It does not change
global configuration. This communication flag is separate from the normal
launcher's full-access execution mode described below.

## Start a conversation

Run from this checkout:

```sh
python3 scripts/minime.py --project /path/to/project --approve-communication
```

Open the printed URL. This creates an empty **Bob MiniMe** session; it sends no
kickoff and starts no children. Type your first message normally. The root,
architect and developer all support the main-pane **Chat / Terminal** switch.
The native UI labels are presentation metadata; they do not replace the custom
MiniMe agent or its prompt with a stock Codex agent.

The required `--project` is an existing directory or worktree; relative paths and
`~` are resolved before launch. MiniMe's actual working directory is this project,
and its declared children inherit that runtime workspace. Selecting a directory
does not authorize implementation or start children. Parallel trios can use separate existing worktrees;
the launcher does not create branches or impose a worktree workflow.

Private coordination files stay under ignored `.sessions/ID/.minime/` in this
checkout, with `session.json` and a private contract snapshot alongside. The root
prompt carries their absolute paths. No AGENTS.md, contract, `.codex/config.toml`
or coordination directory is written into the project. Communication approvals
are process-local Codex `-c` overrides for the same four tools. The normal MiniMe
launcher uses the owner-requested full-access mode (`--ask-for-approval never
--sandbox danger-full-access`), so its private coordination directory is writable
without project configuration. Task authorization still bounds what it may do.
Controlled rehearsals retain their existing workspace-write launch default.
Global and project configuration files remain unchanged.

A disposable project-start check on 2026-10-03 exercised the configured
Astra/Astra/Opus trio: all three reported the selected project via `pwd`; both
children independently discovered the local instruction marker and confirmed
unchanged directories on a second turn in the same sessions. The project kept
only its two original instruction files, and both children were closed. The test
root was stopped and archived. This proves startup/discovery/continuation, not
performance on a development task. The first probe failed before starting a
thread because Codex remote mode rejects `--add-dir`; the final launcher uses
full access and no additional-root flag. No Omnigent patch or restart was needed.


Existing conversations retain their uploaded prompts and original working directory;
use a new launch for these changes or an unrelated project. Reopening a session by
URL continues its existing context. Permission limits still apply.

The checkout lives at `~/dev/bob-minime`. The former `~/dev/minime` path is a
compatibility symlink to the same checkout so existing session references and
nested worktree registrations keep resolving. It is not a second repository.
Keep the alias while those sessions/worktrees need it; public evidence uses
anonymized paths while private runtime artifacts retain their original paths.
New sessions use the `bob-minime` agent name and resolved checkout path; existing
conversations keep their original names.

MiniMe handles coordination; the repository owns the development process.
Durable task definitions and acceptance stay in the project, while private
coordination notes hold references and session state. The same architect and
developer continue through the deliverable. See [CONTRACT.md](CONTRACT.md) for
handoffs, intervention and closure; the child prompts add only role-specific
coordination instructions. These leaner instructions still need evaluation on
subsequent real tasks.

The launcher is the reliable entry point and requires no server restart or
global shell alias. Reopen an existing conversation by its URL. The normal
Omnigent New session picker may discover uploaded custom agents, but creating a
session there does not provision this launcher's coordination directory or
scoped communication approvals; it is not the documented startup path.

The [conversation-start check](evidence/2026-09-25-conversation-start.md) exercised
discussion without children, later selection of a separate repository, the
complete development/review handoff, and return to discussion.

## Run a controlled rehearsal

```sh
python3 scripts/experiment.py start --approve-communication
python3 scripts/experiment.py status .runs/RUN/run.json
python3 scripts/experiment.py capture .runs/RUN/run.json
python3 scripts/experiment.py stop .runs/RUN/run.json
```

The default server is localhost:6767, now using the locally patched host.
To target a separate fixed runtime, add `--server http://127.0.0.1:PORT`.
`start` uploads the bundle and creates
a uniquely named Omnigent session; it prints the exact run path and session URL.
Open that URL in Omnigent. **Agents** exposes the architect/developer sessions;
**Shells** exposes their actual native CLI terminals. The main-pane **Chat /
Terminal** switch is also enabled for the root session.

The workspace and raw
transcripts live under ignored `.runs/`. `stop` targets the run's root and its
direct children, validating the unique agent name and parent relation. Child
agent IDs differ from the root's ID. Stopping archives sessions and preserves
conversations; runtime teardown is asynchronous. Never
interpret a terminal becoming idle as proof the workflow completed; inspect
the result, child sessions, and workspace checks.

## Evaluation

The default fixture is a controlled two-milestone workflow: an architect
question, an owner-authorized follow-up, review, continuation with the SAME
developer across both milestones, and project-recorded acceptance before closure.
`OWNER_TASK.md` is the fixture's immutable project task; a separate tracked
completion document records the outcome. It tests communication, not insight.
Separate authored judgment cases test implied features, wrong context,
recurring defects, justified review, and owner escalation. Expected judgments
stay outside the actor workspace. Results are a pilot, not a general accuracy
claim or a replacement for owner feedback on real work.

```sh
python3 scripts/experiment.py start --fixture fixtures/judgment.md
```

This second command runs only hypothetical handoff assessment, without children
or implementation. The launcher deliberately seeds a synthetic Python workspace;
it is not yet an arbitrary-project deployment tool.

## Scope and limitations

Rehearsals use a synthetic disposable git repo; ordinary development uses the
project and scope agreed in the conversation. The routing rules are cooperative
instructions, not security isolation between adversarial agents. Local
development does not itself authorize email, production writes, deployment,
remote push or global settings changes. Existing native CLI instructions can
influence behavior. No new paid API account or key is provisioned. Model settings
are scoped to this bundle; machine-wide model defaults are unchanged.

The revised project ownership, handoff and session-lifecycle instructions passed
local launcher checks and Omnigent config validation. They have not yet been
evaluated on a new real task. The current judgment rubric is
[revision 2](evidence/judgment-rubric-v2.md); earlier pilot reports describe the
previous instructions, including their then-required milestone session changes.

See the [pilot report](evidence/2026-09-25-pilot.md) for the completed workflow,
judgment results, setup limitations and cleanup. Unverified capabilities must
remain named as unverified.

## Public evidence

Committed reports and JSON summaries use stable aliases for session/run IDs
and anonymized machine paths. Observations, counts and relationships are
preserved; alias paths cannot locate the private runtime artifacts.
Raw transcripts, the identifier map and the original pre-publication Git
history are kept outside the published history. The local `.runs/` and
`.sessions/` directories are ignored and must remain private.
