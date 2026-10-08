# Disco: notes for working on the code

An icon that opens Glowbar Disco (`glowbar://disco`, Glowbar's party mode on Googlebooks, which has no launcher icon
of its own). The app does nothing else: no window, no settings, no permissions, no libraries. Keep it that way.

## This repo may go public
Keep out of every file, commit message and release note: device serial numbers and adb names, build numbers and
codenames, what else is installed or open on the owner's devices, the names of his private projects, and where
signing keys are backed up (say "backed up privately").

## Map
- `app/src/main/java/io/github/kuscher/disco/DiscoActivity.kt`: the whole app. `Theme.NoDisplay`, so it never draws;
  it starts `ACTION_VIEW glowbar://disco` with `FLAG_ACTIVITY_NEW_TASK` (Glowbar's own task, so a second click
  brings the same window back), shows a toast if nothing answers, and finishes.
- `AndroidManifest.xml`: `excludeFromRecents`, `noHistory` and an empty `taskAffinity`, so no Disco task is left
  in Recents or on the taskbar. `android.hardware.type.pc` required, for Google Play's device filter.
- The icon: `tools/icon.py` draws it (a mirror ball whose facets mirror the room, the key light and the Glowbar
  below, over Welcome's ink and Glowbar strip) and writes `res/drawable/ic_launcher_{background,foreground,
  monochrome}.xml`. Never edit those by hand: change the script and run `./dc icon`, which also redraws
  `docs/images/icon.png` for the README.

## Build and try
`./dc build [release]`, `./dc app` (build, install, launch), `./dc state` (Disco's and Glowbar's tasks, the
focus), `./dc idle`. It uses Android Studio's JDK and picks the one attached Googlebook (set `ANDROID_SERIAL` when
there are several). Release builds sign with `~/.config/disco/keystore.jks` + `keystore.pass` when they exist.

## Testing on a Googlebook
Check `./dc idle` and the focus first: the devices are in daily use. A launch opens a Glowbar Disco window; close
it afterwards, and leave Glowbar's microphone question unanswered (it is the owner's call).
Status and what's next: `docs/PICKING-UP.md`.
