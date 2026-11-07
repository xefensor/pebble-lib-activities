# Pebble Activities maintenance contracts

These are current implementation constraints. They apply when changing the
relevant subsystem, not as a requirement to reread every document for every edit.

## Ownership and compatibility

This is a stock-PebbleOS library/convention, not an official standard or background service. Preserve schema1/2/3/4 and ACT1/2/3 compatibility and the public root API. Native owner state/alarms remain authoritative; receipt is acceptance, not a disk-flush/alarm guarantee. Preserve source/run identity and original observation/validity across polls and reconnects. Zero is not completion. Discovery validates returned UUIDs, versions, permissions and removal. Private media/notification content stays transient.

## Current interaction and product boundaries

New providers use summary/schema4, with content separate from host-owned placement, priority and motion. Terminal result visibility is opt-in. A host owns subscriptions, AppMessage dispatch and its single queue. Eight stable publisher slots do not evict other runs; revisions apply source-wide. Imported snapshots preserve original owner history. Root/host imports retain ownership and independent nested data. Consumer pins never change automatically.

## Source ownership

src/js owns injected publisher/provider/consumer helpers; include and src/c own bounded portable packet/state helpers. Root entry modules preserve public provider/consumer imports.

## Phone persistence and evidence

For apps with phone settings, keep active-writer selection, separate Android
DOM/native storage views, exact application acknowledgements and bounded handoffs.
Saving stays open where supported; uncertain writes retain the draft and explicit
readback/retry. Discard cannot undo a write already sent. Load errors must not
silently replace saved choices with editable defaults. Do not introduce unsolicited
focus or scroll changes. Historical browser/emulator results do not validate a
new build. Keep portable, packaged, simulated transport and real-device claims distinct.

## Dependencies, identities and licences

Preserve public identifiers, message-key numbers, compatible storage formats,
licences and attribution. Pinned vendor archives/checksums remain independent of
sibling checkouts. Do not repin consumers or change published bytes as cleanup.

## History

[Earlier maintainer notes](history/maintainer-notes-before-rework.md) retain the
full rationale/history. Read them only when investigating an old decision.
