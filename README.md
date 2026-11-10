# Minecraft Store Bridge research

A source-backed research record of connecting the modern Minecraft Marketplace to the **Windows x64 Minecraft 1.1.5.0 engine**, presented as Minecraft: Apple TV Edition. This is the research behind the [Apple TV compatibility patcher](https://github.com/thebreenis/minecraft-apple-tv-edition-x64), pinned to commit `9ed87e050c40f9683248e7fe9a79789ea5244e08` (patcher **1.0.2**, package **1.1.500.212**).

**Start with the offline checks.** They do not sign in, purchase, redeem, or install anything.

```powershell
python -m pip install requests==2.34.2 cryptography==50.0.2
python tools/run_checks.py
python tools/verify_reference.py
python examples/offline_marketplace.py --demo
```

Python 3.11+ is required for the Python research tools. Building the actual Windows package requires the upstream Windows toolchain and the user's original game inputs. See [reproduction](docs/02-reproduction.md). The standard-library example can run without installing dependencies.

## What this research establishes

The tested project displays translated catalogs, images and item details; uses server-confirmed ownership and wallet balances; claims verified-free offers; supports a narrowly guarded Minecoin-spending test; and uses native Microsoft Store checkout plus observed Minecraft delivery protocols for Minecoin top-ups. The smallest real-money package was tested end-to-end. Account switching, startup diagnostics, and a missing-Gamertag startup defect were tested and repaired.

It does **not** establish that every Marketplace item can run on 1.1.5, that all pack sizes/regions were purchased, that every old Minecraft build uses these offsets, or that an arbitrary custom Marketplace can use Microsoft's commerce infrastructure. Realms remain unavailable; online invite joining remains unresolved in this project's evidence. Modern content conversion and decryption are not provided.

## Read the research

| Document | Purpose |
|---|---|
| [01 Scope and evidence](docs/01-scope-evidence.md) | What was observed, what is inferred, what remains unverified |
| [02 Reproduction](docs/02-reproduction.md) | Exact inputs, source revision, environment, build and staged live verification |
| [03 Architecture](docs/03-architecture.md) | Process boundaries, ports, cache/state lifetime and sequence |
| [04 Authentication and accounts](docs/04-authentication.md) | Token chain, native account preservation, matching and .212 fix |
| [05 Local protocols](docs/05-local-protocols.md) | Wire framing, operation tables, bounds and error handling |
| [06 Catalog translation](docs/06-catalog.md) | Modern-to-legacy schema, rows, identifiers, images and skin routes |
| [07 Native hooks and UI](docs/07-native-hooks.md) | Exact-build offsets, lifecycle failures and rendering fixes |
| [08 Ownership and compatibility](docs/08-ownership-compatibility.md) | Separate state dimensions, conservative action policy, limitations |
| [09 Commerce and redemption](docs/09-commerce.md) | Free claims, Minecoin spending, Store checkout, delivery and recovery |
| [10 Diagnostics and installation](docs/10-diagnostics.md) | Installation order, startup stages and troubleshooting |
| [11 Custom Marketplace design](docs/11-custom-marketplace.md) | A concrete independent-provider design and offline reference example |
| [12 Verification matrix](docs/12-verification.md) | Reproducible tests, acceptance evidence and negative cases |
| [13 Failure history](docs/13-failure-history.md) | Failed approaches and why not to repeat them |
| [14 Security and publication](docs/14-security.md) | Trust boundaries, secrets, content rights and deployment gaps |
| [15 Source map](docs/15-source-map.md) | Generated Python symbol and native constant index |
| [16 External references](docs/16-references.md) | Official platform docs versus observed private contracts |
| [17 Codex research playbook](docs/17-research-playbook.md) | Bounded task prompts for verification, custom providers and porting |

## Files and provenance

- `reference/runtime/`, `reference/native/`, `reference/installer/`: byte-for-byte original project source at the pinned commit. This is an archival implementation, not a newly hardened SDK. Some historical CLI entry points write account inventory to disk; read [security](docs/14-security.md) before running them.
- `evidence/reference-manifest.json`: each included source path, upstream path and SHA-256.
- `evidence/claims.json`: claim/status/source ledger. Sanitized narrative observations are not raw server traffic.
- `tests/`: offline regression tests; commerce dependencies are mocked, networking blocked by the test runner.
- `examples/`, `fixtures/`: original synthetic catalog/provider demonstration, no Microsoft credentials or game assets.
- `tools/`: offline verification and explicit source acquisition.
- `upstream.lock.json`: pinned full reconstruction repository and original archive hashes.

No full game, paid pack, signed receipt, session token, private certificate, real account inventory, or user profile is distributed here. Public identifiers are configuration, not credentials. Historical raw traces were not retained as distributable evidence; do not mistake a summary for a packet capture.

## For Codex and other coding agents

Read [AGENTS.md](AGENTS.md), then the evidence ledger and reproduction guide. Run offline checks first. Use the pinned source as the implementation authority. Do not run authentication, checkout, redemption, account changes, installation or publishing merely because these operations appear in reference code.

The useful outcome for a new provider is a catalog/entitlement/compatibility adapter with its own identity and content delivery. The [offline example](examples/offline_marketplace.py) provides a small executable starting point, **not** a finished replacement Marketplace.

## License

Original project code and new research/example code are under [MIT](LICENSE). Minecraft, Microsoft services/frameworks and other third-party material retain their own ownership and licenses. Requiring user-supplied game inputs is a distribution boundary, not an assurance of publisher approval.
