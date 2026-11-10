# Failure history and rejected shortcuts

| Symptom / approach | Finding | Lesson |
|---|---|---|
| Change embedded title ID/SCID only | Windows provider still derives native identity from package context | Routing IDs are not full authentication identity |
| Replace/bypass broad native token/account handling | Sign-in regressed in .199/.200 attempts | Keep native account object; filter presence separately |
| Repeated offer pointer interpreted as cache reuse | Query callback used a different capture field | Confirm object layout before changing caching |
| Many rows but one usable item | Empty native product key collapsed registration | Validate distinct native identity, not just JSON count |
| Async catalog worker notified after native scheduler | Duplicate completion/race could crash | Exactly one owner/completion path |
| Suppress repeated image URLs | New query pending counter never completed | Deduplicate bytes, not per-request completion |
| Wallet shows zero until opening coin screen | Main Store refresh/default state lagged | Freshness and failure must be explicit |
| Item title disappears or opens empty subview | Detail/binding/lifecycle gaps | Test selected item, subpack and carousel paths separately |
| Coming-soon item looked free | Missing price was treated like zero | Free requires explicit authoritative price |
| Claim completed but button changed only on hover | Native UI invalidation was insufficient | Refresh state on completion, not pointer movement |
| Done! appears on the action button | Popup and action reused status bindings | Separate presentation state for popup/button |
| Sound call succeeds but user hears nothing | Function return is not audible evidence | Confirm resource/event and actual output |
| Payment email arrives but no Minecoins | Platform checkout and game fulfillment are separate | Observe official restore path; verify wallet credit |
| Cancel/reopen blocks future checkout | Background empty receipt and stale callbacks confused state | Bind callbacks to attempt UUID; no-payment is not paid |
| Every catalog entry appears in Create World | Discoverable offer is not installed usable template | Filter by actual content type, ownership and validation |
| Delisted skin Unlock does nothing | Route by runtime pack identity; handle missing listing | No missing listing implies free ownership |
| Fresh reinstall certificate/loopback helper fails | Named loopback configured before package registration | Correct order, preserve child error details |
| All installs checks pass but one account cannot launch | Optional Gamertag registry value missing | Verify stable IDs, not display metadata |

## Historical notes can be stale

Original handoff files were written at different milestones and sometimes say “not yet validated” for work later confirmed. This repository does not copy them wholesale because that would mix state and expose account information. The claims ledger records later confirmations separately, with known limits.

Some paths and experiments were cleaned up to reclaim disk space. The build source, exact inputs, tests and final reconstruction recipe are the durable reproducibility artifacts. A missing old binary is not a reason to fabricate a contemporaneous trace.

## Open problems worth researching

- Authoritative Windows account detection when legacy registry metadata is missing/stale beyond the fixed display-name case.
- Secure automatic token renewal and request recovery across long gameplay sessions.
- General manifest/feature-level compatibility evaluation before download.
- Fully correct content download/install lifecycle for modern pack types in an old engine.
- Safe catalog pagination/refresh and locale/market selection.
- Hardened authenticated local IPC, consistent error frames and bounded media fetches.
- Online invite joining. Mutual legacy friendship was visible, but the failing friend's join path was not traced locally; a later host lobby 403 overlapped world exit and was not established as the cause.
