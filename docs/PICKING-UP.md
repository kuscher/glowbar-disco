# Picking up

## Where it stands (2026-10-07)
- **1.0 (code 1) is released**: GitHub release v1.0 (`GlowbarDisco.apk`), and on Google Play ("Glowbar Disco Shortcut")
  sent for review on production on 2026-10-07, from the Console (a draft app's first release can't be sent through the
  API). Managed publishing is off (the owner's choice): it goes public as soon as Google approves it. The same bundle
  sits as a draft on closed testing; it was never sent.
- Tested on a Googlebook (x86_64, Android 17): a click opens Glowbar Disco in its own window, a second click brings the
  same window back, no task of ours is left; the right-click item "Privacy policy" opens the policy in the browser.
- The launcher label is "Glowbar Disco"; on Play the title is "Glowbar Disco Shortcut". The icon is white on
  purpose: Google's four colours would read as Google's mark.
- Signing: the app's own key (alias `disco`, SHA-256 `fc5f2a76…bfa9c0`), backed up privately; Play's app signing key
  and upload key are this key; the release workflow reads it from the GitHub environment `release`.
- Devices: Play offers it to the five Googlebook models only (`type.pc` required, minSdk 37); Google Play Games on PC
  is unsupported by the minSdk already.

## Next
- Updates: bump `versionCode`/`versionName`, write `docs/release-notes/<version>.md` and the kit's release notes, tag
  `v<version>`; the workflow uploads a draft to closed testing. Sending it is the owner's call each time.
- Not tried: an arm64 Googlebook (nothing native here, so no difference is expected), the taskbar pin.
