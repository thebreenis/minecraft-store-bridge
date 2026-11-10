# Local wire contracts

These are private implementation protocols, not official Minecraft APIs. Every current server binds to loopback. Little-endian lengths are used for local framing; proof-key signatures have different big-endian fields.

## ATVB1 on 32115

Request:
```
5 bytes ASCII "ATVB1"
4 x uint32_le byte lengths
method UTF-8 bytes
url UTF-8 bytes
headers UTF-8 bytes
body bytes
```

There is no separator between payload fields. The server caps each incoming field at 16 MiB. The supplied headers field is currently ignored by BridgeHandler; method/URL/body and selected authorization feed the signer.

Success response:
```
uint32_le status = 0
7 x uint32_le byte lengths
authorization, signature, xuid, gamertag, user_hash, age_group, privileges
```

For PlayFab-host requests it selects the PlayFab authorization context; otherwise Xbox authorization. CONTROL plus local://account-switch requests bridge shutdown for a verified account switch. The client checks field lengths and failures. The archived server error path emits a shorter field list than the normal seven-field client expects; do not design a new client assuming that malformed/failure responses always have success framing. A hardened successor should normalize error framing and add end-to-end tests.

Local access to this port exposes highly sensitive signing/authorization functionality. Loopback is not client authentication. Treat the reference implementation as trusted-user desktop code, not a multi-tenant security service.

## WAL1 on 32121

Client sends exactly four ASCII bytes WAL1. Response is uint32_le payload length followed by UTF-8 legacy wallet JSON; zero length means unavailable. The adapter gets actual permanent entitlements and one authoritative Total Minecoin row. Inventory is cached for 60 seconds.

The wallet JSON contains Balance.currencies with currencyType xmc, EntitlementReceipt empty, and Inventory.items. Each translated item has pack type/ID and offer productId with an empty purchaseReceipt. It does not invent a cryptographic legacy receipt.

Important discrepancy: live_wallet_adapter.wallet expects exactly one Total row and fails if none exists. The newer shared minecoin_balance used by Store/top-up logic accepts an explicit empty currency list as zero, while rejecting missing/ambiguous rows. Preserve this distinction in regression reports; the code paths are not identical.

## Store UI on 32122

Every request starts with a four-byte opcode. Every successful response starts with uint32_le length and bytes. Handler exceptions return zero length. This deliberately loses the detailed server failure at the native boundary; structured diagnostics/error classifications are preferable in a future revision.

| Opcode | Remaining request | Response meaning |
|---|---|---|
| ALL1 | none | state rows + balance/tag |
| DET1 | 36-byte offer UUID | legacy detail JSON |
| CLM1 | 36-byte offer UUID | refreshed states after verified free claim |
| BUY1 | 36-byte offer UUID | guarded historical paid-test purchase |
| SKN1 | uint32 size + ASCII key | resolved installed-skin catalog result |
| SND1 | 36-byte diagnostic string | sound-call observation acknowledgment |
| TOK1 | none | publisher collections token, purchase token, user, newline-separated |
| PRP3 | uint32 size + product ID line + native pending observation | ready:attempt UUID or failure |
| CAN2 | uint32 size + attempt line + native pending observation | cancelled after matched no-payment evidence |
| TOP2 | uint32 size + attempt line + native pending observation | reconcile successful checkout result |
| REC1 | uint32 size + pending observation | recovery without initiating checkout |
| RDM1 | uint32 size + pending observation + two native key lines | official delivery reconciliation |

Historical ARM1, PRP1, PRP2, CAN1, TOP1 also exist. Prefer the current attempt-bound PRP3/CAN2/TOP2 design when studying cancellation. It was added because stale callbacks could otherwise affect another attempt.

Pending observation:
```
<count>\n
<product offer token>|<transaction UUID>\n
...
```

Count is bounded to 0..16, duplicate transaction UUIDs are rejected. Receipt-observation payloads are 1..73728 bytes; skin route keys 1..165 bytes. RDM1 appends collections and purchase keys; native Store code obtains them using publisher tokens. They must not appear in a shared diagnostic trace.

ALL1 state rows:
```
<offer UUID>|<owned 0/1>|<free 0/1>|<compatibility code>\n
BAL|<integer balance>\n
TAG|<display name>\n
```

Codes C/I/U/S/N mean compatible/incompatible/unknown/coming-soon/unavailable. The UI displays U as Incompatible. The reference states producer normally returns I for one known incompatible item and U for most others; C is not the result of a general implemented manifest evaluator.

Native QueryStoreUi uses 180-second timeouts for transactions/restore/key operations and 45 seconds otherwise. Long UI waits should be on worker paths, not block the rendering thread.

## HTTP image adapters

32117 offers the historical thumbnail route, with offer ID in the URL. 32123 accepts only UUID-number.png names, reads a cached source URL, fetches HTTPS media, converts to RGBA PNG and caches it. The source URL comes from catalog/detail data; there is no general URL allowlist or download-size cap in this archival handler. A custom provider must implement those controls before accepting untrusted catalogs.

32118 serves catalog images. Do not treat an image cache hit as a new query's completion: each native pending callback must still finish.
