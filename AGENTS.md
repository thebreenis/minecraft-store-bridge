# Research agent working instructions

1. Read README.md and docs/01-scope-evidence.md before interpreting results.
2. The implementation baseline is upstream.lock.json. Verify reference hashes with tools/verify_reference.py. Do not silently update the baseline to latest.
3. Run tools/run_checks.py before changes and after relevant changes. It prevents real HTTP/network operations and uses temporary journals. Test success is not proof of live service success.
4. Reference source is archival. Put experiments in examples/, tools/, or a separate working checkout. If changing reference/, record the divergence and update provenance deliberately.
5. Never substitute display names for account IDs. Missing Gamertag metadata is not missing identity.
6. Keep ownership, compatibility, downloadability, and payment delivery distinct. A displayed price or HTTP 200 is not entitlement/credit proof.
7. Do not initiate sign-in, free claims, paid purchase, redemption retries, account switching, installs, game closure, or external publishing without an explicit user request covering that action. For payment tests require the exact product/amount/account and inspect previous pending transactions first.
8. Never clear a journal or acknowledge a Store consumable to make a test pass. Do not fabricate ownership, receipts, currency, or game achievement events.
9. Do not publish raw auth/request logs, account inventory, profile data, private keys, game binaries or paid assets. Structured diagnostics may still disclose a Gamertag; review before sharing.
10. Native offsets are only valid for the pinned x64 engine. Validate hashes, calling convention, object lifetime and expected instruction bytes before another-build port.
11. Report evidence level explicitly: source-inspected, offline-tested, developer-machine live, affected-user confirmed, hypothesis, unresolved.
12. A custom provider must own/license its content and use its own entitlement authority. Do not route independent paid offers through Microsoft product IDs.
13. Preserve existing Xbox sessions unless the user authorizes a change. Never retry a payment to investigate uncertain delivery.
