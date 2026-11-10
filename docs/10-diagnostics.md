# Installation and startup diagnosis

## Installation order

The corrected transfer installer verifies file checksums, checks Windows x64/build requirements, rejects a conflicting noncompatibility Minecraft registration, trusts the expected public certificate if necessary, registers the APPX/frameworks, then adds loopback. The initial order attempted loopback before package registration and returned an unhelpful parent error on a fresh reinstall.

Only the public CER is transferred. Local signing keys remain non-exportable. The per-package loopback exemption is required for an AppContainer client to contact local helpers; it is not a reason to disable the firewall globally.

Install-Trust accepts Certificate or Loopback phases and saves phase-specific failures. Install.ps1 invokes Collect-Diagnostics with InstallCheck after installation and also attempts collection after an error. “Installed” should follow verification, not just a process starting.

## What the collector checks

- OS caption, version, numeric build and architecture.
- Current-user package registration, status and revision.
- Minecraft.Windows.exe, launcher EXE, XINPUTATV.dll and manifest existence/hashes.
- Launcher/App manifest entries.
- x64 VCLibs and Store Engagement minimum versions.
- Xbox app, Store and Gaming Services installed versions.
- TokenBroker, XblAuthManager, XblGameSave and XboxNetApiSvc state.
- 32-bit and 64-bit legacy identity metadata field availability and ID equality.
- Named loopback exemption.
- Game/launcher process presence and whether native XINPUTATV.dll appears loaded.
- Listener owners on expected ports and game-process loopback connections.
- Presence/mtime and aggregate signing count from raw logs, without copying raw contents.
- New structured startup logs from either packaged or ordinary LocalAppData locations.

Stopped on-demand services are observations, not automatic proof of failure. Similarly, closed ports after an early account rejection are expected. A copied collector should run as the same Windows user who launches the game.

## Structured startup events

startup_diagnostics rotates startup.jsonl at 1 MiB, keeping startup.previous.jsonl. It records timestamp/PID and explicit fields, not arbitrary exceptions or raw URLs.

Expected stages include packaged_launcher_bootstrap, launcher_started, account_preflight, session_cache_checked, interactive_authentication_started/completed, bridge_listeners_ready, adapters_ready, game_launch_requested, game_activation_dispatched and game_process_observed. A signing observation establishes a bridge request occurred, but may include a launcher probe; do not attribute it to game traffic without process/native evidence.

identity_read_failed_Gamertag with Windows error 2 means the legacy value is missing. The .211 failing report showed ID presence true, matching Windows accounts true, name presence false, no bridge, and verdict unverified. .212 fixes precisely that decision.

## Paths

Typically:
```
%LOCALAPPDATA%\Packages\Microsoft.MinecraftUWP_8wekyb3d8bbwe\LocalCache\Local\MinecraftAppleTV\Diagnostics\startup.jsonl
```

The collector also searches:
```
%LOCALAPPDATA%\MinecraftAppleTV\Diagnostics\startup.jsonl
```

Installer reports sit beside Install.cmd in Install-Diagnostics-<timestamp>. Manual collection creates Minecraft-AppleTV-Diagnostics-<timestamp> on Desktop. Patcher build logs are under LOCALAPPDATA/MinecraftAppleTVBuilder/Logs.

Do not confuse these sanitized startup events with legacy requests.log. That raw log can contain identifiers, URLs and detailed error text. Historical inventory output named “sanitized” is also not necessarily safe to share.

## Troubleshooting decision tree

1. No launcher process/bootstrap event: verify Start menu targets Launcher, installed files, package status and OS/runtime prerequisites. Check Windows deployment/security logs locally; don't collect unrelated machine logs indiscriminately.
2. Bootstrap but no launcher_started: investigate import/startup exceptions and frozen payload completeness.
3. Preflight unverified: identify missing IDs, read errors or missing display-only fields. In .212 a name alone must not block.
4. windows_mismatch: ask the user to align actual accounts; do not rewrite IDs.
5. reauth: expect human device-code flow. If no prompt, inspect progress/browser handoff exceptions without logging codes/tokens.
6. Auth complete but no listeners: inspect binding conflicts, exception type and actual port owner.
7. Listeners but no native module/game: confirm activation target and package registration.
8. Store no wallet/details: distinguish cached state, session expiry, modern service failure and native callback completion.
9. Payment pending: inspect durable recovery and receipt state; do not buy again as a diagnostic.
