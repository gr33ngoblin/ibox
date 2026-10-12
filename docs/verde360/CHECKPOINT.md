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
