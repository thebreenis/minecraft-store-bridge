# Native integration and UI research

## Load path

The engine import name XINPUTUAP.dll is changed to the same-length private XINPUTATV.dll. The proxy forwards XInputGetState to the actual system implementation and installs the compatibility hooks. Controller support is not meant to be replaced. Exact engine patch bytes live in upstream Source/Backend/Patches.json.

The native source includes wallet/catalog hooks, Store ownership/UI logic, checkout, presence filtering and achievement support. They share a private namespace and are not drop-in independent libraries. Build with the pinned upstream toolchain rather than compiling one header alone.

## Important RVA anchors

These values belong only to the pinned Windows x64 1.1.5 engine; they are relative to module base, not absolute addresses.

| Anchor | RVA |
|---|---|
| XSAPI auth helper | 0xE42AF0 |
| Wallet load | 0x672E60 |
| Wallet parse | 0x6A3010 |
| Catalog execute | 0x60D320 |
| Catalog parse | 0x60ECC0 |
| Catalog notify | 0x60E9A0 |
| Catalog init | 0x6C7AA0 |
| Catalog select | 0x6C91D0 |
| Catalog manifest apply | 0x6C9470 |
| Thumbnail callback | 0x6C8C40 |
| Native string assign | 0xDC860 |
| String-map find | 0xDEC30 |

The generated source map lists the rest. Validate current source and expected prologue bytes; these tables are navigation aids, not a safe generic hooking recipe.

## Lifecycle bugs and resolved observations

### Query callback versus standalone callback

The query callback's offer pointer is at capture+0x58; standalone uses +0x50. The wrong field looked like repeated offer-pointer reuse. That led to an early overbroad cache theory. Correct object-layout identification mattered more than forcing additional instances.

The current code identifies the query callback using its vtable entry and routes to the proper offset. Offsets depend on the exact lambda wrapper and compiler layout.

### Owning asynchronous callbacks

Queued thumbnail callbacks must hold native clones with the correct vtable and destroy them correctly. Holding a borrowed pointer across a worker lifetime is not equivalent. The code clones through the native virtual function and stores the returned wrapper before queueing.

### One completion per request

Caching by image URL and suppressing duplicate completion strands newly opened queries. Reopening Store may request the same URL with a different pending counter. Every request must complete even if byte/image data are cached.

### Catalog notification scheduling

A worker notification after the original native task had already notified an empty result caused duplicate completion and task-queue corruption. The .121-style correction populates synchronously in Execute and lets the existing scheduler notify once. Do not call the original continuation twice to make a spinner disappear.

## Presentation bindings

store_ui.h replaces scoped action-label/enabled/description bindings and routes selected offers. It maintains owned/free/compatibility/pending/failure/completion-sound state per UUID. The native label is a projection of that state; it does not grant a license.

Action priority is significant: pending/done wait; guarded paid-test exception; coming-soon/unavailable; unowned verified-free; incompatible/unknown; owned compatible download. An owned incompatible offer shows a disabled Incompatible action, with Owned in supporting text. Unknown is deliberately displayed as Incompatible, though the underlying state remains U.

The progress popup has its own binding for Please Wait... / Done!. The actual action button stays Please Wait... while completion UI resolves; Done! should not leak into the purchase button. The native sound is triggered after inventory-confirmed success, and the popup remains until completion timing resolves. The user confirmed hearing the sound; a successful function call alone would not prove audio was heard.

Preview loading tracks expected screenshot count versus native loaded image entries, with a 30-second cap. This avoids indefinite progress for an incomplete gallery but is not a general timeout policy for every native screen.

## Visual corrections

- Use real detail screenshots and the native carousel lifecycle rather than placeholders.
- Normalize problematic title punctuation that triggered fallback glyph sizing.
- Match account picture/name/wallet spacing between Store and Minecoin screens.
- The Minecoin back action mirrors the existing text navigation style.
- Display platform-formatted top-up prices instead of screenshot prices.
- Do not add a closing “tick” merely for these Store dialogs: the user requested removal to match the rest of this build.
- World/mash-up subviews need the same purchase/compatibility policy as top-level detail; a stale native unlock button is not an acceptable bypass.

## Native testing discipline

Take a hash-identified baseline; attach read-only observers first; record callback entry/exit and owner lifetime; reproduce once; then make the narrowest hook. Distinguish CPU work from network waits and music continuing from a responsive UI. A visibly frozen screen with audio does not prove a network timeout. Keep async work off UI-thread paths except for APIs that explicitly require UI-thread invocation.
