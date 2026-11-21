# Middle-earth Explorer

A 3D map of Tolkien's world in one HTML file, for personal, non-commercial use. It has four sheets:

- **Middle-earth, Third Age.** The north-west of Middle-earth at the time of *The Hobbit* and *The Lord of the Rings*.
- **Beleriand, First Age.** The lost lands of *The Silmarillion*.
- **Númenor, Second Age.** The island of the Dúnedain before the Downfall.
- **Aman, Years of the Trees.** Valinor, Eldamar, Tol Eressëa, and the Pelóri while the Two Trees gave light.

The buttons below the title change the sheet. Search finds cards on all sheets. An AI assistant, the loremaster, answers questions from the cards.

## Open the map

- **On the web:** https://cmrlmatthews-max.github.io/lotr/ (when GitHub Pages is on for this repo).
- **On your computer:** download `index.html` and double-click it. It is one file and it works without an internet connection.
- If the map moves slowly on an older computer, add `?q=2` to the end of the address. This halves the terrain detail.

## Controls

| Action | Result |
|---|---|
| Drag | Move the map |
| Scroll or pinch | Zoom |
| Shift-drag or right-drag | Turn and tilt |
| Click a name | Open the card |
| Double-click a name or the land | Fly to that point |
| `/` | Search |
| `Esc` | Close the card or the journey |
| `Space`, `←`, `→` | Play a journey, go to the previous or next stage |

## On an iPhone

The page changes its layout when the screen is narrower than 900 px. This includes an iPhone, and an iPad that you hold upright.

- **Top bar.** The menu button (three lines) opens the sheets, the layers, the journeys, and the lists. The search field is in the middle. **Ask** opens the loremaster.
- **Card.** A card comes up from the bottom to half height. Drag the handle up for the full card, or down to make it small. Tap the handle to change between half and full.
- **Round buttons** (right side): **2D / 3D** changes between a view from above and a tilted view. The **compass** turns north to the top. The last button shows the whole map.

| Fingers | Result |
|---|---|
| One finger, drag | Move the map |
| Two fingers, pinch | Zoom |
| Two fingers, turn | Turn the map. The map follows your fingers. |
| Two fingers, move up or down together | Tilt the map |
| Tap a name | Open the card |

The first visit shows these gestures in a short note. **About** has a link that shows the note again.

**Home Screen app.** Open the web address in Safari. Tap **Share**, then **Add to Home Screen**. The map then opens full screen from its own icon. After one visit with a connection, the map also opens without a connection. The loremaster always needs a connection.

**Lighter graphics.** On a phone the page uses half the terrain detail, a smaller relief image, and no edge smoothing. Add `?q=1` to the address for full terrain detail.

## Contents: Middle-earth

- **Terrain.** A 2 km height grid with a 600 m parchment relief image. Relief is exaggerated 15 times. The factor decreases when you zoom in.
- **Places.** 401 cards: towns, strongholds, halls, bridges, mountains, forests, rivers, roads.
- **Realms and peoples.** 37 realms and regions, 23 peoples.
- **Battles.** 33 battles, from S.A. 1697 to T.A. 3019.
- **Journeys.** 9 routes with stages. Frodo's route uses the line from the map data set. The other routes are curves through the stage points.

## Contents: Beleriand

- **Terrain.** No survey data exists for Beleriand. The terrain is an original model made for this map from the descriptions in the books. `scripts-beleriand/geo.py` holds the coasts, ridges, rivers, and place positions. `terrain.py` makes the relief from them.
- **Accuracy.** The layout follows the distances that the books give (for example Dorthonion 60 leagues wide, Sirion 130 leagues long, Angband 150 leagues from Menegroth). A review agent compared the layout with the books, and I applied its corrections. Positions are still approximate.
- **Cards.** 97 places, 27 realms and regions, 18 peoples, 22 battles, and 8 journeys (for example Beren and Lúthien, Túrin, Tuor, and the return of the Noldor). All eight routes are curves through the stage points.

## Contents: Númenor

