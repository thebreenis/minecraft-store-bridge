# Commerce, platform checkout and Minecoin delivery

This chapter describes real account mutations present in the archival code. It is not an instruction to execute them as a reproduction prerequisite. Start with offline tests.

## Modern session and inventory

Marketplace.__init__ logs in with Xbox through PlayFab title 20CA2, reads SessionTicket, then POSTs a session/start request to authorization.franchise.minecraft-services.net/api/v1.0. The response supplies authorizationHeader; subsequent Minecraft requests also carry a generated session-id.

The configured device profile says MinecraftPE, Windows10, uwp.store and a modern game version. The request currently sets en-US/US. This is separate from native Microsoft Store currency/pricing and is a known generalization limitation.

inventory() GETs entitlements.mktpl.minecraft-services.net/api/v1.0/player/inventory and returns result.inventory. The canonical balance helper requires an explicit virtualCurrencyBalances list and one integer, nonnegative Minecoin Total row. An explicit empty list is zero. Missing lists, duplicate Total rows, noninteger or negative values are errors, not zero.

Do not sum Purchased/Promotional stacks and Total together. Do not hardcode the balance from a prior session. Main Store initially showing zero until the Minecoin screen refreshed was a stale/default presentation problem, not evidence of missing money.

## Free claims

claim() serializes mutations with a lock and forces a fresh inventory read. If already permanently owned, it returns updated states. Otherwise it requests live detail and requires listPrice to be an actual integer zero with virtualCurrencyType Minecoin. This guards against stale seed prices, missing price and Coming Soon entries.

It POSTs /transaction/virtual with OfferId, empty StoreId and VirtualCurrency Amount string "0", Type Minecoin. It then polls fresh inventory for up to 30 seconds, requiring the offer's purchased entitlement and unchanged currency collection. Only then is success presented.

The older acquire_wilderness_free CLI is an experiment-specific helper with inventory/version headers and additional tags. It also writes full inventory/transaction results to local files despite a historical “sanitized” filename. Do not run or publish those files as if they were secret-free diagnostics.

## Existing-Minecoin item purchase

The tested paid offer UUID is ddd2bcc0-0996-4031-993a-0f541266c3dc, historically selected at 160 Minecoins. The source contains a deliberately narrow buy_test method, not generic checkout.

It requires a local authorization object containing that offer, amount 160 and an unexpired timestamp. Before POST, the authorization file is atomically consumed into a per-attempt record. The live price is rechecked and the expected balance is verified. Confirmation requires both owned entitlement and the exact 160 decrement. Ambiguous response becomes a reconciliation condition; it must not submit again just because the UI timed out.

No authorization file is included here. The old user authorization was for one historical transaction; it does not authorize future users' purchases.

## Five top-up products

Identifiers are observed configuration and can change. Prices are not guaranteed constants.

| Store product | Total coins | Legacy in-app offer token |
|---|---:|---|
| 9NHGX9G9JF1X | 320 | minecraft.win10.minecoin.200 |
| 9PD3R529P5XZ | 1020 | minecraft.win10.minecoin.600 |
| 9P063P6X637H | 1720 | minecraft.win10.minecoin.1000 |
| 9P2XG2G6PPRC | 3500 | minecraft.win10.minecoin.2000 |
| 9NJSBHH6FVRF | 8800 | minecraft.win10.minecoin.5000 |

Totals include the bonus presentation on applicable cards. The legacy suffix is not a reliable coin amount. ProbeCoinPlatform queries StoreContext.GetStoreProductsAsync, matches actual StoreId values, and uses Price.FormattedPrice plus CurrencyCode. Screenshot dollar prices were design references, not the live price authority. Product availability and market-specific currency require live platform checks; a larger-pack live purchase was not performed.

## Checkout is not delivery

Native coin_checkout.h calls StoreContext.RequestPurchaseAsync. Microsoft's UI controls the payment. The bridge does not take card details and does not replace that UI.

A success result or emailed receipt proves a platform purchase step, not that the Minecraft wallet has been credited. This distinction explained the first pending 320-Minecoin transaction. Launching the unmodified official Windows client credited that transaction; tracing its restore behavior informed the bridge implementation. A later separately authorized 320-Minecoin test succeeded through the bridge flow.

## Observed Windows delivery flow

1. Obtain PlayFab EntityToken through LoginWithXbox.
2. Call inventory/GetAccessTokens with MarketplaceConfigInstance Secondary and TargetMarketplace onestore.
3. Receive publisher Collections/Purchase access tokens.
4. Native StoreContext derives customer collections/purchase IDs with GetCustomerCollectionsIdAsync and GetCustomerPurchaseIdAsync.
5. PUT entitlements /transaction/redeem with purchaseInfo and a JSON-string receipt carrying publisher collections token, native collections key, native purchase key and RETAIL sandbox.
6. Validate result.failed, result.succeeded and result.transactionIds are arrays.
7. Read authoritative inventory repeatedly and require expected credit.
8. Only after credit confirmation acknowledge the exact native unfulfilled consumable using CurrentApp.ReportConsumableFulfillmentAsync.
9. Re-read pending native consumables; only reopen checkout when the relevant recovery state permits it.

The archived receipt also contains empty actor/inventory fields, purchasePath -1, empty productSku/platformPurchaseId and custom tags. These are observed official-client request shapes, not a public guaranteed service contract. See windows_coin_redemption.redeem_windows and the request-shape unit tests for the exact schema.

## Xbox restore fallback

POST /transaction/redeem/xbox uses a Redemption.MarketplaceData object with userId and XboxToken. The bridge follows this path only after an explicit empty Windows result and an unchanged wallet. A timeout, malformed response or failed Windows request must **not** trigger blind fallback. Otherwise one uncertain request becomes two uncertain requests.

## Journal and idempotency

The journal records attempt UUID, product, coin total, account XUID, baseline balance, native receipt, timestamps and recovery status. Secrets are absent, but transaction/account metadata is still personal and must not be distributed.

States include prepared, awaiting receipt, redeeming, requires reconciliation, confirmed and cancelled. A prepared record is saved before platform checkout. A recovery attempt is saved before the network operation. Completed attempts never call redemption again.

If current balance equals baseline+expected coins after a prior started attempt, recovery can confirm without resubmission. Unexpected changes require review. This exact-delta heuristic assumes no concurrent independent wallet activity; it is not a universal transaction-ID ledger proof. Document and test that limitation before broad deployment.

Recovery is bounded: 45-second poll window, 60-second retry separation, maximum three official attempts. Account changes, unknown products, changed transaction IDs and excessive/malformed native pending lists block rather than guessing.

## Cancellation regression

An empty native pending list while a checkout window is open is not “payment completed.” REC1 returns checkout-open for a merely prepared record. CAN2 and TOP2 carry the originating attempt UUID, so an old callback cannot cancel or complete the next checkout. Cancellation is accepted only with no receipt, no redemption started, the same account and a cancelable state.

The tests cover repeated cancel/reopen across all five products, stale attempt callbacks, missing receipts, account changes, exact delivery, no replay after confirmation and failure-versus-empty fallback. They run with fake services and temporary journals.

## Custom paid providers

Do not reuse these Microsoft product IDs to sell independent goods. A custom paid Marketplace needs its own payment integration, terms, refund handling, server-side entitlement authority and idempotent ledger. The reusable finding is the separation of checkout, fulfillment, credit verification and UI confirmation—not ownership of Microsoft's delivery backend.
