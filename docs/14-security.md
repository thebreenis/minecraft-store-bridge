# Security, data handling and publication boundaries

## Archival implementation, not a hardened public service

The reference bridge is designed for a user's trusted desktop session. It returns tokens/signatures over unauthenticated loopback and accepts URLs from a local caller. Binding to 127.0.0.1 prevents ordinary remote access; it does not protect against another process/user able to connect locally. Do not expose these ports on a LAN, forward them, or put them behind an internet proxy.

A hardened successor needs OS-bound IPC authorization, request allowlists, maximum frame/body sizes, strict error framing, clear cancellation, secret zeroization/lifetimes and careful separation of signing from presentation services. Local auth helpers must not become a generic credential oracle.

## Known source limitations to review

- ATVB1 error response shape differs from normal seven-field success shape.
- Some historical CLI/probe paths print service responses or write complete inventory/transaction JSON.
- The file name live-inventory-sanitized.json does not guarantee anonymization.
- requests.log contains raw method/URL records and may carry account-sensitive values.
- Gallery URL sidecars have syntax checking but no comprehensive remote-host allowlist or decompressed image bounds.
- Detail cache invalidation is simple; stale metadata must never authorize a transaction.
- Account-matching registry metadata can lag actual app UI.
- Automatic auth renewal is not implemented.
- Top-up balance-delta confirmation assumes no unrelated concurrent wallet activity.

These are documented limitations, not claims of newly audited exploitability. Do not silently “fix” the archival snapshot without maintaining a separate provenance record.

## State that must stay private

Do not commit auth-session.bin, proof keys, device codes, Microsoft/Xbox/PlayFab/franchise tokens, Store publisher/native keys, raw receipts, account inventory, pending transaction journals, account-specific acquisition permits, world saves, full process dumps or installed profile folders. DPAPI ciphertext still belongs to the user and is not appropriate for a redistribution.

The structured diagnostic collector deliberately copies only bounded new startup logs, not raw auth/request logs. It can include a Gamertag and process/version metadata; get consent to share those reports and review them.

## Publication contents

This repository includes original source, synthetic fixtures, public service/product identifiers, exact game-input hashes and documentation. It excludes original game packages, decrypted Apple executables, paid content, screenshots/artwork, runtime frameworks/binaries, private signing keys and personal captures.

The pinned upstream patcher repository contains its separately documented build recipe and framework dependencies; users obtain original game inputs themselves. Fetching that source is explicit and does not run it.

## Custom provider rights and authority

A custom catalog may describe original or properly licensed content. It cannot grant Microsoft's purchased entitlements by editing a local Owned field, mint Minecoins, or sell independent goods using official Store IDs. If it offers its own paid currency, name and account for it distinctly and use its own payment/entitlement authority. This repository documents actual integration, not a license to operate Microsoft's commerce endpoints as a general public API.

## Testing discipline

Offline checks block networking by default. Live tests need an operator's account and an explicit action scope. Free claims still modify account inventory; redemption still mutates transaction state even when no new payment occurs. A prior failed checkout is a recovery task, not authorization for another purchase.