- **Terrain.** The terrain is an original model from "A Description of the Island of Númenor" in *Unfinished Tales*. The land is a five-pointed star. The Mittalmar in the middle is about 250 miles across. Five promontories, each about 100 miles wide and more than 200 miles long, reach out from it. `scripts-numenor/geo.py` holds the geometry.
- **Accuracy.** A review agent compared each position with the books. It found 3 errors and I corrected them. The largest: the three small bays of the Andustar face west, not north. The exact bearing of each promontory, and the distances between the Meneltarma, Armenelos, and Rómenna, are a judgment.
- **Descriptive names.** 11 features have a descriptive name (for example "Forests of Hyarrostar"), because the text describes them and does not name them. Their cards say so.
- **Cards.** 40 places, 10 regions, 7 peoples, 4 events (for example the Downfall of Númenor), and 4 journeys (for example Aldarion and Erendis, and the last days of Númenor).

## Contents: Aman

- **Terrain.** The books give no detailed map of Aman. The terrain is a model from the text of *The Silmarillion*, with *The History of Middle-earth* where the published book is silent. `scripts-aman/geo.py` holds the geometry. The relief is coarse in close views: one pixel for each 1 km.
- **Accuracy.** A review agent compared each position with the books. I applied its 9 corrections. For example, I removed three invented rivers and one invented name, and I added the Door of Night. Many positions are approximate: the Gardens of Lórien, the Halls of Mandos, the Halls of Nienna, the Mansions of Aulë, the Wells of Varda, the Caves of the Forgotten, and the Door of Night. Their cards say so.
- **Time.** The sheet shows the Years of the Trees. Some places are of a later time, for example Avallónë, the Enchanted Isles, and the landing of Ar-Pharazôn. Their cards say so.
- **Cards.** 29 places, 9 regions, 5 peoples, 4 events (for example the Darkening of Valinor and the Kinslaying at Alqualondë), and 4 journeys (for example the Flight of the Noldor and the voyage of Eärendil).
- **Links.** 45 person and thing cards link to exact places on the two new sheets (for example Fëanor to Tirion and Formenos, and Elendil to Rómenna). Links that said "Valinor" or "Númenor" as text now point to the map.

## Persons, things, and links

- **Persons and creatures.** 259 cards: Hobbits, Men, Elves, Dwarves, Wizards, Valar, enemies, and named creatures of all ages.
- **Things.** 62 cards: rings, jewels, weapons, seeing-stones, ships, books, heirlooms, and plants.
- **Links.** Each person or thing card lists its places with the type of link, for example born, lived, ruled, fought, made, or died. When you open the card, the map marks these places in red and moves to show them. The map changes sheet if most of the places are on the other sheet. Places that are not on the two sheets (for example Valinor and Númenor) show as text.
- **Reverse links.** Each place card lists the persons and things that link to it.
- **Search.** The search box finds persons, things, places, realms, battles, and journeys on all sheets. It also finds other names, for example Strider or Mithrandir.
- **New places.** 68 places that are not in the map data set have a label and a card (52 in Middle-earth, 16 in Beleriand), for example Buckland, the Westfold, the Gap of Rohan, and the Dry River. A plan agent set each position from the books and a review agent examined it. These positions are approximate.
- **Files.** The cards are in `source/cards-lore/`. `master_people.json`, `master_things.json`, and `master_places.json` are the lists. `review_*.md` are the change logs of the review.

## Lore and history

The left panel has a section **Lore and history** with 353 knowledge entries. Search finds them too. They hold what the person, place, and thing cards do not:

- **Chapter summaries.** Each chapter of *The Hobbit*, *The Lord of the Rings* (with the Prologue and the Appendices), and *The Silmarillion*, in the writer's own words. Each chapter card marks its places on the map and links to the chapter before and after.
- **Unfinished Tales and other books.** The parts of *Unfinished Tales*, the other books, and short entries on J.R.R. Tolkien and Christopher Tolkien.
- **Timeline.** 28 dated lists, from the making of the world to the Fourth Age. The years 3018 and 3019 of the Third Age go day by day.
- **Powers, peoples and ideas.** The Valar and Maiar, the fate of Elves and Men, the Rings of Power, the Wizards, kinds of creatures, languages, writing, calendars, customs, and government.
- **Lands beyond the map.** Harad, Rhûn, and other lands that are not on the sheets. The entries for Aman and Númenor link to the two new sheets.
- **Lines and lists.** Family lines and lists of kings, stewards, ring-bearers, and more.
- **Films and series.** The Peter Jackson films, the main changes from book to film, *The Rings of Power*, and older screen and radio versions.
- **Questions readers ask.** Answers from the books to common questions. Each answer says when the books leave the question open.

