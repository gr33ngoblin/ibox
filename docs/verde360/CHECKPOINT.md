# Verde360 / iBox checkpoint

## Baseline — 2026-10-12

- Upstream: https://github.com/xenios-jp/XeniOS
- Pinned baseline: `87b176a078c316fde3adf67a217f0c44615b0e0d` (upstream HEAD independently checked).
- Local branch: `verde360/ufc-baseline`; repository folder: `D:\-aiemulators\iBox`.
- Host: Windows, Git 2.47.1.windows.2, Python 3.12. No detected Xcode,
  Apple SDK, CMake, Ninja or Clang. No Apple signing credentials supplied.
- No baseline compile, IPA, device run or performance measurements yet.
- GitHub connector account: gr33ngoblin. Fork creation is not exposed by the
  connector; browser sign-in is pending. Actions availability is not established.
- Submodule revisions are pinned by upstream but their contents are not initialized.
  Local Git's submodule shell failed to resolve its helper commands in this sandbox.

## Repository map and existing capabilities

- Instructions: `.github/CONTRIBUTING.md`, `docs/style_guide.md`, `docs/building.md`;
  no tracked AGENTS.md found.
- BSD 3-clause root license; retain LICENSE and upstream credits. Dependencies
  retain their individual licenses. Release redistribution needs their notices too.
- iOS frontend: `src/xenia/ui/ios/`, `src/xenia/app/xenia_main_ios.mm`.
- ARM64 JIT: `src/xenia/cpu/backend/a64/`; iOS executable-memory support in
  `src/xenia/base/memory_posix.cc`, `cache_control_ios.cc` and iOS JIT broker code.
- Metal: `src/xenia/gpu/metal/`; shared range materialization in
  `src/xenia/gpu/shared_memory.cc`; memexport sizing in `gpu/draw_util.cc`.
- Config: iOS settings catalog/storage and shared cvars/config TOML.
- Patches: `src/xenia/patcher/`, existing iOS per-title patch toggles and persisted
  local TOML overrides. The runtime requires title ID and executable hash matches.
- Existing persistent/async shader controls, presentation cap, guest timing cap,
  touch controls, log viewer, and Metal upload/synchronization counters.
- Apple packaging: `tools/build_apple_release.sh`, `tools/package_ios_ipa.sh`.
  Upstream publish workflow uses macos-15 + Xcode 26.3 and upstream attestation
  and website secrets. Fork builds must not depend on those publish secrets.
- `.gitmodules` pins dependencies including metal-cpp 26, shader converter,
  SPIRV-Cross/Tools, DXC, FFmpeg, SDL3, ZArchive and wxWidgets.

## UFC investigation

Issue 1093 and its comments are external, unverified reports. Reported title ID
5451087D is a discovery hint; the user's media ID, title update and executable
hash remain unknown. Do not substitute the reporter's build identity.

Metal uses AddMemExportRanges too, so oversized estimated ranges are a relevant
investigation lead. However MetalSharedMemory allocates a separate full-size
MTL shared buffer; RequestRanges requests host GPU residency, not a new guest
physical heap allocation. Guest heap fragmentation does not directly explain
failure of that Metal allocation path.

The suggested allocation-size clamp is not accepted as a general fix:
QueryRegionInfo's allocation_size describes the allocation; region_size scans
matching page state/protection. An allocation may contain differently committed
subregions. It also does not prove a GPU export cannot span adjacent allocations.
Shrinking the CPU materialization range does not bound the translated shader's
actual stores. Need trace data and stock/created-fighter comparison before changing
rendering or readback semantics. No compatibility fix or performance gain claimed.

## Pending validation

Unmodified and fork iOS CI builds; entitlement extraction; signing/installation;
script-assisted JIT on iPhone 17 Pro Max iOS 26.0.1; menus; stock fighter; created
fighter; career/tutorial; sustained match. Record frame intervals, game clock
progress versus wall time, shader stutter, memory and thermal state independently.
Any graphics presets or cheats remain unverified until those tests pass.

## Next actions

