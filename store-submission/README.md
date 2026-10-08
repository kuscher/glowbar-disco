# Store submission kit

Everything Google Play asks for, in the layout the other Googlebook apps use.

- `listing/en-US/`: title (30), short description (80), full description (4000), release notes (500). Check
  lengths with `wc -m`. The release workflow uploads `listing/en-US/release-notes.txt` with each bundle.
- `graphics/icon-512.png`: the launcher icon's visible 72 dp at 512 px, from `./dc icon`.
- `graphics/scenes/`: drawn stand-ins (a desktop, an app list, a lid), no real screen content, from
  `tools/store_scenes.py`.
- `graphics/spec.json` → `graphics/feature-graphic.png` and `graphics/screens/*.png` (1920 × 1080, no alpha), made
  by the shared Play graphics tool (`graphics.js spec.json OUT_DIR`).
- `forms/`: the answers for App content and Data safety; `forms/data-safety.md` is the source for the privacy page.