Each place card lists the chapters and lore entries that link to it. The entries are in `source/knowledge/`.

## The loremaster (AI assistant)

Select **Ask the loremaster** to ask a question in your own words, for example "Who killed the Witch-king, and where?".

- **What it is.** The loremaster is an AI model: Claude, made by Anthropic. The page calls Anthropic's API from your browser. The assistant needs an internet connection. The map and the cards work without one.
- **Your own key.** The assistant needs your own Anthropic API key. Get a key at https://platform.claude.com/. Select **Key**, paste the key, then select **Save**. Anthropic bills each question to your account.
- **Where the key goes.** The key stays in your browser. The page sends it only to `api.anthropic.com`, with your question and the text of the cards that fit it. The key is not in the HTML file and not in this repository. **Forget key** removes it.
- **Shared storage.** A remembered key is in the storage of the web address. Other pages on the same address (for GitHub Pages: all projects of the same account) can read it. Clear the box "Remember the key in this browser" to keep the key only until you close the page.
- **How it answers.** The page finds the 10 cards that fit the question best and sends them with the question. The model can search the cards up to four more times. Text below **From the cards** comes from the cards; each small button opens its source card. Text below **Beyond the cards** comes from the model's own knowledge of the books. No one reviewed that text. Check it against the books.
- **The map.** A name with a dotted border opens its card and moves the map. **Show these places on the map** marks the places of an answer in red.
- **Models and cost.** Claude Haiku 5.5 is the default (fast, lowest cost). Claude Sonnet 5.5 gives deeper answers at a higher cost. At the prices of November 2026, one question costs about $0.001 to $0.003 with Haiku 5.5 and about $0.02 to $0.05 with Sonnet 5.5. Each answer shows its token count and an approximate cost.
- **Files.** The assistant code is `source/chat.js`.

## Art and setting

- **Card pictures.** 102 cards have a picture at the top. 24 are on the Númenor and Aman sheets (13 places and regions, 4 peoples, 7 events). 24 are things, for example the One Ring, the Arkenstone, Sting, and the Silmarils. Of the other 54: 30 are places (22 in Middle-earth, 8 in Beleriand). 12 are peoples, for example Hobbits, Rohirrim, Dwarves, Ents, Noldor, and Sindar. 12 are battles, for example the Hornburg, the Pelennor Fields, the Battle of Five Armies, and the Fall of Gondolin.
- **Landmark drawings.** The 30 places with a picture also show a small sepia drawing on the map. 16 show at all distances. The other 14 show only when the view is near. The checkbox **Landmark drawings** hides them.
- **Map ornaments.** Each sheet has a drawn border, corner ornaments, a compass rose, a title scroll, ships, and a sea serpent.
- **Woodlands.** Forests have a low raised canopy. Small ink tree crowns fill each forest from edge to edge.
- **Colors.** The sheet uses one sepia paper tone and one grey-brown ink tone. The sea has a faint grey tint and the forests have a faint olive tint. Red marks only battles, journeys, and the selected place. `scripts/regrade.py` makes `base_sepia.jpg` from `base.jpg`.
- **Setting.** The sheet lies on a wooden table in warm light. The panels look like parchment. The app draws the table and the parchment with code.
- **Source of the art.** Google Gemini made the 102 pictures and the 6 ornaments from text prompts written for this map. The prompts describe each place, people, or battle in plain words. They do not name a film, an actor, or an artist. `art/process.py` removes the paper background and makes the card pictures, the sepia map drawings, and the ornaments. The original Gemini images (63 MB) are not in this repo.
- **Accuracy.** The pictures are an impression. They do not show each place as the books describe it in every detail.

## How to read a card

- **Book** text gives only what Tolkien's published books say.
- **Film** text gives what the Peter Jackson films show or change.
- **Series** text gives the same for *The Rings of Power*.
- Each card shows a confidence level and where to read more.

