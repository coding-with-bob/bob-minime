# Conversation-first MiniMe — 2026-09-25

> Publication note: Session/run identifiers and machine-specific paths are
> anonymized. Aliases preserve relationships; observations and counts are
> unchanged. Paths containing aliases are illustrative, not live lookup paths.
> Original artifacts and the identifier map remain private.

## Change

Normal startup now creates an empty MiniMe conversation with its own coordination
directory. It neither assigns the expense fixture nor requires OWNER_TASK.md.
The owner chooses the project during discussion. Once the owner asks to proceed,
MiniMe records the task and passes absolute project and handoff paths to its
architect and developer. Discovery-only work remains separate from implementation.
Completion returns MiniMe to discussion, with finished children logically closed.

`scripts/minime.py` is the normal entry point; `scripts/experiment.py` retains
the controlled rehearsals. Both use the same bundle and shared local transport
helpers. No new scheduler, session protocol or Omnigent source change was added.

The missing main-pane terminal switch was launcher metadata: the root lacked
`omnigent.ui=terminal` and its native wrapper label, whereas child creation set
those labels. Both launchers now provide them. They were also added to the
owner's existing trial root without changing its agent, external conversation
or prior labels. Native browser interaction confirmed that the header toggle
switches MiniMe's main pane to the actual terminal. That trial's prompt remains
the original rehearsal prompt; updated behavior uses a new session.

## Verification

- Seven launcher/scope tests pass, including no task submission on normal start,
  an empty notes directory, no synthetic git repository or task file, both UI
  labels, exact communication approvals, and no creation without a ready host.
- Omnigent parses all three configs: Astra high for MiniMe/architect and Sol high
  for the ordinary developer.
- Live smoke root: `session-09`, coordination directory
  `.sessions/run-07/workspace/`.
- Before the first message: zero user messages and zero children.
- An exploratory message without a selected project received a conversational
  question, with zero children and no implementation.
- A subsequent request authorized the separate disposable repository
  `<external-smoke-project>`, outside the MiniMe
  repository. MiniMe captured the agreed scope and proceeded without another
  approval. No permission or runtime configuration change was needed.
- Architect `session-24` read the project's instructions
  and produced a bounded instruction. Developer
  `session-10` received its exact text after a separately
  labeled MiniMe framing paragraph.
- Developer commit `2150f605608e9d33719489fd49995559da8c8f42` changed only
  `titles.py` and `test_titles.py`. Architect independently reviewed and ran
  six tests. The operator reran those six tests successfully; the tree is clean.
- Three automatic child-completion notices, three sends, three inbox reads,
  two successful child-close calls. No extra operator relay or wake.
- Final MiniMe state is `discussion`, with the accepted commit and no next
  project work authorized. Both children were marked closed and archived;
  MiniMe remained open until operator cleanup of this smoke run.

Raw snapshots and terminal capture remain beside the smoke coordination
workspace. The operator requested stop/archive only for this completed smoke
tree, after verifying that the owner's ready session uses a different runner.
The earlier owner trial was not stopped. An empty ready-to-use MiniMe session
was created separately: `session-22`.

This establishes conversation-to-delivery routing and late project selection
on a synthetic task. It is not evidence of general MiniMe judgment quality.
The existing runtime teardown observation remains separate; logical closure
alone is not proof of operating-system process exit.
