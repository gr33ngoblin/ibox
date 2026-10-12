# Verde360 credits and distribution

Verde360 is an independent experimental fork of XeniOS, based on Xenia Edge
and Xenia. This fork does not imply endorsement by their contributors.

Keep the upstream LICENSE, copyright notices and dependency notices with source
and binary distributions. The root license is BSD 3-clause, not a blanket
license for third_party. Upstream app icons and credits are retained at this
milestone. The provisional display name is Verde360; the executable name stays
XeniOS for compatibility with the existing packaging tools.

Fork bundle ID: io.github.gr33ngoblin.verde360. Fork launch URL: verde360://.
Existing upstream xenios:// shortcuts should be recreated for the fork. The
StikDebug handoff reads NSBundle's actual bundleIdentifier, so it targets the
identifier produced by the signer. Assign the JIT script to that installed ID,
especially if SideStore rewrites it during signing.

Do not use upstream release-attestation keys or website publishing credentials.
The fork must be labeled independently and must not claim to be an official
XeniOS build.