An AI model wrote the card text in its own words. A second model then examined each card and corrected errors. For the 389 person, thing, and new-place cards, the review changed 324 cards and corrected 229 serious errors (a wrong fact, a wrong place link, or a film invention in the book text). The change logs are in `source/cards/review_A.md` to `review_D.md` (Middle-earth) and `source/cards-beleriand/review_X.md` to `review_Z.md` (Beleriand). For the 353 knowledge entries, the review changed 308 entries and corrected 238 serious errors (most often an event told in the wrong chapter, a wrong date, or a wrong name). The change logs are in `source/knowledge/review_know_1.md` to `review_know_8.md`. For the 116 cards and 46 link sets of the Númenor and Aman sheets, the review changed 74 and corrected 34 serious errors. The change logs are in `source/cards-numenor/` and `source/cards-aman/` (`review_places.md`, `review_realms_events.md`, and `geo_review.json` for positions). Errors are still possible. Cards with low confidence need a check against the books.

## Map data and license

- Terrain and map layers: Rose, Robert A. (2020), *GIS & Middle Earth Presentation & Data Set*, William & Mary. https://doi.org/10.21220/RKEZ-X707. This data builds on the ME-DEM project.
- License: Creative Commons Attribution-NonCommercial-ShareAlike 4.0 (CC BY-NC-SA 4.0).
- The reduced terrain and the vector layers in this folder are an adaptation of that data set. They keep the same license. Give the same credit if you share the file. Do not use it for commercial work.
- 3D engine: three.js (MIT license).
- Pictures and ornaments: made with Google Gemini for this map. Each Gemini image has an invisible SynthID watermark that marks it as AI-made.
- Middle-earth and its names are the creation of J.R.R. Tolkien. This project has no connection with the Tolkien Estate, the publishers, or the film and series makers.

## Folder contents

| Path | Contents |
|---|---|
| `index.html` | The map. This is the only file that you need. |
| `data/` | Reduced Middle-earth data: `height.png`, `base.jpg`, `base_sepia.jpg`, `vectors.json`, `gazetteer.json` |
| `scripts/` | `terrain.py`, `vectors.py`, and `regrade.py`. They make `data/` from the William & Mary downloads (4.9 GB, not in this repo; see the link above). |
| `data-beleriand/`, `scripts-beleriand/` | The modelled Beleriand data and the scripts that make it |
| `data-numenor/`, `data-aman/` | The modelled data of the two new sheets |
| `scripts-numenor/`, `scripts-aman/` | `geo.py` (the control geometry) for each new sheet |
| `scripts-landgen/` | The sheet generator: `terrain.py`, `make_vectors.py`, `preview.py`, `run.sh`, the briefs for the agents, and `check_cards.py` |
| `icon-*.png`, `manifest.webmanifest`, `sw.js` | The Home Screen files: the icons, the app description, and the service worker that keeps the offline copy |
| `source/` | `app.js`, `chat.js`, `template.html`, `build.py`, `package.json`, and the card files in `source/cards/`, `source/cards-beleriand/`, `source/cards-numenor/`, and `source/cards-aman/` |
| `art/` | `out/` (processed images that `build.py` puts in the HTML file) and `process.py` |

`build.py` joins the data, the cards, and the script into the HTML file. It has paths from the build computer. Change the paths at the top before you run it.

## Known limits

- Close views are soft. The relief image has one pixel for each 600 m.
- The data set stops at straight lines in the east, the north, and the south-east. The map shows plain paper there.
- The data set has borders for Gondor, Rohan, and Mordor only. Other realms show a name at their centre.
- Some names in the data set do not come from the books. Their cards say this.
- Card pictures exist for 102 of the 1533 cards. Named persons have no picture.
- 167 of the 321 person and thing cards have medium confidence, and 6 have low confidence. Check these against the books before you rely on them.
- Film and series text is empty on many person and thing cards. The writers left it empty when they were not sure.
- 268 of the 353 knowledge entries have medium confidence. The writers and the reviewers worked from their knowledge of the books, not from the book text. Check dates and chapter details against the books before you rely on them.
- The loremaster test used a simulated API. No test called the real Anthropic API, because the builder had no key. If the first real question shows an error, the error text says what to do.
- The loremaster can make errors, also in text that it gives a card for. The card is the source: open it to check.
- The Aman sheet is a model with little support from the books. Do not use it as a source for where a place is.
- 63 of the 116 map cards on the two new sheets have medium confidence, and 7 have low confidence.
- The phone layout was tested in a simulated iPhone only (Chromium with touch emulation). No test used a real iPhone, Safari, or the Home Screen mode.
- The file is about 24 MB. The first load can take some seconds.
- Beleriand terrain is modelled, not measured. It is smoother than the Middle-earth terrain.
