# Pebble Activities maintainer instructions

## Scope

Work on the existing stock-PebbleOS implementation; preserve accepted behaviour and public compatibility.
Read [CONTRIBUTING](CONTRIBUTING.md) for setup, output locations and commit/release policy.
Older packages, QA records and source archives remain frozen. Hosts and consumer
pins are independent; history is not a second active specification.

## Important boundaries

This is a stock-PebbleOS library/convention, not an official standard or background service. Preserve schema1/2/3/4 and ACT1/2/3 compatibility and the public root API. Native owner state/alarms remain authoritative; receipt is acceptance, not a disk-flush/alarm guarantee. Preserve source/run identity and original observation/validity across polls and reconnects. Zero is not completion. Discovery validates returned UUIDs, versions, permissions and removal. Private media/notification content stays transient.

## Read only what the task needs

- Ownership, storage, source lifecycle, privacy or capabilities:
  [current maintenance contracts](docs/MAINTENANCE.md).
- Public API or wire changes: [host/provider contract](docs/SUMMARY-SPECIFICATION.md) and existing cross-language fixtures.
- Versioning, archives, tags, upload or deployment: [release boundary](docs/RELEASING.md).

## Work and verification

Respect research/review versus implementation scope. Preserve established user
choices; clarify materially different interpretations before changing direction.
Run relevant required checks. Tests alone do not judge visual quality. Keep
source/portable tests, packaged execution, native emulator and real-device
verification distinct. Use disposable development evidence; do not overwrite
historical proof or relabel it as fresh.

`npm test` runs portable source tests and workflow guards. `npm run build`
creates a disposable candidate; it must not replace frozen dist/release files.
Do not bump versions or create release archives for routine edits. Never push,
publish or deploy as an implicit part of testing. Keep instructions current;
put superseded decisions in [history](docs/history/maintainer-notes-before-rework.md).
