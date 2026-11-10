# Verification and test matrix

## Offline acceptance

tools/run_checks.py runs tests against reference account/wallet/redemption logic and the synthetic provider. It blocks network calls and redirects runtime state to a temporary directory. All receipt, identity, currency and key values used by recovery tests are fabricated. The runner must fail if a supposedly offline path attempts a connection.

tools/verify_reference.py recomputes all reference hashes and confirms the source map is tied to upstream.lock.json. It does not contact Xbox or prove external services are still compatible.

The recovery tests were carried forward from development with mocked Marketplace/redemption. They test cancellation, account changes, receipt/product mismatches, successful expected credit, uncertain delivery, duplicate suppression, bounded retry state, and official request shape. This is stronger evidence than merely importing the modules, but weaker than a new real transaction.

## Live matrix

| Area | Action | Evidence to retain | Negative case |
|---|---|---|---|
| Install | fresh install, same-user update | package version/status, file hashes, loopback | missing framework, conflicting package |
| Preflight | matched Windows IDs | field availability/equality | missing IDs; names missing should still pass |
| Bridge identity | correct/incorrect XUID | verdict and auth stages | stale different-account bridge |
| Native load | launch through Launcher | module loaded, game process | direct App bypass |
| Catalog | open, switch, close, reopen | distinct UUID/offer counts | same image requested twice |
| Detail | gallery and subviews | expected/loaded image count | unavailable image, delisted pack |
| Wallet | first Store entry | fresh inventory vs header | unavailable inventory must not become zero |
| Free claim | authorized zero-price offer | ownership observed, unchanged balance | missing price, coming soon, changed price |
| Paid item | exact authorized item/amount | ownership and exact debit | duplicate click, expired permit |
| Coin top-up | smallest explicitly approved pack | native result, restore, exact credit, cleanup | cancellation is not success |
| Recovery | restart after uncertainty | account/receipt/attempt-bound state | no blind replay or new charge |
| Long session | remain active across expiry | request/auth/achievement behavior | renewal is not implemented |
| Custom content | install your test pack | hashes, manifest, actual game load | catalog visibility alone insufficient |

Use separate human approval for every paid test. Existing history is not future authorization. Never deliberately produce duplicate financial side effects to test idempotency against a live account; use mocks first.

## Evidence format

Record source commit, package revision, engine hash, Windows build, reproduction steps, sanitized stage sequence, expectation, actual result and unresolved alternatives. A useful failure report says “metadata has XUID but Gamertag value is absent; preflight rejected before auth,” not merely “sign-in broken.”

For native failures record module-relative addresses and hook version rather than publishing raw process addresses or entire dumps. Keep private traces local, extract only the fields necessary to establish the claim, and make the extraction reproducible where possible.

## Current limits

The user confirmed .212 resolves the missing-Gamertag account case. That does not retest every Store route, the three gameplay achievements, long-session renewal, larger-pack payment or online invite multiplayer. The newest diagnostic additions passed build/source tests; source code and assertions do not certify all future Windows versions.

The initial 320-credit recovery through an official client and the later bridge-delivered test must remain separate evidence rows. Likewise, a Windows price probe for another region is not an actual purchase there.

## Optional GitHub Actions

examples/github-actions/research-checks.yml is a CI template for the same offline checks. It is not an active workflow in this repository. A maintainer with workflow permission can copy it into .github/workflows/. The publishing OAuth credential did not have that permission; no account permissions were changed.
