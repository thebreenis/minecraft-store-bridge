# Building an independent custom Marketplace

## What is reusable

The project separates an old native presentation/parser from newer service data. The same pattern can connect a catalog of your own licensed content, without impersonating Microsoft commerce. The native UI wants stable offer documents, query rows, thumbnails, gallery callbacks and explicit action state. It does not inherently require that your catalog be a copy of Microsoft's.

There are two different projects:
- Reproduce the observed Microsoft-backed compatibility bridge with the user's own inputs/session.
- Build an independent provider with your own catalog, identity, entitlement ledger and content delivery.

Do not mix their balances or represent custom grants as official Microsoft purchases.

## Suggested provider interface

```text
list_offers(cursor, locale) -> page, next_cursor, catalog_revision
get_offer(offer_id, locale) -> metadata, price, content descriptors
get_inventory(account_id) -> owned offers, wallet snapshot, revision
evaluate_compatibility(content_digest, engine) -> C/I/U + reasons
claim_free(account_id, offer_id, idempotency_key) -> transaction reference
download_descriptor(account_id, content_id) -> bounded URL, hash, size
transaction_status(account_id, transaction_id) -> authoritative outcome
```

Define the normalized domain model first; translate it to legacy JSON as a separate step. Use stable IDs, not title strings. Keep locale/region, ownership authority and content hash in cache keys. Include a provider namespace so UUID collisions cannot merge independent catalogs.

## Executable offline example

examples/offline_marketplace.py loads only the synthetic fixtures/catalog.json. Its model separates price, ownership and compatibility. It supports a free, in-memory claim with duplicate protection; paid actions are rejected. It emits a legacy-shaped catalog and ALL1-style state text, and can serve a small HTTP API on 127.0.0.1:33224.

```
python examples/offline_marketplace.py --demo
python examples/offline_marketplace.py --serve
```

GET /catalog returns translated rows, GET /states returns text, GET /offers/<uuid> returns the fixture, and POST /claim/<uuid> claims only a known zero-price non-coming-soon offer. There is no Microsoft connection, login, real currency, pack download, game patch, or persistent ownership. Claims are lost on server restart.

The example uses a separate port deliberately. The real game will not discover it automatically. To integrate it, implement a provider-backed version of the reference adapters and keep the native transport endpoints consistent with the compiled hooks. Do not blindly redirect a live signed session to this server.

The example's minEngine is a toy declared requirement, not manifest-scanner evidence. The synthetic compatible item does not include a runnable Minecraft pack. Supply your own licensed test pack and validate the full installation path independently.

## Implementation sequence

1. Generate several stable fake offers with distinct titles and IDs. Prove translation and unique native registration before introducing commerce.
2. Implement query rows and category selection. Make selection deterministic and pagination explicit.
3. Add one image and then multiple gallery images. Verify every request completes after repeated Store openings.
4. Add session-scoped inventory and a read-only balance. Test account changes and cache invalidation.
5. Add free grants with transaction IDs/idempotency and post-write inventory confirmation.
6. Add a compatibility evaluator with unknown as a first-class result, plus reasons.
7. Implement downloads only for authorized, verified-compatible content. Use staging, hashes, bounded extraction and atomic commit.
8. Verify local pack discovery and Create World filtering independently from Store detail.
9. Only then consider paid checkout, with a separate backend ledger and explicit human-authorized tests.
10. Exercise failures: server offline, malformed JSON, missing image, expired auth, duplicate callback, account change, interrupted download and delayed entitlement propagation.

## Necessary work beyond the reference

The reference assumes a trusted local catalog/source. A public provider needs authentication, authorization, endpoint allowlists, request-size limits, decompression/image pixel limits, cancellation, deadlines, content signing, replay protection, concurrent transaction policy and server audit trails. Native ABI and memory safety need review separately from protocol correctness.

A suitable compatibility database records engine build hash, manifest/content hashes, observed load result and feature-specific failures. Do not replace a failed compatibility check with an Owned flag. For bundles, validate required dependencies collectively.

The reusable UI can display Owned, Free, Download, Incompatible and Coming Soon, but only the provider's authoritative state can justify those labels. A custom store can be fully useful without paid transactions: original community packs plus explicit free grants are enough to exercise the architecture.
