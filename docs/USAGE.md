# Using Pebble Activities

## Publish an activity

```js
var summary = require('pebble-activities/summary');
var provider = summary.defineProvider({
  pluginUuid: OWN_PLUGIN_UUID,
  displayName: 'Delivery',
  storage: localStorage,
  readCurrent: function () {
    // Example content. Read your authoritative current source here.
    return [summary.standard('parcel-42', {
      name: 'Parcel',
      icon: 'delivery',
      headline: summary.text('Driver nearby'),
      detail: summary.text('Front door')
    })];
  }
});
Pebble.registerSourceHandler(provider.handleSource);
```

Use your installed plugin's UUID. Declare the provider's `sourceDeclaration`
in the plugin manifest: category `activity`, item `summary`, with
`summary.SOURCE_PROPERTIES`. The library manages the response metadata; plugins
author the content shown above. Keep one stable ID for the same ongoing item,
and return `[]` when nothing should be shown.

Choose the content that fits your source:

| Content | Publish |
| --- | --- |
| Message or status | `summary.standard(id, {headline: summary.text('Driver nearby')})` |
| Countdown | `summary.standard(id, {headline: summary.countdown({deadline: endUtcSeconds})})` |
| Elapsed time | `summary.standard(id, {headline: summary.elapsed({since: startUtcSeconds})})` |
| Measurement | `summary.standard(id, {headline: summary.value(6.2, 'mmol/L')})` |
| Music or media | `summary.media(id, {title: 'Song', artist: 'Artist', itemId: trackId})` |

Add optional `detail`, `name` or an icon when it contributes useful context.
Media can include `artwork`. A completed/cancelled record is hidden unless its
result is explicitly opted into; acknowledge a finished source by removing it
from the next complete response. Keep timestamps in UTC seconds.

For media, keep `itemId` stable while metadata or artwork arrives for the same
track, and change it for the next track. A host can then animate the track change
once while ordinary updates stay still.

An optional `openApp: {watchAppUuid: APP_UUID}` identifies an already installed
watchapp. It enables hosts such as Dynamic/Open Activity to open that whole app;
it does not select a particular message or timer inside it. Contextual `actions`
are separate capabilities for interactive hosts. Dynamic requests the app
destination and display data only.

The consuming app chooses priority and placement. In Dynamic, Primary uses the
larger bottom-aligned content block and Secondary is one static row above it.
Any source can occupy either role. Text starts at its beginning and truncates;
it never scrolls. Plugins do not choose layouts or primary/secondary positions.

Use `defineProvider` for a fresh authoritative read. A saved native timer or
cached owner snapshot uses `defineSnapshotProvider`; retain its original
observation, revision and validity instead of treating each poll as fresh data.
The [summary specification](../docs/SUMMARY-SPECIFICATION.md) covers the full API,
manifest, limits and snapshot adapter. The
[older activity API](../docs/ACTIVITY-SPECIFICATION.md) remains supported for existing
schema3 providers. Real-phone and physical-watch checks retain their separate
scope in [validation](../docs/VALIDATION.md).

## Package contents

| Part | Responsibility |
| --- | --- |
| [Simple activity API](../docs/ACTIVITY-SPECIFICATION.md) | Content, optional detail/image, app identity and lifecycle through `activity/live` schema 3 |
| Compatibility contracts | Advanced schema 2 and legacy schema 1 remain supported; ACT2 native transport stays internal |
| JavaScript publisher and provider | Accept native snapshots into shared phone-side storage, return revision receipts, and answer plugin reads |
| JavaScript consumer | Discover compatible providers, normalize their state and send a bounded projection through the host's queue |
| Portable C helpers | Validate atomic packets, track sessions and expiry, and calculate countdown or elapsed time |
| Optional compatibility adapter | Existing music/notification coordination, including privacy and notification baselines |

The package does not depend on Watchface Core. The host owns AppMessage dispatch,
SDK services, timers, persistence keys and rendering. Dynamic and another watchapp
can use separate instances of the same helpers while keeping their own UI.

Read-only display hosts can import `pebble-activities/host`. It supplies
`createActivities`, `createContext`, `selection`, `summary`, `summaryView`,
`activity`, `view` and `wire`, without loading `publisher.js`. The root import
continues to include all publisher/provider APIs for existing integrations.