Create/push GitHub fork once browser or CLI write authentication is available.
Run the manual baseline workflow before the fork workflow. Obtain a signed IPA,
verify JIT first, then conduct one operator test at a time. Keep traces/dumps,
pairing files and credentials outside the repository. No game files bundled.

## Milestone 1 implementation

- Baseline checkpoint: 8fe971eb8.
- Branding: 6ac561555 — distinct display name, bundle ID and launch URL. Upstream
  executable/icon/credits retained; StikDebug uses the actual installed bundle ID.
- Build workflow: 2d1bf8ba5 — manual baseline/fork builds on macOS CI, license
  notices and hashed manifests, no upstream publish/attestation secrets.
- Patch metadata UI: 76c15148f — supported hash list from the active local TOML,
  title ID/filename, explicit relaunch and unverified-toggle messaging.
- Local checks: Python syntax compilation and manifest generation succeeded;
  iOS plist XML/plist parsing succeeded; git diff whitespace check passed.
  Changed Objective-C++ regions formatted using clang-format 23.1.3.
- Additional finding: Metal cache initialization currently hardcodes 1x1 scale.
  Internal display resolution is not the same as guest render-resolution scaling.
  Higher-resolution UI, sharpening, measured presets and performance gains deferred.
- Full iOS compile remains pending CI access. Patch UI runtime behavior remains
  pending; hash mismatch rejection already exists in the upstream runtime.
- No verified UFC cheat addresses introduced. Conflict detection, restore-defaults,
  per-game graphics profiles and additional diagnostics are outstanding work.
- Baseline problems are external reports; no confirmed local/device regression.
- Artifacts: source in D:\-aiemulators\iBox; docs/verde360/BUILD.md,
  INSTALL-JIT.md, CREDITS.md and manifest.json. No IPA artifact exists yet.

## Remote fork and first CI dispatch

- Fork: https://github.com/gr33ngoblin/ibox
- origin is the user's fork; upstream remains xenios-jp/XeniOS. Default fork
  HEAD matched the pinned upstream baseline before changes were pushed.
- Review branch: verde360/ufc-baseline, pushed successfully.
- CI source commit: 8bbc07f117123bdcca5d3b37d39aaff843c5dfcf.
- iOS build run: https://github.com/gr33ngoblin/ibox/actions/runs/38205632933.
  Both jobs passed Xcode/toolchain selection and reached dependency setup.
  Compilation and artifacts still pending at this checkpoint.
- Inherited CI run 38205633091 failed full-tree clang-format 21.1.8 lint on
  unchanged a64_backend.cc and a64_seq_memory.cc. Verified those lines exist
  in the pinned baseline. This is an upstream formatting issue, not evidence
  of a Verde360 runtime regression. Separate iOS workflow is not gated by it.
- GitHub connector cannot create a draft PR in this fork (403 integration
  permission); normal Git push authentication works. The branch remains
  available for review without merging.

## Build artifact and device setup checkpoint

- CI run 38205632933 completed successfully for both baseline and fork.
- Fork built source: 8bbc07f117123bdcca5d3b37d39aaff843c5dfcf.
- Toolchain: Xcode 26.3 (17C529), iPhoneOS SDK 26.2, CMake 4.4.3,
  Ninja 1.13.2, Python 3.14.7, Git 2.55.0, hosted macOS runner.
- Fork IPA downloaded to
  D:\-aiemulators\Verde360-artifacts\fork-build\xenios_ios_iphone_ipad.ipa.
- SHA-256: bdaf4bfb61680dc6121655981b0562eeb1a257c878e21610e1a73f367a867337.
  Matched the CI manifest; plist confirmed Verde360 and the distinct bundle ID.
- Artifact is ad-hoc signed and requires real signing/provisioning through
  iloader or another supported signer. Verde360 installation and JIT are pending.
- Operator reports Luigi's Mansion loads and reaches working gameplay in
  DolphiniOS via StikDebug on the target phone. This supports that app's setup;
  it does not verify Verde360's ARM64 JIT/broker or UFC gameplay.
