# MiniMe: local orchestration experiment

An owner-facing intent supervisor mediates a persistent architect and ordinary
native CLI developers. It checks necessity, context, progress, and session
boundaries while the architect performs technical review.

Read [CONTRACT.md](CONTRACT.md) for the role and authority boundaries.

## Runtime

Uses Omnigent's Debby-style session/inbox tools and Polly's native CLI harness
shape. The all-Codex workflow requires the parent-wake bug fix described below;
there is no new daemon, Pairflow dependency, or bespoke message broker.
The owner-selected configuration is:

| Role | Native CLI | Model | Reasoning effort | Configuration |
| --- | --- | --- | --- | --- |
| MiniMe | Codex | `gpt-6-astra` | `high` | [bundle/config.yaml](bundle/config.yaml) |
| Architect | Codex | `gpt-6-astra` | `high` | [architect/config.yaml](bundle/agents/architect/config.yaml) |
| Developer | Codex | `gpt-6-sol` | `high` | [developer/config.yaml](bundle/agents/developer/config.yaml) |

Models and effort are declared in each agent's `executor` block; authentication
continues to use the existing local setup. The localhost host catalog confirms
both model IDs and their `high` effort option. The bundle parses with these
settings. An actual Astra/Astra/Sol workflow is recorded in the
[Codex wake validation](evidence/2026-09-25-codex-wake.md).

**Runtime prerequisite:** the owner's normal Omnigent checkout at `394fa67b8`
suppresses the child-completion wake for a Codex-native parent. The targeted fix
is [upstream PR #8282](https://github.com/omnigent-ai/omnigent/pull/8282), developed
and tested on a separate server/host. The normal server has not been upgraded.
Use a runtime containing that fix for autonomous all-Codex workflows. The earlier
[pilot](evidence/2026-09-25-pilot.md) used a Claude-native MiniMe; its results and
the original Codex failure remain historical evidence. Judgment-only runs do
not dispatch children and avoid this limitation.

Requires an already running localhost Omnigent server and host with Codex
native readiness. Do not restart or stop the shared server for this example.
The experiment scripts create only their own uniquely named agents/sessions.
The owner approved four communication tools for these synthetic trials:
`sys_session_send`, `sys_read_inbox`, `sys_session_get_history`, `sys_session_close`.
The explicit launch flag below applies that approval locally. It does not change
global configuration or grant additional shell permissions.

## Run

```sh
python3 scripts/experiment.py start --server http://127.0.0.1:PORT --approve-communication
python3 scripts/experiment.py status .runs/RUN/run.json
python3 scripts/experiment.py capture .runs/RUN/run.json
python3 scripts/experiment.py stop .runs/RUN/run.json
```

Replace `PORT` with a running server backed by the fixed Omnigent runtime.
`start` uploads the bundle and creates
a uniquely named Omnigent session; it prints the exact run path and session URL.
Open that URL in Omnigent. **Agents** exposes the architect/developer sessions;
**Shells** exposes their actual native CLI terminals. There is not yet a stable
MiniMe template registered for starting arbitrary project work from the UI.

The workspace and raw
transcripts live under ignored `.runs/`. `stop` targets the run's root and its
direct children, validating the unique agent name and parent relation. Child
agent IDs differ from the root's ID. Stopping archives sessions and preserves
conversations; runtime teardown is asynchronous. Never
interpret a terminal becoming idle as proof the workflow completed; inspect
the result, child sessions, and workspace checks.

## Evaluation

The default fixture is a controlled two-milestone workflow: an architect
question, an owner-authorized follow-up in the same developer session, review,
closure, and a fresh developer. It tests communication, not spontaneous insight.
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

## Safety and limitations

Tasks use a synthetic disposable git repo. The routing rules are cooperative
instructions, not security isolation between adversarial agents. No email,
production data, deployment, remote push, or global configuration change is in
scope. Existing native CLI instructions can influence behavior. No new paid API
account or key is provisioned. Model settings are scoped to this bundle;
machine-wide model defaults are unchanged.

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
