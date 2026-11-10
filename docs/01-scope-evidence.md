# Scope, evidence and qualifications

## Baseline

The executable is the Windows x64 Minecraft 1.1.5.0 engine, adapted to Apple TV title identity and presentation. This is not recompilation of the Apple ARM64 engine. The decrypted Apple input supplies research identity/artwork; the Windows input supplies executable and ordinary assets. Package revision .212 identifies the latest launcher/account fix; it does not mean a newer engine.

We built the system during October–November 2026. Service responses, product availability and undocumented request shapes may change after the recorded observations. Upstream commit 9ed87e0 is the reproducible source anchor. Dates refer to the development record; raw personal captures are deliberately excluded.

## Evidence levels

- **Source-inspected:** a behavior is present in the pinned source. This alone does not prove that a particular branch executed on a live service.
- **Offline-tested:** deterministic assertions passed with synthetic input/mock dependencies.
- **Developer-machine live:** the project was exercised against actual installed Windows/Minecraft/service state on the development PC.
- **User-confirmed:** the human performing gameplay, payment or another-PC testing reported the outcome.
- **Unresolved/hypothesis:** plausible explanation without sufficient confirming evidence.

These levels are not interchangeable. The original work often combined native tracing, service responses and a user's visible result. We no longer have a publishable complete raw capture set. The claims ledger points to source and summarizes the observed result, with limits.

## Confirmed milestones

1. Apple TV XSTS identity was acquired and used in the old client while retaining native Windows account handling. In-game achievements and presence were observed under Apple TV identity.
2. Multiple distinct catalog offers loaded without the earlier callback crash. Repeated Store entry and item switching were exercised.
3. Modern ownership/wallet data fed the old UI. Free acquisition was confirmed through subsequent inventory reads. The completion chime was audibly confirmed by the user.
4. One specifically authorized 160-Minecoin item purchase reduced balance by the expected amount and created ownership.
5. A previously pending 320-Minecoin purchase was credited by the official Windows client during investigation. The bridge then implemented the observed restore flow. A subsequent user-approved 320-Minecoin checkout was credited by the bridge on the first observed Windows redemption attempt. These are different tests; do not describe the first as bridge-delivered.
6. Five top-up cards were exposed and offline-tested for routing/recovery. Only the smallest real-money package was purchased in live testing.
7. Fresh installation failed because the transfer installer attempted named loopback configuration before registration. Reordered installation succeeded on the development PC; this is not a broad Windows-matrix certification.
8. On an affected second PC, all install checks passed and stable account IDs matched, but the Gamertag value was absent. Startup diagnostics showed preflight rejection. .212 removed only that optional-name requirement; the user confirmed the previously failing account then worked.

## Boundaries

- Catalog coverage is what the seed and dynamically resolved entries contain, not every current Marketplace listing.
- There is no general verified modern-pack compatibility scanner in this release. Most items are classified unknown and blocked for download; unknown displays as Incompatible.
- A free incompatible item may still be claimed; account ownership is independent of local engine support.
- Create World must not show arbitrary catalog entries as usable templates. Filtering and manifest validity matter independently of Store visibility.
- Marketplace availability, authenticated entitlement access, content download, local pack parsing, and actually loading a world are different proof obligations.
- Account detection uses legacy registry metadata, not a universal authoritative API for the current Xbox app UI. .212 fixes a known missing-name case, not all staleness scenarios.
- Long-session automatic token renewal is deferred.
- LAN was reported working. Xbox invite joining produced a friends-related error despite mutual legacy friendship; reverse-direction diagnosis was deferred. Do not label online multiplayer fixed.
- Realms are unavailable.
- A custom Marketplace is an engineering application of these findings, not an already tested replacement service.
