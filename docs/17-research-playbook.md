# Suggested Codex research sessions

These task descriptions are intentionally bounded. They let a reader verify specific claims without giving an agent a vague instruction to make all services work.

## Session 1: map the system offline

Ask: “Read AGENTS.md. Verify the reference manifest and run offline tests. Explain the call chain from the native Store action to the Python entitlement request, citing functions. Do not contact external services.”

Expected result: source-hash verification, test summary, links to StoreActionEnabled/ClaimStoreFree, QueryStoreUi, Handler.handle, claim, Marketplace.detail/inventory. A correct explanation distinguishes a presentation binding from authority to grant an entitlement.

## Session 2: reproduce the missing-name defect

Ask: “Use synthetic Accounts instances and mocked registry reads to show .211's rejected condition and .212's corrected decision. Preserve all stable-ID and bridge-XUID checks.”

Inputs: matching account IDs, present XUID, absent display name. Expected: reauth without a bridge; ready with matching bridge XUID; reauth with another bridge XUID; windows_mismatch when Windows account IDs differ. Do not edit the real registry.

## Session 3: validate cancellation recovery

Ask: “Trace PRP3, REC1, CAN2 and TOP2 through the journal. Run mocked tests proving a stale cancel cannot cancel a new attempt, and an empty pending list cannot prove a completed payment.”

Expected: attempt UUID carried across callbacks, prepared state preserved during checkout-open, canceled state only after no-payment evidence, no redemption calls in cancellation-only tests. Do not invoke Store APIs.

## Session 4: build a custom free catalog

Ask: “Extend the synthetic catalog with two original free items and a declared incompatible bundle. Add tests for IDs, categories, gallery metadata and action state. Do not fetch official assets or alter reference code.”

Expected: stable synthetic IDs; free claims independent of compatibility; unknown/incompatible download disabled; deterministic catalog output. Next steps may add your own assets and pack validation, but this session does not prove native integration.

## Session 5: reproduce the Windows package

Ask: “Read the exact input hashes and build guide. Verify my supplied archive hashes, build from the pinned source using build-only mode, and produce the validation report. Do not install, sign into an account or publish a full game package.”

The operator supplies originals. A mismatch should stop before reconstruction. If the toolchain is absent, report what is missing; do not download an arbitrary game copy. A build creates a local signing key as documented; public certificate and logs stay in local build output.

## Session 6: authorized live observation

Only after the operator explicitly asks for it: collect a preflight report, launch the installed game, and record sanitized stages. The operator handles device-code sign-in and any payment UI. Start with catalog/detail/wallet reads; do not infer authority to claim or buy from “test Store.”

For a live transaction, write down the exact offer/product, account, amount, current pending state and success criteria before the operator confirms. If delivery is uncertain, stop new checkout and reconcile that attempt. Never erase uncertainty from the journal.

## Session 7: port one native hook

Ask: “For this separately supplied executable hash, identify the catalog execute/notify path through read-only disassembly. Compare object layout and continuation ownership. Do not install hooks yet.”

Expected: provenance and ABI notes; no copied RVAs without verification. A later narrow experiment should change one hook and preserve rollback/source evidence. Generalize only after a repeatable test on the new binary.

## What to ask contributors to submit

A source commit, offline test result, exact engine/package hashes, Windows build, sanitized stage evidence, steps, and clear evidence classification. For native changes add expected original bytes, function ABI/lifetime assumptions and rollback instructions. For provider changes add schema examples and failure tests. No raw auth captures or paid-content archives.
