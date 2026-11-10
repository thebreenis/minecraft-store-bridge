# Authentication, account matching and session lifetime

## Identity constants

| Meaning | Value |
|---|---|
| Apple bundle | com.mojang.minecraftappletv |
| OAuth client | ios-app://com.mojang.minecraftappletv |
| Xbox title | 1835298427 / 0x6D646E7B |
| Xbox SCID | 00000000-0000-0000-0000-00006d646e7b |
| Device type / sandbox | AppleTV / RETAIL |
| Modern PlayFab title | 20CA2 |
| Windows family retained | Microsoft.MinecraftUWP_8wekyb3d8bbwe |

The OAuth client string was derived from the Apple implementation's bundle-ID formatting behavior, not a guessed Windows client ID. Changing xboxservices.config alone did not change the account provider's authenticating title.

## Observed chain

appletv_auth_probe.py contains the detailed construction:

1. Generate a P-256 proof key.
2. Authenticate an Xbox device using its public JWK and AppleTV device type.
3. Obtain a Microsoft ticket through a human-completed device-code flow.
4. Authenticate the Xbox user.
5. Authenticate the Xbox title using device/user/MSA context.
6. Authorize Xbox XSTS with user, device and title tokens.
7. Obtain a relying-party-appropriate XSTS context for PlayFab.
8. Log into PlayFab and start a Minecraft franchise session for modern commerce.

The legacy XSTS property is **SandboxId**, not Sandbox. The wrong spelling produced a failing final XSTS request despite earlier successful stages. Read the actual function arguments and payload in request_xsts_token; do not substitute a newer tutorial's schema indiscriminately.

## Proof-of-possession signature

ProofKey.sign_request takes method, URL, exact body bytes, authorization and optionally a timestamp. The signed digest is SHA-256 over:

```
BE32(1) || NUL || BE64(FILETIME) || NUL ||
UPPERCASE_METHOD || NUL || UTF8(path[?query]) || NUL ||
UTF8(authorization) || NUL || body || NUL
```

The ECDSA signature uses P-256 and prehashed SHA-256. The returned base64 decodes to version BE32, timestamp BE64, r as 32 bytes and s as 32 bytes. It is not a DER signature in the final transport field. Preserve the actual serialized body; signing one JSON representation and transmitting another is a different message.

The JWK x/y values are base64url coordinates. Private proof keys must not be included in research reports. A deterministic timestamp is useful for an offline verify test, but live calls require actual valid session context.

## Keep the native Windows account object

The x64 native helper hook is at RVA 0xE42AF0. The implementation lets the ordinary Windows account path run and replaces request authorization/signature and associated identity strings in the native result. The native account reference remains intact. Broad suppression/replacement of native authentication broke sign-in; reverting to the known .198 behavior and filtering the presence request separately was necessary.

The presence filter and request identity changes are not an invitation to replace native objects with Python structures. They are ABI-sensitive and tied to this executable. See presence_filter.cpp for the narrowly scoped Windows presence suppression and xinput_proxy.cpp for result construction.

## .212 account guard

windows_accounts reads metadata from HKCU:
- Software/Microsoft/XboxLive: AccountId, Xuid, Gamertag.
- Software/Microsoft/Windows/CurrentVersion/Store: PrimaryWebAccountId.
- IdentityCRL metadata is used only to form a display label when the Store account differs; credential stores are not read.

The decision function requires Xbox account ID, Xbox XUID, and Store account ID. IDs must match between Windows apps. Bridge XUID must match before game launch; otherwise bridge reauthentication is required.

Gamertag is optional. The affected-PC report had all stable identifiers, matching app accounts, but no Gamertag value in either registry view. .211 required the display name and rejected the launch. .212 removed that requirement, preserved ID checks and used explanatory display labels. The subsequent user test confirmed success.

These records may be missing or stale on other Windows/Xbox app versions. A matching registry record is the implemented policy, not proof that every visible account picker has synchronized. Do not silently guess identity from a profile picture or display name.

## Caching and renewal

The packaged launcher stores unexpired session material with current-user DPAPI in auth-session.bin. It loads only for the expected XUID. Developer probes are nonpersistent by default. The cache is not portable between users/machines and must never accompany a redistributable.

Automatic token renewal was deferred. Do not promise hours of continued service from startup success alone. A long-session test must observe expiry, request behavior and achievement delivery; extending expiry timestamps locally is not renewal.

Modern Marketplace sessions use a separate authorizationHeader plus session-id. The source currently supplies fixed language/region/device metadata (including en-US/US and a modern gameVersion). This is a compatibility profile, not evidence that all account locales have been modeled. Native Store top-up prices are obtained separately.
