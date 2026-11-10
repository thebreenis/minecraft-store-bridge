# Source map

Generated from pinned commit 9ed87e050c40f9683248e7fe9a79789ea5244e08. See the manifest for byte hashes.

The constants below are exact-build anchors, not portable offsets. Links point into the archived source.

## reference/installer/Collect-Diagnostics.cmd

[Read source](../reference/installer/Collect-Diagnostics.cmd)

## reference/installer/Collect-Diagnostics.ps1

[Read source](../reference/installer/Collect-Diagnostics.ps1)

## reference/installer/Install-Trust.ps1

[Read source](../reference/installer/Install-Trust.ps1)

## reference/installer/Install.cmd

[Read source](../reference/installer/Install.cmd)

## reference/installer/Install.ps1

[Read source](../reference/installer/Install.ps1)

## reference/native/achievement_ui.h


## reference/native/coin_checkout.h

- [Line 14](../reference/native/coin_checkout.h#L14): `std::string CoinPlatformPrice(size_t index) {`
- [Line 20](../reference/native/coin_checkout.h#L20): `std::string CoinCheckoutStatus() {`
- [Line 23](../reference/native/coin_checkout.h#L23): `void SetCoinCheckoutStatus(const char* text) {`
- [Line 26](../reference/native/coin_checkout.h#L26): `void CoinProbeReport(const std::wstring& text) {`
- [Line 32](../reference/native/coin_checkout.h#L32): `bool ReconcileWindowsCoins(const char* operation) {`
- [Line 101](../reference/native/coin_checkout.h#L101): `bool ReconcileWindowsCoinsWithRetry(const char* operation) {`
- [Line 109](../reference/native/coin_checkout.h#L109): `DWORD WINAPI ProbeCoinPlatform(LPVOID) {`
- [Line 211](../reference/native/coin_checkout.h#L211): `void RegisterCoinPurchaseButtons(void* controller) {`
- [Line 225](../reference/native/coin_checkout.h#L225): `void StartCoinPlatformProbe() {`

## reference/native/inception_achievement.h


## reference/native/presence_filter.cpp

- [Line 16](../reference/native/presence_filter.cpp#L16): `bool PresenceUrl(const std::wstring& url) {`
- [Line 48](../reference/native/presence_filter.cpp#L48): `bool ShouldBlock(HINTERNET request,LPCWSTR headers,DWORD length) {`
- [Line 106](../reference/native/presence_filter.cpp#L106): `void InstallPresenceWriteFilter(){InitOnceExecuteOnce(&installOnce,InstallOnce,nullptr,nullptr);}`
- [Line 107](../reference/native/presence_filter.cpp#L107): `void ObserveNativePresenceAuthorization(const std::wstring& value) {`

## reference/native/shulker_achievement.h


## reference/native/store_ownership.asm

[Read source](../reference/native/store_ownership.asm)

## reference/native/store_ui.h

- [Line 128](../reference/native/store_ui.h#L128): `constexpr const char* kPaidTestOffer = "ddd2bcc0-0996-4031-993a-0f541266c3dc";`
- [Line 10](../reference/native/store_ui.h#L10): `void* __fastcall CacheStorePicture(void* callback, void* result) {`
- [Line 21](../reference/native/store_ui.h#L21): `bool QueryStoreUi(const char* operation, const std::string& id, std::string& response) {`
- [Line 37](../reference/native/store_ui.h#L37): `void ApplyStoreUiStates(const std::string& response) {`
- [Line 61](../reference/native/store_ui.h#L61): `void RefreshStoreUiStates() {`
- [Line 68](../reference/native/store_ui.h#L68): `DWORD WINAPI RefreshHeaderWallet(LPVOID) {`
- [Line 76](../reference/native/store_ui.h#L76): `void EnsureHeaderWalletRefresh() {`
- [Line 84](../reference/native/store_ui.h#L84): `void* __fastcall LiveHeaderWallet(void* callback,void* result) {`
- [Line 94](../reference/native/store_ui.h#L94): `void* __fastcall LiveStoreTitle(void* callback,void* result) {`
- [Line 106](../reference/native/store_ui.h#L106): `std::string StoreOfferId(void* callback) {`
- [Line 114](../reference/native/store_ui.h#L114): `StoreUiState StoreState(const std::string& id) {`
- [Line 122](../reference/native/store_ui.h#L122): `void AssignNativeString(void* result, const std::string& text) {`
- [Line 129](../reference/native/store_ui.h#L129): `bool PaidTestOffer(const std::string& id) { return id == kPaidTestOffer; }`
- [Line 130](../reference/native/store_ui.h#L130): `DWORD WINAPI ReportStoreSound(LPVOID result) {`
- [Line 135](../reference/native/store_ui.h#L135): `void PlayClaimSuccess(void* callback) {`
- [Line 153](../reference/native/store_ui.h#L153): `StoreUiState StorePresentationState(void* callback) {`
- [Line 175](../reference/native/store_ui.h#L175): `void* __fastcall StoreActionLabel(void* callback, void* result) {`
- [Line 215](../reference/native/store_ui.h#L215): `bool __fastcall StoreActionEnabled(void* callback) {`
- [Line 228](../reference/native/store_ui.h#L228): `void TrackStorePreview(const std::string& id, const std::string& document) {`
- [Line 235](../reference/native/store_ui.h#L235): `bool __fastcall StoreActionCoins(void* callback) {`
- [Line 261](../reference/native/store_ui.h#L261): `void* __fastcall StoreDescription(void* callback, void* result) {`
- [Line 277](../reference/native/store_ui.h#L277): `DWORD WINAPI ClaimStoreFree(LPVOID parameter) {`
- [Line 311](../reference/native/store_ui.h#L311): `void RegisterTaggedStoreText(void* controller, const char* name, uintptr_t purpose) {`
- [Line 324](../reference/native/store_ui.h#L324): `void __fastcall RegisterStoreWaitText(void* controller) {`
- [Line 328](../reference/native/store_ui.h#L328): `void __fastcall RegisterCoinHeader(void* controller) {`
- [Line 341](../reference/native/store_ui.h#L341): `void InstallCoinHeaderBinding(unsigned char* base) {`
- [Line 357](../reference/native/store_ui.h#L357): `void InstallStoreWaitBinding(unsigned char* base) {`
- [Line 377](../reference/native/store_ui.h#L377): `void __fastcall RegisterProfileHelp(void* controller) {`
- [Line 387](../reference/native/store_ui.h#L387): `void InstallProfileHelp(unsigned char* base) {`
- [Line 403](../reference/native/store_ui.h#L403): `void InstallStoreUiBindings(unsigned char* base) {`
- [Line 479](../reference/native/store_ui.h#L479): `void InstallStoreOwnershipPresentation(unsigned char* base) {`

## reference/native/test_inception.cpp


## reference/native/test_presence_filter.cpp


## reference/native/test_shulker_source.cpp


## reference/native/xinput_proxy.cpp

- [Line 47](../reference/native/xinput_proxy.cpp#L47): `constexpr uintptr_t kAuthHelperRva = 0x00E42AF0;`
- [Line 48](../reference/native/xinput_proxy.cpp#L48): `constexpr uintptr_t kWalletBaseUrlRva = 0x01927C90;`
- [Line 49](../reference/native/xinput_proxy.cpp#L49): `constexpr uintptr_t kWalletUrlResolverRva = 0x0069A500;`
- [Line 50](../reference/native/xinput_proxy.cpp#L50): `constexpr uintptr_t kWalletUrlLoadRva = kWalletUrlResolverRva + 0xCC;`
- [Line 51](../reference/native/xinput_proxy.cpp#L51): `constexpr uintptr_t kWalletLoadRva = 0x00672E60;`
- [Line 52](../reference/native/xinput_proxy.cpp#L52): `constexpr uintptr_t kWalletReadyJumpRva = 0x00672EB8;`
- [Line 53](../reference/native/xinput_proxy.cpp#L53): `constexpr uintptr_t kWalletCompletionRva = 0x0069F320;`
- [Line 54](../reference/native/xinput_proxy.cpp#L54): `constexpr uintptr_t kWalletGetServiceRva = 0x000DB8E0;`
- [Line 55](../reference/native/xinput_proxy.cpp#L55): `constexpr uintptr_t kWalletTaskCleanupRva = 0x000D4570;`
- [Line 56](../reference/native/xinput_proxy.cpp#L56): `constexpr uintptr_t kWalletParseRva = 0x006A3010;`
- [Line 57](../reference/native/xinput_proxy.cpp#L57): `constexpr uintptr_t kWalletPreprocessRva = 0x006A36F0;`
- [Line 58](../reference/native/xinput_proxy.cpp#L58): `constexpr uintptr_t kWalletContextRva = 0x00699F90;`
- [Line 59](../reference/native/xinput_proxy.cpp#L59): `constexpr uintptr_t kJsonParseRva = 0x00E68960;`
- [Line 60](../reference/native/xinput_proxy.cpp#L60): `constexpr uintptr_t kCatalogInitRva = 0x006C7AA0;`
- [Line 61](../reference/native/xinput_proxy.cpp#L61): `constexpr uintptr_t kCatalogExecuteRva = 0x0060D320;`
- [Line 62](../reference/native/xinput_proxy.cpp#L62): `constexpr uintptr_t kCatalogParseRva = 0x0060ECC0;`
- [Line 63](../reference/native/xinput_proxy.cpp#L63): `constexpr uintptr_t kCatalogNotifyRva = 0x0060E9A0;`
- [Line 64](../reference/native/xinput_proxy.cpp#L64): `constexpr uintptr_t kCatalogSelectRva = 0x006C91D0;`
- [Line 65](../reference/native/xinput_proxy.cpp#L65): `constexpr uintptr_t kCatalogApplyManifestRva = 0x006C9470;`
- [Line 66](../reference/native/xinput_proxy.cpp#L66): `constexpr uintptr_t kCatalogManifestCallbackVtableRva = 0x017304E0;`
- [Line 67](../reference/native/xinput_proxy.cpp#L67): `constexpr uintptr_t kOfferPurchasableRva = 0x006C5040;`
- [Line 68](../reference/native/xinput_proxy.cpp#L68): `constexpr uintptr_t kThumbnailCallbackRva = 0x006C8C40;`
- [Line 69](../reference/native/xinput_proxy.cpp#L69): `constexpr uintptr_t kThumbnailDecodeCallbackRva = 0x006C8D70;`
- [Line 70](../reference/native/xinput_proxy.cpp#L70): `constexpr uintptr_t kThumbnailTextureCallbackRva = 0x006C88F0;`
- [Line 71](../reference/native/xinput_proxy.cpp#L71): `constexpr uintptr_t kThumbnailLoadRva = 0x005F0020;`
- [Line 72](../reference/native/xinput_proxy.cpp#L72): `constexpr uintptr_t kThumbnailApplyCallRva = 0x006C8C5F;`
- [Line 73](../reference/native/xinput_proxy.cpp#L73): `constexpr uintptr_t kThumbnailIdentityLoopRva = 0x006C8C9F;`
- [Line 74](../reference/native/xinput_proxy.cpp#L74): `constexpr uintptr_t kStringAssignRva = 0x000DC860;`
- [Line 75](../reference/native/xinput_proxy.cpp#L75): `constexpr uintptr_t kStringMapFindRva = 0x000DEC30;`
- [Line 76](../reference/native/xinput_proxy.cpp#L76): `constexpr uintptr_t kOfferFactoryFindReturnRva = 0x006C8746;`
- [Line 77](../reference/native/xinput_proxy.cpp#L77): `constexpr uint16_t kBridgePort = 32115;`
- [Line 78](../reference/native/xinput_proxy.cpp#L78): `constexpr bool kUseNativeThumbnails = true;`
- [Line 79](../reference/native/xinput_proxy.cpp#L79): `constexpr char kMagic[] = "ATVB1";`
- [Line 80](../reference/native/xinput_proxy.cpp#L80): `constexpr size_t kHookSize = 13;`
- [Line 81](../reference/native/xinput_proxy.cpp#L81): `constexpr size_t kWalletResolverHookSize = 14;`
- [Line 82](../reference/native/xinput_proxy.cpp#L82): `constexpr size_t kWalletLoadHookSize = 19;`
- [Line 83](../reference/native/xinput_proxy.cpp#L83): `constexpr size_t kWalletCompletionHookSize = 19;`
- [Line 84](../reference/native/xinput_proxy.cpp#L84): `constexpr size_t kCatalogInitHookSize = 18;`
- [Line 85](../reference/native/xinput_proxy.cpp#L85): `constexpr size_t kCatalogExecuteHookSize = 18;`
- [Line 86](../reference/native/xinput_proxy.cpp#L86): `constexpr size_t kOfferPurchasableHookSize = 18;`
- [Line 87](../reference/native/xinput_proxy.cpp#L87): `constexpr size_t kThumbnailCallbackHookSize = 16;`
- [Line 88](../reference/native/xinput_proxy.cpp#L88): `constexpr size_t kThumbnailDecodeCallbackHookSize = 18;`
- [Line 89](../reference/native/xinput_proxy.cpp#L89): `constexpr size_t kThumbnailTextureCallbackHookSize = 17;`
- [Line 90](../reference/native/xinput_proxy.cpp#L90): `constexpr size_t kThumbnailLoadHookSize = 19;`
- [Line 91](../reference/native/xinput_proxy.cpp#L91): `constexpr size_t kStringMapFindHookSize = 14;`

## reference/native/XINPUTUAP.def

[Read source](../reference/native/XINPUTUAP.def)

## reference/runtime/account_guard.py

- [Accounts](../reference/runtime/account_guard.py#L8)
- [normalize](../reference/runtime/account_guard.py#L15)
- [windows_accounts](../reference/runtime/account_guard.py#L18)
- [decision](../reference/runtime/account_guard.py#L42)
- [describe](../reference/runtime/account_guard.py#L49)
- [bridge_request](../reference/runtime/account_guard.py#L56)
- [bridge_identity](../reference/runtime/account_guard.py#L75)
- [stop_bridge](../reference/runtime/account_guard.py#L81)
- [listener_pids](../reference/runtime/account_guard.py#L97)
- [stop_legacy_bridge](../reference/runtime/account_guard.py#L111)
- [reject_message](../reference/runtime/account_guard.py#L128)
- [alert](../reference/runtime/account_guard.py#L134)
- [wait_before_exit](../reference/runtime/account_guard.py#L140)

## reference/runtime/appletv_auth_bridge.py

- [log_event](../reference/runtime/appletv_auth_bridge.py#L57)
- [recv_exact](../reference/runtime/appletv_auth_bridge.py#L64)
- [read_fields](../reference/runtime/appletv_auth_bridge.py#L71)
- [write_response](../reference/runtime/appletv_auth_bridge.py#L78)
- [BridgeState](../reference/runtime/appletv_auth_bridge.py#L87)
  - [BridgeState.__init__](../reference/runtime/appletv_auth_bridge.py#L88)
- [publish_presence](../reference/runtime/appletv_auth_bridge.py#L110)
- [presence_heartbeat](../reference/runtime/appletv_auth_bridge.py#L138)
- [BridgeHandler](../reference/runtime/appletv_auth_bridge.py#L144)
  - [BridgeHandler.handle](../reference/runtime/appletv_auth_bridge.py#L145)
- [BridgeServer](../reference/runtime/appletv_auth_bridge.py#L193)
  - [BridgeServer.__init__](../reference/runtime/appletv_auth_bridge.py#L197)
- [WalletHandler](../reference/runtime/appletv_auth_bridge.py#L202)
  - [WalletHandler.do_GET](../reference/runtime/appletv_auth_bridge.py#L205)
  - [WalletHandler.log_message](../reference/runtime/appletv_auth_bridge.py#L216)
- [load_legacy_thumbnail](../reference/runtime/appletv_auth_bridge.py#L220)
- [ThumbnailHandler](../reference/runtime/appletv_auth_bridge.py#L239)
  - [ThumbnailHandler.do_GET](../reference/runtime/appletv_auth_bridge.py#L242)
  - [ThumbnailHandler.log_message](../reference/runtime/appletv_auth_bridge.py#L260)
- [launch_game](../reference/runtime/appletv_auth_bridge.py#L264)
- [bridge_is_running](../reference/runtime/appletv_auth_bridge.py#L276)
- [game_is_running](../reference/runtime/appletv_auth_bridge.py#L284)
- [stop_after_game](../reference/runtime/appletv_auth_bridge.py#L294)
- [find_playfab_xsts](../reference/runtime/appletv_auth_bridge.py#L308)
- [authenticate](../reference/runtime/appletv_auth_bridge.py#L366)
- [launcher_visible](../reference/runtime/appletv_auth_bridge.py#L410)
- [monitor_accounts](../reference/runtime/appletv_auth_bridge.py#L421)
- [main](../reference/runtime/appletv_auth_bridge.py#L445)

## reference/runtime/appletv_auth_probe.py

- [open_account_selection_browser](../reference/runtime/appletv_auth_probe.py#L40)
- [base64url](../reference/runtime/appletv_auth_probe.py#L46)
- [filetime_now](../reference/runtime/appletv_auth_probe.py#L50)
- [ProofKey](../reference/runtime/appletv_auth_probe.py#L54)
  - [ProofKey.__init__](../reference/runtime/appletv_auth_probe.py#L55)
  - [ProofKey.jwk](../reference/runtime/appletv_auth_probe.py#L58)
  - [ProofKey.sign_request](../reference/runtime/appletv_auth_probe.py#L69)
- [compact_json](../reference/runtime/appletv_auth_probe.py#L112)
- [signed_post](../reference/runtime/appletv_auth_probe.py#L116)
- [require_token](../reference/runtime/appletv_auth_probe.py#L134)
- [request_device_token](../reference/runtime/appletv_auth_probe.py#L145)
- [acquire_msa_token](../reference/runtime/appletv_auth_probe.py#L173)
- [request_user_token](../reference/runtime/appletv_auth_probe.py#L252)
- [request_title_token](../reference/runtime/appletv_auth_probe.py#L276)
- [find_title_token](../reference/runtime/appletv_auth_probe.py#L307)
- [request_xsts_token](../reference/runtime/appletv_auth_probe.py#L354)
- [request_achievements](../reference/runtime/appletv_auth_probe.py#L385)
- [run_full_probe](../reference/runtime/appletv_auth_probe.py#L412)
- [print_response](../reference/runtime/appletv_auth_probe.py#L486)
- [main](../reference/runtime/appletv_auth_probe.py#L509)

## reference/runtime/auth_progress.py

- [SignInCancelled](../reference/runtime/auth_progress.py#L7)
- [SignInProgress](../reference/runtime/auth_progress.py#L10)
  - [SignInProgress.__init__](../reference/runtime/auth_progress.py#L11)
  - [SignInProgress._run](../reference/runtime/auth_progress.py#L24)
  - [SignInProgress.wait_for_ok](../reference/runtime/auth_progress.py#L68)
  - [SignInProgress.check_cancelled](../reference/runtime/auth_progress.py#L72)
  - [SignInProgress.status](../reference/runtime/auth_progress.py#L75)
  - [SignInProgress.close](../reference/runtime/auth_progress.py#L76)
- [begin](../reference/runtime/auth_progress.py#L81)
- [check_cancelled](../reference/runtime/auth_progress.py#L88)
- [status](../reference/runtime/auth_progress.py#L92)
- [close](../reference/runtime/auth_progress.py#L96)
- [close_when_game_starts](../reference/runtime/auth_progress.py#L101)

## reference/runtime/auth_session_cache.py

- [Blob](../reference/runtime/auth_session_cache.py#L9)
- [protect](../reference/runtime/auth_session_cache.py#L12)
- [clear](../reference/runtime/auth_session_cache.py#L24)
- [save](../reference/runtime/auth_session_cache.py#L27)
- [load](../reference/runtime/auth_session_cache.py#L34)

## reference/runtime/catalog_image_server.py

- [cache_image](../reference/runtime/catalog_image_server.py#L21)
- [Handler](../reference/runtime/catalog_image_server.py#L38)
  - [Handler.do_GET](../reference/runtime/catalog_image_server.py#L39)
  - [Handler.log_message](../reference/runtime/catalog_image_server.py#L53)

## reference/runtime/coin_topup.py

- [balance](../reference/runtime/coin_topup.py#L28)
- [save](../reference/runtime/coin_topup.py#L31)
- [parse_pending](../reference/runtime/coin_topup.py#L36)
- [confirm](../reference/runtime/coin_topup.py#L50)
- [reconcile](../reference/runtime/coin_topup.py#L57)
- [handle](../reference/runtime/coin_topup.py#L126)

## reference/runtime/live_marketplace.py

- [objects](../reference/runtime/live_marketplace.py#L13)
- [minecoin_balance](../reference/runtime/live_marketplace.py#L22)
- [Marketplace](../reference/runtime/live_marketplace.py#L37)
  - [Marketplace.__init__](../reference/runtime/live_marketplace.py#L38)
  - [Marketplace.inventory](../reference/runtime/live_marketplace.py#L52)
  - [Marketplace.detail](../reference/runtime/live_marketplace.py#L57)
  - [Marketplace.acquire_wilderness_free](../reference/runtime/live_marketplace.py#L62)

## reference/runtime/live_wallet_adapter.py

- [wallet](../reference/runtime/live_wallet_adapter.py#L14)
- [Handler](../reference/runtime/live_wallet_adapter.py#L41)
  - [Handler.handle](../reference/runtime/live_wallet_adapter.py#L42)
- [Server](../reference/runtime/live_wallet_adapter.py#L53)

## reference/runtime/packaged_launcher_runtime.py

- [_diagnostic_exception](../reference/runtime/packaged_launcher_runtime.py#L7)

## reference/runtime/packaged_services.py

- [start](../reference/runtime/packaged_services.py#L6)

## reference/runtime/probe_playfab_from_bridge.py

- [read_exact](../reference/runtime/probe_playfab_from_bridge.py#L15)
- [get_bridge_fields](../reference/runtime/probe_playfab_from_bridge.py#L22)
- [main](../reference/runtime/probe_playfab_from_bridge.py#L38)

## reference/runtime/runtime_paths.py


## reference/runtime/session_presence.py

- [signed_request](../reference/runtime/session_presence.py#L10)
- [publish](../reference/runtime/session_presence.py#L25)
- [verify](../reference/runtime/session_presence.py#L33)
- [run](../reference/runtime/session_presence.py#L40)

## reference/runtime/skin_store_route.py

- [installed_packs](../reference/runtime/skin_store_route.py#L8)
- [resolve](../reference/runtime/skin_store_route.py#L27)

## reference/runtime/startup_diagnostics.py

- [event](../reference/runtime/startup_diagnostics.py#L10)
- [once](../reference/runtime/startup_diagnostics.py#L22)
- [start](../reference/runtime/startup_diagnostics.py#L29)
- [accounts](../reference/runtime/startup_diagnostics.py#L33)

## reference/runtime/store_ui_adapter.py

- [refresh](../reference/runtime/store_ui_adapter.py#L34)
- [states](../reference/runtime/store_ui_adapter.py#L50)
- [detail](../reference/runtime/store_ui_adapter.py#L67)
- [claim](../reference/runtime/store_ui_adapter.py#L97)
- [minecoins](../reference/runtime/store_ui_adapter.py#L122)
- [buy_test](../reference/runtime/store_ui_adapter.py#L125)
- [exact](../reference/runtime/store_ui_adapter.py#L165)
- [Handler](../reference/runtime/store_ui_adapter.py#L173)
  - [Handler.handle](../reference/runtime/store_ui_adapter.py#L174)
- [Server](../reference/runtime/store_ui_adapter.py#L227)
- [ImageHandler](../reference/runtime/store_ui_adapter.py#L231)
  - [ImageHandler.do_GET](../reference/runtime/store_ui_adapter.py#L232)
  - [ImageHandler.log_message](../reference/runtime/store_ui_adapter.py#L247)

## reference/runtime/test_account_guard.py

- [AccountTests](../reference/runtime/test_account_guard.py#L5)
  - [AccountTests.test_missing_registry_gamertag](../reference/runtime/test_account_guard.py#L6)
  - [AccountTests.test_friend_missing_tag_starts_auth](../reference/runtime/test_account_guard.py#L16)
  - [AccountTests.test_mismatch_not_bypassed](../reference/runtime/test_account_guard.py#L24)
  - [AccountTests.test_missing_ids_still_blocked](../reference/runtime/test_account_guard.py#L26)
  - [AccountTests.test_existing_named_account](../reference/runtime/test_account_guard.py#L29)
  - [AccountTests.test_display_name_not_identity](../reference/runtime/test_account_guard.py#L33)

## reference/runtime/wallet_https_server.py

- [_modern_items](../reference/runtime/wallet_https_server.py#L33)
- [_legacy_document](../reference/runtime/wallet_https_server.py#L60)
- [_legacy_query_manifest](../reference/runtime/wallet_https_server.py#L124)
- [Handler](../reference/runtime/wallet_https_server.py#L182)
  - [Handler._reply](../reference/runtime/wallet_https_server.py#L185)
  - [Handler.do_GET](../reference/runtime/wallet_https_server.py#L238)
  - [Handler.do_POST](../reference/runtime/wallet_https_server.py#L241)
  - [Handler.log_message](../reference/runtime/wallet_https_server.py#L244)
- [DiagnosticHTTPSServer](../reference/runtime/wallet_https_server.py#L248)
  - [DiagnosticHTTPSServer.__init__](../reference/runtime/wallet_https_server.py#L249)
- [main](../reference/runtime/wallet_https_server.py#L255)

## reference/runtime/windows_coin_redemption.py

- [access_tokens](../reference/runtime/windows_coin_redemption.py#L6)
- [summary](../reference/runtime/windows_coin_redemption.py#L17)
- [redeem_windows](../reference/runtime/windows_coin_redemption.py#L25)
- [redeem](../reference/runtime/windows_coin_redemption.py#L38)
