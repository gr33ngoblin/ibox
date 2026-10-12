# Windows installation and JIT: iPhone 17 Pro Max, iOS 26.0.1

Status: documented candidate route, not verified on this device. No fork IPA has
been built yet. Installing an IPA and activating JIT are separate checks.

## Install SideStore once using Windows

1. Use the current [SideStore prerequisites](https://docs.sidestore.io/docs/installation/prerequisites).
   Install iTunes on Windows (SideStore recommends Apple's direct version;
   Apple Devices is an alternative if the iTunes route fails) and
   [iloader](https://iloader.app), using its official Windows x64 installer.
2. On the phone, install LocalDevVPN from the App Store as linked by SideStore.
   Allow its VPN configuration. Use Wi-Fi for the initial setup.
3. Connect the unlocked phone by USB, tap **Trust**, and enter its passcode.
   Follow [SideStore Install](https://docs.sidestore.io/docs/installation/install)
   in iloader to install SideStore with your Apple Account and generate/import
   its pairing file. Do not send or commit that file, password or certificates.
4. Enable **Settings > Privacy & Security > Developer Mode** when required,
   restart and confirm. If prompted, trust the developer profile under
   **Settings > General > VPN & Device Management**.
5. Open SideStore with LocalDevVPN active and Wi-Fi connected. Confirm SideStore
   refreshes successfully before installing the emulator. A free Apple Account
   normally requires app refreshes every seven days and has sideload limits.

## Install the fork IPA when available

6. Download the **fork** Actions artifact described in BUILD.md, extract the
   archive and save its IPA to the phone's Files app. Compare SHA-256 with the
   build manifest before distributing or installing it.
7. With the SideStore VPN active, open **SideStore > My Apps > +**, choose the
   IPA and finish signing/installing. CI produces an ad-hoc IPA requiring real
   provisioning; no direct-install claim is made. The source bundle ID is
   `io.github.gr33ngoblin.verde360`; check the actual installed identifier if
   the signer rewrites it. The home-screen display name is Verde360.
8. Verify the signed provisioning/entitlements preserve the memory capability
   `com.apple.developer.kernel.increased-memory-limit` where permitted. For
   StikDebug discovery, the installed app needs `get-task-allow`. The repository's
   requested entitlements are not proof that a signer/profile grants them.
   If the app is absent in StikDebug, diagnose signing/discovery before gameplay.

## Candidate JIT route — must be tested

9. Install current [StikDebug](https://github.com/StephenDev0/StikDebug/releases)
   using its official instructions. Use its [pairing guide](https://github.com/StephenDev0/StikDebug-Guide/blob/main/pairing_file.md)
   and the same valid device pairing file where supported. Follow its VPN setup.
10. After restarting the phone, SideStore's guide says to open StikDebug on
    Wi-Fi with VPN connected, force-close it, then reopen to mount the DDI.
    Follow current StikDebug guidance if it differs for your version.
11. Assign bundled `Amethyst-MeloNX.js` or `universal.js` to **the installed
    Verde360 app**, as required by [XeniOS getting started](https://xenios.jp/docs/ios/getting-started).
    If missing, update StikDebug or import its official
    [universal.js](https://github.com/StephenDev0/StikDebug/blob/main/StikJIT/Scripts/universal.js).
    Do not assume generic debugger attachment alone works on this device.
12. Activate the script-assisted JIT route, return to Verde360, and verify its
    JIT status and log before launching UFC. Auto-Enable JIT via StikDebug uses
    NSBundle's installed ID; enable that convenience only after manual success.
    The fork uses `verde360://` launch links rather than upstream `xenios://`.

The [SideStore JIT guide](https://docs.sidestore.io/docs/advanced/jit), read on
2026-10-12, warns iOS 26 has limited app support and does not list XeniOS among
supported apps. XeniOS documents a script route and its code requires a debugger
broker for iOS major version 26+, but neither establishes successful JIT on
iPhone 17 Pro Max / 26.0.1. Ordinary SideStore built-in JIT is not the assumed
route. JIT success is pending a real operator test; do not update/downgrade iOS
as a speculative remedy.

## First operator test only

1. **Readiness check (no game launch):** On the phone open **Settings > General >
   About** and confirm iPhone 17 Pro Max / iOS 26.0.1. Then open SideStore with
   Wi-Fi and LocalDevVPN active and refresh SideStore. Expected: refresh succeeds
   without a signing or pairing error. Reply with the confirmed model/version,
   SideStore and StikDebug versions (or "not installed"), and refresh success or
   the exact error text. If sending a screenshot, crop out Apple Account and
   serial/UDID information. No pairing file or credentials are needed.

Wait for that result before issuing the installation/JIT operator test. This
readiness check does not establish emulator or gameplay compatibility.
