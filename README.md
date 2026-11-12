# Pebble Activities

An embedded library and provider convention for semantic ongoing activities on stock PebbleOS.

## Download

[Version 0.4.4](https://github.com/xefensor/pebble-lib-activities/releases/tag/v0.4.4) is a development prerelease.

[package](https://github.com/xefensor/pebble-lib-activities/releases/download/v0.4.4/pebble-activities-0.4.4.tgz),
[SDK archive](https://github.com/xefensor/pebble-lib-activities/releases/download/v0.4.4/dist.zip), and
[checksums](https://github.com/xefensor/pebble-lib-activities/releases/download/v0.4.4/SHA256SUMS.txt).

Package name: `pebble-activities`. This library is bundled by a host app; it is not installed on
the watch separately.

Download the package into your project’s `vendor/` directory, then pin it locally:

```sh
npm install --save-exact ./vendor/pebble-activities-0.4.4.tgz
```

Commit the lockfile and upstream checksum/provenance record. Consumer upgrades are independent.

```js
var summary = require('pebble-activities/summary');
```

Use schema 4 summaries for new providers and the explicit ACT3 native profile. [Provider and
host usage](docs/USAGE.md) · [Summary specification](docs/SUMMARY-SPECIFICATION.md). Providers
own source truth; consumers own placement and presentation. Schema 1–4 and ACT1–3 remain
compatible.

## Compatibility

The development SDK targets are **Emery / Time 2, Flint / Pebble 2 Duo and Gabbro / Round 2**, using **Pebble SDK 4.44**.

## Version 0.4.4

- Retry failed source bindings during configuration and periodic discovery while

## Development

Use Node 22, Python 3.12 and a C compiler. SDK builds additionally need Pebble SDK 4.33.1 on
PATH.

```sh
npm ci --ignore-scripts
npm test
npm run build
npm run pack:candidate
```

[Contributor guide](CONTRIBUTING.md) · [Release preparation](docs/RELEASING.md) · [History index](docs/history/index.md).
Development outputs belong in ignored `build/`; published archives stay frozen.

## Licence

[PolyForm Noncommercial 1.0.0](LICENSE). Preserve bundled third-party notices and attribution.

## Version 0.4.5

Builds the unchanged ACT1–3 / schema 1–4 runtime for Emery, Flint and Gabbro with SDK 4.44. Public APIs, leases, identities and owner authority are unchanged.

This is local release preparation; published downloads above remain frozen.
