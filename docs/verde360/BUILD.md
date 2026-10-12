# Build without a Mac

Push this branch to your GitHub fork and enable Actions. Branch pushes run both
the baseline and fork as separate jobs. Once this workflow is on the default
branch, **Verde360 iOS review build** also offers manual baseline/fork/both runs.
The baseline source is pinned and unmodified; the control checkout supplies
only the workflow's manifest generator. Both use upstream's build/packaging
script. No Apple or upstream attestation secrets are required.

The runner must provide `/Applications/Xcode_26.3.app` on macos-15, matching
upstream's current release workflow. If unavailable, this build fails explicitly;
select an available supported Xcode version deliberately and record its SDK in
the manifest before retrying. Runner availability and compilation are pending.
GitHub Actions quotas/billing depend on your account; no paid runner configured.

Download the Actions artifact named `verde360-{variant}-requires-signing-{run}`.
The IPA inside retains upstream's filename `xenios_ios_iphone_ipad.ipa`.
Verify its SHA-256 against the accompanying manifest.json. **It is ad-hoc signed
and requires provisioning and re-signing before installation on stock iOS.**
Keep the bundled notices with any binary you redistribute.

Equivalent commands on a macOS build host are in the workflow. Upstream
submodules must be initialized at their pinned revisions, and `fetchdata` must
complete before building. The release-publish workflow is not the fork build
route: it needs upstream-specific secrets and publishes to the upstream website.

This Windows checkout has not produced an IPA. A green build is not a gameplay
test. Device results remain pending independently in every generated manifest.
