# Reproduce without guessing

## Track A: offline research

Use Python 3.11+ and a fresh virtual environment. Install requests and cryptography from requirements-reference.txt, or the minimal versions shown in README. Pillow/PyInstaller are needed for the full upstream build, not the standard-library example. Run:

```
python tools/verify_reference.py
python tools/run_checks.py
python examples/offline_marketplace.py --demo
```

No existing Xbox session is necessary. No reference authentication CLI is run. The test runner redirects runtime state into a temporary directory and blocks outgoing connections/HTTP. Tests include real reference wallet/recovery functions with mocked service responses. Fixture values are invented; similar historical balance numbers in regression tests are test constants, not an account dump.

## Track B: exact compatibility build

Acquire your own legally usable supported originals. Filenames are not validation: use the two SHA-256 values in upstream.lock.json. Repacked archives are rejected even if the visible version is unchanged. The patcher does not decrypt Apple packages.

Fetch the exact source explicitly:

```
python tools/fetch_upstream.py work/upstream
```

This command performs a network Git clone and detached checkout; it does not build, install, authenticate or run downloaded code. Alternatively clone the repository yourself and check out the full pinned commit.

On Windows x64, install .NET SDK supporting net8.0-windows, Python 3.11+ x64, Visual Studio C++ Build Tools (C++/WinRT and MASM), and Windows SDK packaging/signing tools. From that checkout:

```powershell
.\Build-Helpers.ps1 -Python python.exe
.\Publish.ps1
.\Release\MinecraftAppleTVBuilder.exe --self-test C:\Temp\builder-selftest.json
```

Build-only validation, using a new destination:

```powershell
.\Release\MinecraftAppleTVBuilder.exe --verify-build C:\Temp\build-report.json --apple-tv C:\Inputs\Minecraft_1.1.5_decrypted.tipa --desktop C:\Inputs\Minecraft-1.1.5.0.Appx --output C:\Temp\ATV212
```

The builder verifies archives, reconstructs the baseline, applies hash-checked byte/UI edits, stamps package revision .212, obtains pinned artwork URLs, packages and signs locally. Generated signing certificates/timestamps differ across machines, so do not expect whole APPX hashes to match another person's output. Use Build-Report.json, installed component hashes and the source recipe to compare relevant content.

The pinned recipe has the exact binary patch spans and UI modifications. Do not recreate a patch using offsets from this prose when the recipe already validates original bytes. Reference source is enough to study the bridge; the full pinned checkout is required for the package recipe, catalog seed, framework packaging and frontend.

## Install separately

Build-only does not install. When ready, extract the generated transfer output and run Install.cmd as the intended Windows user. Certificate trust and loopback steps request elevation; app registration must remain for the intended account. Trust is limited to Local Computer/Trusted People; no hosts-file redirection or global firewall disable is required. A conflicting ordinary Minecraft package shares the Windows identity and is not automatically removed.

Verify the installed revision, launcher entry, bridge executable, XINPUTATV.dll, both x64 frameworks and named loopback exemption. Collect-Diagnostics.cmd performs these checks without signing in.

## Track C: staged live verification

1. Ask the test operator to use the same account in Xbox and Microsoft Store.
2. Launch from Start's Launcher entry; verify preflight logs before interacting with auth.
3. Complete the human-owned device-code sign-in when requested.
4. Check main menu identity, Apple TV achievement list, Store open/close, wallet refresh and item details. Compare server inventory only after authentication.
5. Test a free item only with authorization to add it to that account. Confirm ownership by a fresh read, not by button text.
6. Treat paid-item and real-money tests as separate opt-in operations. Review pending journal/native receipts before any checkout; do not duplicate a charge.
7. Record package/source revision, Windows build, sanitized diagnostic stages, operation, expected and actual outcome. Do not publish raw account data.

## Porting to another engine

Preserve the provider-side concepts, not the numeric addresses. Locate that build's token-result helper, catalog task lifecycle, ownership bindings, image pipeline and UI controller APIs. Confirm ABI, register use, string layout, allocator/destructor pairing, task ownership and thread context. Introduce one hook at a time and capture a read-only baseline. An Apple TV/native ARM build is a different ABI, not another choice of these x64 RVAs.