- SideStore nightly rejected the combined Remote Pairing/Lockdown file as
  ambiguous. A Remote Pairing-only derivative was prepared outside this repo;
  no credentials or raw device logs were added to the repository.
- Baseline device tests, UFC build identity, fighter rendering, performance,
  sustained thermals and gameplay-altering patches remain pending.

## Signing blocker after installation

- Operator installed and launched Verde360 using iloader. StikDebug app
  discovery was subsequently reported working; Verde360 gameplay/JIT is pending.
- Phone screenshot reports missing increased-memory entitlement.
- Verified original artifact XeniOS.signed-entitlements.plist contains the
  increased-memory-limit entitlement. Installed entitlement state differs.
- Current isideload source signs with provisioning-profile entitlements instead
  of preserving all original requests. This is a lead for iloader's behavior,
  not a complete audit of the user's installed signing library version.
- Sideloadly's official changelog lists custom entitlements as a Patreon feature
  requiring Apple Developer Program membership. No free fix claimed.
- User requests no SideStore dependency. Account type and a supported signing
  route remain to be established. No Apple credential changes made.
- Warning wording corrected to explain re-signing, without the upstream app name
  or an unexplained Get More RAM setting. This does not grant the entitlement.

## Free-account signing candidate

- User declines paid Developer Program and requests no SideStore.
- Further signer tracing found isideload already exposes increased_memory_limit
  and requests Apple's INCREASED_MEMORY_LIMIT capability before provisioning.
  Current iloader source calls install_app with that argument false.
- A separate local Windows CLI uses the existing true flag. The attempted
  signature-only library experiment was discarded; isideload library source
  remains unchanged. Local review commit: 5459374 in signing-tools/isideload.
- Executable: D:\-aiemulators\signing-tools\isideload\target\debug\verde360-sign.exe.
  SHA-256: 79305c46b6c9da8524920da02b48dca88c75463be827b2c8c0d1c377dd297a53.
- Windows build passed. Help, rejection of unapproved input before prompting
  for credentials, rustfmt and whitespace checks passed. No account operation
  or phone installation was performed. No credentials supplied to this agent.
- CLI accepts only the verified original IPA hash, hides password/2FA input,
  requires one USB device and retains explicit certificate-revocation selection.
  Its source, MIT license and own manifest remain outside the emulator repo.
- Free-account capability acceptance and installed entitlement status are pending
  the next operator test. Do not claim a resolved signing or memory blocker yet.

## Authentication blocker

- Operator ran the signer; initial Apple GrandSlam login failed with -80045.
  The memory capability request, signing and installation were never reached.
- iloader login also failed. Normal account.apple.com web sign-in succeeded;
  changing the password did not resolve the sideloading login failure.
- Similar public reports: nab138/iloader issues 859 and 864. Comments checked
  contain no verified remedy. These reports support a shared authentication
  route problem but do not identify Apple's exact reason for rejection.
- Preserve installed apps and existing certificates; no revocation, repeated
  password changes or speculative provider/account switching performed here.
- Signer updated to exit with a clear authentication failure instead of unwrap
  panic. Free-account memory grant remains untested. No game results invented.

## ISO mapping diagnostics — 2026-10-13

- Operator reports roughly 5.7 GB ISO. Both app-local and iCloud launches log
  Disc image could not be mapped. ZAR conversion also failed; no conversion
  error details supplied. UFC has not reached verified title-screen/gameplay.
- DiscImageDevice maps the whole file before GDFX verification. Existing log
  cannot distinguish open/fstat/empty-file/mmap failures. File size is virtual
  mapping size, not a claim that all bytes are loaded into resident RAM.
- Added error-only POSIX mapping diagnostics: failing operation, preserved errno,
  error message, file size, requested mapping length, offset and protection.
  Loading semantics unchanged. No speculative RAM entitlement or range fix.
- Formatting and whitespace checks passed. iOS diagnostic build pending CI.
  Existing IPA lacks these diagnostics; no more repeated phone attempts needed
  until a successfully built and installed diagnostic artifact is available.
