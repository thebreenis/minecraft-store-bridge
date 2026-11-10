# Catalog, detail and image translation

## Source shapes and identifiers

_modern_items recursively walks modern-store-root.json for dictionaries with an id, title and contentType MarketplaceDurableCatalog_V1.2. This is a snapshot-driven bootstrap, not a complete continuously paginated discovery implementation.

_legacy_document constructs a MarketplaceDurableCatalog_V1.1 document. Important mappings:

| Modern concept | Legacy field |
|---|---|
| id / offer UUID | productId and documentId |
| title / description | initially strings, localized dictionaries for detail |
| creatorPage | creatorId suffix after ! |
| creatorName | creatorName and creatorGamertag presentation |
| thumbnail.url | local thumbnailUrl and images entries |
| price.listPrice | numeric price and custom.price |
| packType | tags and custom.packType |
| startDate | creationDate/startDate/lastModifiedDate |
| packIdentity | custom.packIdentity |
| rating | custom.rating |

Pack type mapping: SkinPack → skinpack; ResourcePack → resourcepack; WorldTemplate → worldtemplate; MashUp → worldtemplate. A mash-up contains more than a world; this mapping is a legacy presentation approximation, not proof that all associated content is a valid template.

The adapter's historical default of missing price to zero is unsafe as a commerce decision. The final free-claim function independently re-reads the live item and requires an actual integer zero Minecoin price. Never decide that a missing price means free.

The historical minClientVersion/clientVersion/version values of 1.1.5 were parser placeholders. detail removes minClientVersion and clientVersion precisely because those fields were not compatibility evidence. A new provider should validate real manifests and use a clearly separate display/version schema.

## Query manifests and category rows

The old client first expects a QueryManifest_V1.1.5 document and legacy queries with fields such as queryOrder, rowName, searchCriteria, tags, sort, itemOrder, featured and isNavButtonQuery. Simply returning modern items without the query manifest is insufficient.

The prototype _legacy_query_manifest includes a Featured row. The final packaged recipe/seed provides the broader category setup and the requested Free/New front-page rows. Do not infer final row configuration solely from the older helper function. The full pinned upstream payload and UI patch recipe are required for exact reconstruction.

“Every free item” in this project means every detected free offer within the known catalog, not exhaustive enumeration of Microsoft's current global catalog. A real discovery service needs pagination, product availability rules, refresh provenance and regional handling.

## Detail routes

Marketplace.detail posts to /layout/pages/ItemDetail_<offer UUID>. store_ui_adapter.detail starts with the corresponding legacy document, localizes string title/description fields, normalizes an en dash to a hyphen to avoid the old title font fallback, extracts ImageGallery URLs, and appends local screenshot entries.

Each image gets a deterministic <offer>-<index>.png cache name with a sidecar .url. The image service fetches/converts on demand. Detail JSON itself is cached. For a custom store, include content-version/locale in the cache key and invalidate when metadata changes; the reference cache is intentionally simpler.

Some skin packs supplied only one gallery image. The development question was whether the service actually returned one image or our traversal omitted others. Do not pad the carousel with invented assets. Compare the raw gallery count, unique HTTPS URLs, converted-file count and native loaded-image count.

## Installed skin selection → Store

skin_store_route resolves the chosen installed skin pack, not merely a manually maintained list of offer names:

1. Read installed skin_pack manifests, skins.json and localization keys.
2. Prefer the runtime-selected pack UUID when replacement manifests differ.
3. POST /layout/pages/packId/<pack UUID>.
4. Require the returned packIdentity to include the selected UUID.
5. Translate the actual offer and gallery into legacy form.
6. If absent/unreachable, show unavailable/retry information; do not grant ownership.

Cache key is the skin key plus UUID, with five-minute success caching. Transient failures are not cached as permanent absence. A delisted licensed pack is not automatically public domain or owned.

## Distinct offer identity and thumbnails

Modern rows initially produced blank native product strings, collapsing multiple offers into one registration-map key. The native hook recovered each exact product UUID from the thumbnail URL and assigned it through the game's native string routine. This fix is separate from the later discovery that query and standalone thumbnail callbacks had different object layouts.

For verification, compare unique catalog UUID count, native registered offer count, titles, per-offer image selection, and reopening behavior. “125 rows parsed” alone did not prove 125 distinct usable offer objects.

## Creating world templates

A catalog entry is an advertisement, not an installed template. The project encountered sound/texture/animation items incorrectly appearing in Create World with placeholders such as version 0.0.0. Ownership, actual template type, engine compatibility, complete installation, and parseable manifest must all hold before a template is offered as usable. A custom provider should keep this list driven by validated local installations rather than by its Store query results.
