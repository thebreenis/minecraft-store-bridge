# Sources and external documentation

## Primary implementation

- [Pinned project source](https://github.com/thebreenis/minecraft-apple-tv-edition-x64/tree/9ed87e050c40f9683248e7fe9a79789ea5244e08)
- [Published patcher 1.0.2](https://github.com/thebreenis/minecraft-apple-tv-edition-x64/releases/tag/v1.0.2)
- [Original Xbox Live API reference source](https://github.com/microsoft/xbox-live-api/tree/798bf03b07a3a2bfef2db544e3dd91cb4ce582eb), used during historical SDK comparison.

The reference-manifest maps every archived source file back to the exact pinned project path and SHA-256. Use docs/15-source-map.md for functions/constants.

## Official Windows documentation

Checked 2026-11-10:
- [StoreContext](https://learn.microsoft.com/en-us/uwp/api/windows.services.store.storecontext): platform checkout, product queries and customer Store key APIs. Its documented checkout constraints include UI-thread invocation and no elevated in-app purchasing.
- [UWP firewall/loopback troubleshooting](https://learn.microsoft.com/en-us/windows/security/operating-system-security/network-security/windows-firewall/troubleshooting-uwp-firewall): AppContainer loopback exemptions and diagnostic context.

These pages support the Windows platform concepts, not the private Minecraft service schemas. The Minecraft franchise/entitlement request forms in this repository were inferred from implementation and official-client observations during the project; they are not promised public interfaces.

## Evidence that is not distributed

Personal raw traces, successful tokens, receipts, inventories and gameplay recordings are not included. User/developer live outcomes are summarized in evidence/claims.json and the validation documentation. They can be reproduced only with appropriate original game inputs, compatible environment, service availability and an explicitly authorized account operation. Offline tests validate contracts/state transitions, not current Microsoft service acceptance.
