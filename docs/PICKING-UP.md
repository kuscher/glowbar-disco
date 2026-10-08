# Picking up

## Where it stands (2026-10-07)
- 1.0 (code 1) works: tested on a Googlebook (x86_64, Android 17), launched with `./dc launch` and by a click on the
  icon in the app list. Glowbar Disco opens in its own window; a second click brings the same window back; no task of
  ours is left behind.
- The launcher label is "Glowbar Disco"; on Play the title is "Glowbar Disco Shortcut".
- Signing: the app's own key (alias `disco`, SHA-256 `fc5f2a76…bfa9c0`), backed up privately; the release workflow
  reads it from the GitHub environment `release`.
- Store kit: `store-submission/` (texts, icon, feature graphic, four screenshots, the App content and Data safety
  answers).

## Next
- Google Play: the app in the Console, Play App Signing with this key (before the first bundle), the App content
  forms, the tag `v1.0`, closed testing, review. Production only on the owner's word.
- Not tried: an arm64 Googlebook (nothing native here, so no difference is expected), the taskbar pin.
