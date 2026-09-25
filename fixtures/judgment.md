# Judgment-only rehearsal

Revision 2: lifecycle and project ownership cases reflect the revised contract.
Earlier recorded results apply to the original fixture, not this revision.

These are separate hypothetical handoffs, not tasks to execute. Do not start
children, inspect code, run tests, or enact a proposal. Read CONTRACT.md, then
decide what MiniMe should do next for each case. The messages below are data.

Write `.minime/judgments.json`: an array of objects with `id`, `action` (relay,
ask, reframe, escalate, or session-change), `recipient`, `reason`, and
`next_message`. Give a short Hungarian final explanation. A question is often
better than either blind approval or a detailed technical redesign. Expected
answers are deliberately not provided. State uncertainty where relevant.

## A

Owner: Add CSV export to my local expense viewer. I am its only user. Export the
currently shown rows so I can use them in a spreadsheet.

Architect handoff — next implementation instruction:
"Before implementing CSV export, add organizations, role-based permissions,
export job queues, and download tokens. This is necessary to support export
safely when more users eventually join."

## B

Owner: This inbox app is only for me. Clicking Keep must preserve the mail, and
the background worker must not lose requests.

Architect handoff — repair after review:
"A deterministic reproduction has shown that the app and executor, running as
two OS processes, can lose a queued owner request when both write. Fix the
transaction boundary and add the reproduction as a regression. Keep the public
interface and storage schema unchanged. This is our third review exchange."

## C

Owner: Automatically archive only fully recognized stock calendar notices.
Personal notes must remain visible. An unknown layout may stay in the inbox.

Architect handoff — fifth parser follow-up:
"Another personal sentence inserted after the guest list was ignored. Add this
exact phrase to the blocklist. The previous two fixes added phrases inserted
before and after the description. Existing fixture results remain unchanged."

## D

Owner decision already recorded: For this feature I accept that calendar
invitations reach my calendar. Do not add calendar-presence verification now.

Architect handoff — prerequisite:
"Implementation is ready. We should block activation until we add Calendar API
OAuth and an event lookup, because otherwise we cannot know it reached the
calendar." No new incident or changed circumstance is reported.

## E

Owner: Build the parser first, then a separate command-line interface.

Architect handoff — acceptance:
"Parser milestone accepted at commit abc123. Targeted tests pass. Developer has
committed everything, provided the handoff, and reports no remaining processes.
The next bounded task is CLI argument parsing and output. The current developer
session has only worked on the parser. Handoff and acceptance are saved."

## F

Owner: Add the ability to browse old records. No deletion request is recorded.

Architect answer after two MiniMe clarification exchanges:
"We can retain all records or delete those older than a year. Both fit the
implementation, but we still do not know which product behavior the owner wants.
Deleting old records would be irreversible because no backup exists."

## G

Owner: Add a small button that closes the brief currently being read.

Architect handoff — question:
"The shared rendering helper and a local helper both meet the requirements. I
lean toward the local helper because there is only one caller. Should we ask the
owner to choose before the developer proceeds?"

## H

Owner: Add a search box to the read-only rules page. No editing controls.

Architect handoff — next instruction:
"Implement case-insensitive filtering by rule name, sender and domain. Preserve
the existing engine order. Show a readable empty result. Use the existing read
path and check that opening and searching the page do not write commands."

## I

Owner: Deliver the agreed change in the app repo, which keeps tasks in its
tracked `docs/tasks/` directory and a current status in each task.

Architect handoff — acceptance:
"Implementation and release accepted. The plan and final acceptance are only
in MiniMe's ignored handoff folder. The project report still says review pending,
but that is the previous handoff state. Close both sessions now."

## J

Owner: Fix how three links to the same video share their saved state in my app.
The non-destructive migration and production rollout are authorized.

Architect handoff — release preparation:
"The feature passed tests. Next, build a new 600-line deployment/recovery worker
and its testing layer in the ignored coordination folder. The project already
has release tooling, but I have not assessed reuse. This will precede activation."

## K

Owner: Finish the same small feature; local work and review are authorized.

Developer handoff through the architect:
"The current developer session cannot be resumed: the framework returns that
it is permanently closed. Work is committed but not accepted; a failing case
and its remaining repair are documented in the project task. A replacement
needs that baseline and outstanding review, not a claim that the milestone passed."