## What the user installs

The library is bundled into each consuming app; it is not a separate watchapp or
background service. A provider plugin may ship alongside its native watchapp, as
[Timer](https://github.com/xefensor/pebble-app-timer) does, or in a plugin-only PBW. The phone app must support
Pebble plugins and have the preview enabled where that is required.

For the timer path, install Timer and a compatible consumer such as
Dynamic. Start a timer on the watch, then return to the watchface. The timer sends
its state through its own PKJS; its plugin later serves the saved snapshot to the
consumer. This is a phone-mediated handoff between otherwise separate apps.

The timer owns its alarm even when sharing fails. Without a phone connection, a
consumer may have no activity or an explicitly unconfirmed earlier countdown.
Reaching zero locally does not prove that the originating app completed or rang.

## Host and native integration

Use `createActivities({..., nativeFormat: 2})` with the host’s existing queue,
clock and SDK lifecycle. Discovery prefers `activity/live`, then the advanced
`activity/card`, then legacy `activity/session`, once per compatible provider.
`catalogue()` supplies validated internal views to host selection; plugins never
choose Dynamic’s priority or layout. Another host can keep its own order and UI.

`activity.toView()` compiles a simple record into the existing ACT2 transport.
The native packet is unchanged. Its mandatory field bookkeeping stays internal;
public activities contain no `main`, `support`, `meter` or layout properties.
The [simple source contract](../docs/ACTIVITY-SPECIFICATION.md) is the current
plugin authoring guide. [Schema 2 and ACT2](../docs/VIEW-SPECIFICATION.md) and
[schema 1/ACT1](../docs/SPECIFICATION.md) remain supported compatibility contracts.
Historical architecture/browser studies describe earlier design decisions and
do not add requirements to the simple API.

For native watchapps, `createPublisher` still accepts authoritative bridge
snapshots, validates revision floors and writes/reads back public shared state
before issuing receipts. `createProvider({presentation: 'simple', appName: 'Timer',
...})` exposes those saved snapshots as `activity/live`; existing session/card
sources remain available. No alarm, native storage or receipt ownership moves
to the consuming watchface.

`createContext` adapts standard Music and notification sources with their
existing privacy/baseline rules. Its transient Music activity now uses the
same simple model, without fabricated Track/Artist labels or a missing-artist
placeholder. Opt into `notificationAsActivity: true` to merge
`context.notificationActivity()` into the same ACT3 roles. It carries app identity,
sender/title, optional private body, app icon and the stock Notifications destination.
The initial phone shade remains a suppressed baseline. All opt-in privacy views
share one non-renewable eight-second arrival window; legacy context defaults keep
their three/eight-second policy. See the [bridge contract](../docs/VIEW-SPECIFICATION.md#optional-canonical-notification-activity-bridge-041)
for the baseline ACK gate, preferences and expiry-bearing event sidecar.
Native consumers include `pebble-activity-view.h`; these helpers register no SDK
services and allocate no host UI. See the specification for exact failure rules.

### Multiple native timers

A provider that owns several independent records uses
`createPublisher({storage: localStorage, pluginUuid: UUID, maxRecords: 8})`.
Include `ACTIVITY_SLOT` (0–7) in each native snapshot, or `slot` when calling
`accept` directly. The host owns those stable slots; run IDs remain the public
identity. A new run replaces only the previous run in the same slot. Missing
slot means zero, preserving the original single-record path.

Each accepted update advances a **source-wide** revision, even when updating
another slot. A native resync obtains `lastRevision()` and republishes its slots
with distinct higher revisions. The read-only provider loads all slots without
an extra option. A consumer may still project only its best two activities to
the watch; the host chooses that presentation policy.

## Boundaries

- This convention is our public contract, not an official Pebble activity standard.
- Existing timer and workout apps need an explicit integration; discovery cannot
  access another watchapp's private memory or storage.
- The built-in Workout app's live manual session is not exposed by the current
  public SDK. This stock implementation does not claim to provide that session.
- Fully watch-local sharing and Health-style cross-app compositor transitions
  require additional OS support. No firmware or phone-app fork is used here.
- Private music and notification content is transient and is not persisted by
  these consumer helpers. The reference publisher is a bounded, non-private timer
  handoff, not a persistent cache for private messages or medical readings.
