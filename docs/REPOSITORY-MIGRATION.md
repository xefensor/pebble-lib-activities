# XOCE repository migration

The repository naming convention is `pebble-<type>-<name>`, under the XOCE
(Xef's Open Computing Ecosystem) umbrella.

| Identity | Value |
| --- | --- |
| Former repository | `xefensor/pebble-activities` |
| Repository destination | [`xefensor/pebble-lib-activities`](https://github.com/xefensor/pebble-lib-activities) |
| Public package and import name | `pebble-activities` |
| Current published version | `0.4.4` |
| Frozen artifact source | `df4f30f4a66419ce835959eeeec6de7999704fa0` |

This is a repository and documentation migration. Public JavaScript exports,
C includes, source contracts, wire formats and runtime behaviour are unchanged.
Consumer `file:` dependencies, version pins and archive checksums stay the same.
Maintained consumer provenance can point its repository field at the new
destination while retaining the original source commit and archive identity.

Published tags, SDK archives and package tarballs retain their original source
and bytes. Embedded package metadata or documentation in those historical
archives may still name the former repository. The current README supplies the
maintained download links. Changing published package bytes requires a new
version; do not rebuild 0.4.4 to update an embedded URL.

The release configuration publishes to the new repository and bootstraps the
original tested 0.4.4 source. Future versions use their own artifact commits.
Historical QA records remain evidence of their original checks.

## Migration verification

On 2026-11-06, `npm test` passed 195 JavaScript tests and the portable native
suites; the release-helper suite passed 19 tests. All 15 tracked release files,
including `dist.zip`, were compared with the pre-migration commit and
retained their original bytes. These are local automated checks, not a new
phone or physical-watch validation.
