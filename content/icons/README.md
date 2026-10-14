# Pictograms: Health Icons

The app's topic tiles, phrase cards, and answer buttons use icons from
[Health Icons](https://healthicons.org) (resolvetosavelives/healthicons on GitHub), outline
style. The icons are released under **CC0 1.0** (public domain); the project's code is MIT.
Fetched 2026-10-14 from the `main` branch, `public/icons/svg/outline/`.

Only the icons the content references are kept here, one file per icon, named
`<category>__<name>.svg`. Add a new icon by downloading it into this folder and referring to
it from a record as `hi:<category>/<name>` in the `pictogram` field. Plain emoji still work as
a fallback. Build the app's icon map with:

```bash
python3 -m tools.build_icons
```
