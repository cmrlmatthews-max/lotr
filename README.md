# Middle-earth Explorer

A 3D map of Tolkien's world in one HTML file, for personal, non-commercial use. It has two sheets:

- **Middle-earth, Third Age.** The north-west of Middle-earth at the time of *The Hobbit* and *The Lord of the Rings*.
- **Beleriand, First Age.** The lost lands of *The Silmarillion*.

The buttons below the title change the sheet. Search finds cards on both sheets. An AI assistant, the loremaster, answers questions from the cards.

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

## Persons, things, and links

- **Persons and creatures.** 259 cards: Hobbits, Men, Elves, Dwarves, Wizards, Valar, enemies, and named creatures of all ages.
- **Things.** 62 cards: rings, jewels, weapons, seeing-stones, ships, books, heirlooms, and plants.
- **Links.** Each person or thing card lists its places with the type of link, for example born, lived, ruled, fought, made, or died. When you open the card, the map marks these places in red and moves to show them. The map changes sheet if most of the places are on the other sheet. Places that are not on the two sheets (for example Valinor and Númenor) show as text.
- **Reverse links.** Each place card lists the persons and things that link to it.
- **Search.** The search box finds persons, things, places, realms, battles, and journeys on both sheets. It also finds other names, for example Strider or Mithrandir.
- **New places.** 68 places that are not in the map data set have a label and a card (52 in Middle-earth, 16 in Beleriand), for example Buckland, the Westfold, the Gap of Rohan, and the Dry River. A plan agent set each position from the books and a review agent examined it. These positions are approximate.
- **Files.** The cards are in `source/cards-lore/`. `master_people.json`, `master_things.json`, and `master_places.json` are the lists. `review_*.md` are the change logs of the review.

## Lore and history

The left panel has a section **Lore and history** with 353 knowledge entries. Search finds them too. They hold what the person, place, and thing cards do not:

- **Chapter summaries.** Each chapter of *The Hobbit*, *The Lord of the Rings* (with the Prologue and the Appendices), and *The Silmarillion*, in the writer's own words. Each chapter card marks its places on the map and links to the chapter before and after.
- **Unfinished Tales and other books.** The parts of *Unfinished Tales*, the other books, and short entries on J.R.R. Tolkien and Christopher Tolkien.
- **Timeline.** 28 dated lists, from the making of the world to the Fourth Age. The years 3018 and 3019 of the Third Age go day by day.
- **Powers, peoples and ideas.** The Valar and Maiar, the fate of Elves and Men, the Rings of Power, the Wizards, kinds of creatures, languages, writing, calendars, customs, and government.
- **Lands beyond the map.** Aman, Númenor, Harad, Rhûn, and other lands that are not on the two sheets.
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

- **Card pictures.** 78 cards have a picture at the top. 24 are things, for example the One Ring, the Arkenstone, Sting, and the Silmarils. Of the other 54: 30 are places (22 in Middle-earth, 8 in Beleriand). 12 are peoples, for example Hobbits, Rohirrim, Dwarves, Ents, Noldor, and Sindar. 12 are battles, for example the Hornburg, the Pelennor Fields, the Battle of Five Armies, and the Fall of Gondolin.
- **Landmark drawings.** The 30 places with a picture also show a small sepia drawing on the map. 16 show at all distances. The other 14 show only when the view is near. The checkbox **Landmark drawings** hides them.
- **Map ornaments.** Each sheet has a drawn border, corner ornaments, a compass rose, a title scroll, ships, and a sea serpent.
- **Woodlands.** Forests have a low raised canopy. Small ink tree crowns fill each forest from edge to edge.
- **Colors.** The sheet uses one sepia paper tone and one grey-brown ink tone. The sea has a faint grey tint and the forests have a faint olive tint. Red marks only battles, journeys, and the selected place. `scripts/regrade.py` makes `base_sepia.jpg` from `base.jpg`.
- **Setting.** The sheet lies on a wooden table in warm light. The panels look like parchment. The app draws the table and the parchment with code.
- **Source of the art.** Google Gemini made the 78 pictures and the 6 ornaments from text prompts written for this map. The prompts describe each place, people, or battle in plain words. They do not name a film, an actor, or an artist. `art/process.py` removes the paper background and makes the card pictures, the sepia map drawings, and the ornaments. The original Gemini images (63 MB) are not in this repo.
- **Accuracy.** The pictures are an impression. They do not show each place as the books describe it in every detail.

## How to read a card

- **Book** text gives only what Tolkien's published books say.
- **Film** text gives what the Peter Jackson films show or change.
- **Series** text gives the same for *The Rings of Power*.
- Each card shows a confidence level and where to read more.

An AI model wrote the card text in its own words. A second model then examined each card and corrected errors. For the 389 person, thing, and new-place cards, the review changed 324 cards and corrected 229 serious errors (a wrong fact, a wrong place link, or a film invention in the book text). The change logs are in `source/cards/review_A.md` to `review_D.md` (Middle-earth) and `source/cards-beleriand/review_X.md` to `review_Z.md` (Beleriand). For the 353 knowledge entries, the review changed 308 entries and corrected 238 serious errors (most often an event told in the wrong chapter, a wrong date, or a wrong name). The change logs are in `source/knowledge/review_know_1.md` to `review_know_8.md`. Errors are still possible. Cards with low confidence need a check against the books.

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
| `source/` | `app.js`, `chat.js`, `template.html`, `build.py`, `package.json`, and the card files in `source/cards/` and `source/cards-beleriand/` |
| `art/` | `out/` (processed images that `build.py` puts in the HTML file) and `process.py` |

`build.py` joins the data, the cards, and the script into the HTML file. It has paths from the build computer. Change the paths at the top before you run it.

## Known limits

- Close views are soft. The relief image has one pixel for each 600 m.
- The data set stops at straight lines in the east, the north, and the south-east. The map shows plain paper there.
- The data set has borders for Gondor, Rohan, and Mordor only. Other realms show a name at their centre.
- Some names in the data set do not come from the books. Their cards say this.
- Card pictures exist for 78 of the 1417 cards. Named persons have no picture.
- 167 of the 321 person and thing cards have medium confidence, and 6 have low confidence. Check these against the books before you rely on them.
- Film and series text is empty on many person and thing cards. The writers left it empty when they were not sure.
- 268 of the 353 knowledge entries have medium confidence, and 0 have low confidence. The writers and the reviewers worked from their knowledge of the books, not from the book text. Check dates and chapter details against the books before you rely on them.
- The loremaster test used a simulated API. No test called the real Anthropic API, because the builder had no key. If the first real question shows an error, the error text says what to do.
- The loremaster can make errors, also in text that it gives a card for. The card is the source: open it to check.
- The file is about 20 MB. The first load can take some seconds.
- Beleriand terrain is modelled, not measured. It is smoother than the Middle-earth terrain.
- Not in this file yet: map sheets for Númenor and Valinor. Persons and things from those lands have cards.
