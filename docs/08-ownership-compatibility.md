# Ownership, compatibility and action policy

## Four independent questions

1. **Listing:** does an offer exist and have valid metadata/price?
2. **Entitlement:** does the authenticated account own the relevant offer/content?
3. **Compatibility:** can this engine parse and execute that payload?
4. **Installation:** is a complete, verified local copy present and usable?

A marketplace can answer yes to any subset. Never use an Owned badge as proof of compatibility, or a parsed catalog version as proof of manifest support.

## Reference ownership rule

store_ui_adapter.states builds owned offer IDs only from inventory entitlements whose ownership is Purchased. The wallet adapter also restricts its legacy item projection to permanent purchased Item entries with a packId and offerIds. Subscription/pass rows are not converted into permanent licenses. The source does not claim to model every current entitlement category.

A successful claim response is insufficient: refresh inventory until the expected entitlement is present. An unchanged coin balance is required for a free claim. Pending state must refresh the native UI without requiring the mouse to leave and reenter the button.

## Policy matrix

| Ownership | Listing | Compatibility | Intended action |
|---|---|---|---|
| unowned | verified free | any/unknown | Free claim permitted |
| unowned | paid | incompatible/unknown | disabled Incompatible |
| owned | available | compatible and installable | Download |
| owned | available | incompatible/unknown | disabled Incompatible; ownership still shown |
| unowned | no price, explicitly coming soon | unknown | Coming Soon |
| unowned | unavailable/no verified price | unknown | Unavailable |
| any | transaction in flight | any | Please Wait..., no duplicate action |

The historical 160-Minecoin purchase test is a narrow exception protected by an expiring, one-use authorization file. It is not a general feature allowing all incompatible paid offers. The source's action predicate and label priority should be read together; a future provider should make the matrix a single explicit policy module to avoid contradictory labels/click behavior.

## What the existing classifier actually does

In states(), the specific Wilderness Bound offer is I; other known offers are U by default. Absence of price leads to S when description contains “coming soon,” otherwise N. This is conservative gating, not full manifest inspection. The I path's description names a known required engine version in native code; that string is item-specific evidence, not a general version resolver.

“Unknown” can arise because:
- Listing metadata contains pack identity/version but no minimum supported engine.
- Payload manifests are unavailable before acquisition/download.
- Bundles contain multiple subpacks or dependent packs with different requirements.
- Schema fields are modern, renamed, absent, or not understood by the old parser.
- A minimum version alone does not capture unsupported entity formats, geometry, render/material features, scripting, world data or behavior components.
- Cached detail metadata may be stale or mismatched to the actual downloadable payload.

## Designing a real evaluator

For content you may inspect, parse each manifest and dependencies; identify pack type, format_version, min_engine_version and actual feature requirements; preserve the original evidence. Evaluate a bundle as the conjunction of required components. Return compatible/incompatible/unknown with a reason and the manifest/content digest used. Do not fill a missing minimum with 1.1.5.

A useful result schema is:
```json
{"status":"unknown","reason":"manifest_not_available","engine":[1,1,5],"contentDigest":null}
```

The offline fixture uses declared synthetic minima to demonstrate policy only. It does not certify real Minecraft content.

## Downloads are a separate project

A custom provider needs a download descriptor, integrity hash, entitlement check, bounded extraction, dependency handling, atomic install, rollback and local pack indexing. The reference research does not supply a universally working downloader/converter for modern Marketplace packs or a way to decrypt content without authorization. Keep that boundary visible in the UI.

The original Create World bug demonstrated why: arbitrary Store catalog entries, including non-world content, were projected as templates. A usable-world list should be derived from validated installed content with genuine ownership, not from offer discoverability.
