# UI notes: Middle-earth Explorer

Pass of 21 November 2026. It applies the High and Medium items of the UI audit (commit b99a538) and connects the app to the shared library (`/shared-ui/`).
Edit `source/template.html` (CSS and markup), `source/app.js`, and `source/chat.js`, then rebuild `index.html` with `source/build.py`. Never edit `index.html` by hand.

## Accepted exception: text colors stay below 4.5:1

By the owner's decision, no text color and no text opacity changed in this pass. The parchment look stays. These pairs stay below the 4.5:1 rule on purpose.
Ratios are from the audit, measured on flat paper `#e6dabb` (the real panels carry a noise texture, so values are approximate).

| Text | Color | Ratio | Where |
|---|---|---|---|
| Muted brown | `#7a6a50` | 3.77 | `.groups summary em`, `.links .onsheet` |
| Lighter brown | `#8a7a5e` | 3.01 | `.msg .meta`, compass needle |
| Paper on gold | `#e6dabb` on `#a07c34` | 2.78 | `.series .tag`, `.part.beyond>.tag`, Series tag in the menu and About |
| Gold on results fill | `#a07c34` on `#fbf3d8` | 3.48 | `#results .ty-lore` |
| Realm region labels | `#6a5740` at opacity .7 | about 2.83 | `.lbl.realm.region` |
| Realm labels | `#55412a` at opacity .7 | about 3.49 | `.lbl.realm` (passes 3:1 only for the 20 px size) |

Text sizes did change (see below). Control edges and the focus ring are not text and do meet 3:1.

## What this pass changed

- Fix 1, journey bar: the bar no longer sits at a fixed center with a 420 px minimum. From 1180 px up it fills the free map area between the panel and the card (max 620 px). Between 901 and 1179 px (desktop, iPad landscape) it docks in the card column under the card, and the card gets shorter while a journey runs (`--jbh` from a ResizeObserver). On a landscape phone the round buttons move to the right side while a journey runs.
- Fix 2, sizes: every text size below 12 px is now 12 px. Control borders (`.chip`, `#lands button`, `#journeys button`, sheet handle) use `--edge` (4.23:1).
- Fix 3, focus: one two-tone ring (cream inside, red outside) on every `:focus-visible`. The canvas is no tab stop (it has `role="img"` and a label). Closed drawer, card, journey bar, and chat use `visibility:hidden`, so Tab cannot reach them. Links made from `<a data-go>` without `href` now get `tabindex="0"` and Enter or Space.
- Fix 4, reduced motion: CSS durations are 0 (tokens plus a global override). Camera fly-to and tilt jump, damping is off, and the map offset does not ease. The setting is read again when it changes.
- Fix 5, Escape: closes about, chat, phone menu, journey or card, search results, one per press. Dialogs have `role="dialog"` and a name, focus moves in on open and returns on close. Background controls are `inert` behind a modal layer.
- Fix 6, touch targets: 44 px on the phone layout and on any coarse pointer (`body.coarse`). Stage markers and the sheet handle have a 44 px hit area around a smaller visual.
- Fix 8, first-visit hint: sits beside the round buttons, closes on the first canvas press or after 6 s.
- Fix 9, state: `?land=`, `?card=`, `?layers=` are written with `history.replaceState`. `?q=` and `?phone=` still work. The last camera is saved in `me-explorer.view` and restored with no animation when the address has no card.
- Fix 10, ARIA: `aria-pressed` on sheet and journey buttons, `aria-expanded` on the menu button, a live region for search count and journey stage, a combobox and listbox for search, labels on the search field, chat field, and canvas.
- Fix 11, loader: a `<progress>` bar driven by real boot stages (art decode, image decode, terrain, labels, panel).
- Fix 12, pinch: card, menu scroll area, chat log, and About dialog allow the browser text zoom. The map canvas keeps its own pinch. The Safari gesture block applies only to the canvas.
- Service worker: cache name `lotr-explorer-v2`, old caches deleted on activate, page request revalidates with the server (`cache: no-cache`), shared files cached at run time.
- `dvh`: every `vh` fallback has a `dvh` line after it.
- Shared library: `/shared-ui/tokens.css` and `/shared-ui/shell.js` load before the app. `SharedUI.init`, `resume.set` (land change, card open), and the hub link in the menu. Without the files the app still runs; every token has a literal fallback.

## What remains

- Skipped by decision: zoom and rotate buttons (audit item 7).
- Low items not done: 13 (type scale and `!important`), 15 (placeholder cut at 288 px, empty wood on phone first screen, iPad portrait layout), 17 (a Places list in the menu), and the rest of 16 (stale-while-revalidate for the 24 MB page, service worker on `localhost`, a MediaQueryList `change` listener).
- Inline text links in prose (About, API key note) stay under 44 px high, as the rule allows for inline links.
- Stage markers on a dense journey can sit closer than 44 px, so their hit areas overlap there. The stage list in the card and the previous and next buttons are the alternative.
- Not testable here (from the audit): real iPhone Safari (safe-area insets, Home Screen mode, `gesturestart`, text pinch, keyboard), real network load time of the 24 MB file, VoiceOver and TalkBack, exact contrast of text over the parchment texture and the 3D map, real two-finger gestures, tap targets of every map label, offline use of the installed app.
