# PIM-PAM Digital Workspace

A single Dash app that aggregates three World Bank PIM-PAM tools \u2014 **PIA**,
**GoAT**, and the **Country Benchmarking Dashboard (CBD)** \u2014 behind one
"workbench," so a user can move between them without separate tabs or links.

## Files

| File | Purpose |
|---|---|
| `app.py` | Layout + callbacks. Run this. |
| `constants.py` | All tool/country data, URLs, and color tokens. Edit this to add a tool or a PIA country. |
| `utils.py` | Component builders (cards, tabs, iframe wrapper) used by `app.py`. |
| `assets/style.css` | Dark theme, loosely inspired by the PIM-PAM marketing site's palette (`#0A0E1A` background, indigo/teal/green/orange accents, Fira Sans + Inter). No logos are used anywhere. |

## Running it

```bash
pip install dash
python app.py
```

Then open `http://127.0.0.1:8050/`.

## How PIA's five countries are handled

PIA is one Posit Connect deployment that serves five countries through a
query string: `?country=zambia`, `?country=malawi`, etc. Rather than listing
five separate hyperlinks (which is what the brief asked to avoid), the
workbench shows PIA as **one tool** with a **country switcher**: a row of
pill-shaped buttons (not links) that update a `dcc.Store`, which in turn
re-renders the embedded `<iframe src=...>` with the right query string. The
map/analysis view underneath stays in the same visual frame the whole time \u2014
switching Zambia to Nepal feels like changing a filter, not navigating to a
new page.

`pia_url_for()` in `constants.py` is the single place that builds this URL;
add a country by adding one entry to `PIA_COUNTRIES`.

## A note on iframes

GoAT, CBD, and PIA are embedded live via `<iframe>` rather than re-built or
screenshotted, so the workspace always reflects the real, current tool. Some
Posit Connect / World Bank deployments may set `X-Frame-Options` or
`Content-Security-Policy: frame-ancestors` headers that block embedding from
an external origin. If an embed renders blank, use the "Open full window"
link shown above each embed \u2014 it opens the exact same URL directly. If you
control the Posit Connect deployment settings, allow-listing this
workspace's origin in the frame policy will let the embed render normally.

## Extending

- **Add a tool:** add an entry to the `TOOLS` list in `constants.py` with a
  `kind` of `"simple"` (single URL) and it will automatically get a hero
  card, a workbench tab, and an embed \u2014 no changes to `app.py` needed.
- **Add a PIA country:** add an entry to `PIA_COUNTRIES` in `constants.py`.
- **Restyle:** all colors are CSS custom properties at the top of
  `assets/style.css` (`--bg`, `--surface`, `--accent-1` etc.) so a palette
  change is a find-and-replace in one place.