# Middle-earth Explorer

A 3D map of Tolkien's world in one HTML file, for personal, non-commercial use. It has two sheets:

- **Middle-earth, Third Age.** The north-west of Middle-earth at the time of *The Hobbit* and *The Lord of the Rings*.
- **Beleriand, First Age.** The lost lands of *The Silmarillion*.

The buttons below the title change the sheet. Search finds cards on both sheets.

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

## Art and setting

- **Card pictures.** 40 cards have a picture at the top. 29 are places (22 in Middle-earth, 7 in Beleriand). 10 are peoples, for example Hobbits, Rohirrim, Dwarves, and Sindar. 1 is a battle, the Battle of the Hornburg. More battle pictures come in the next update.
- **Landmark drawings.** The 29 places with a picture also show a small sepia drawing on the map. 16 show at all distances. The other 13 show only when the view is near. The checkbox **Landmark drawings** hides them.
- **Map ornaments.** Each sheet has a drawn border, corner ornaments, a compass rose, a title scroll, ships, and a sea serpent.
- **Woodlands.** Forests have a low raised canopy. Small ink tree crowns fill each forest from edge to edge.
- **Colors.** The sheet uses one sepia paper tone and one grey-brown ink tone. The sea has a faint grey tint and the forests have a faint olive tint. Red marks only battles, journeys, and the selected place. `scripts/regrade.py` makes `base_sepia.jpg` from `base.jpg`.
- **Setting.** The sheet lies on a wooden table in warm light. The panels look like parchment. The app draws the table and the parchment with code.
- **Source of the art.** Google Gemini made the 40 pictures and the 6 ornaments from text prompts written for this map. The prompts describe each place, people, or battle in plain words. They do not name a film, an actor, or an artist. `art/process.py` removes the paper background and makes the card pictures, the sepia map drawings, and the ornaments. The original Gemini images (63 MB) are not in this repo.
- **Accuracy.** The pictures are an impression. They do not show each place as the books describe it in every detail.

## How to read a card

- **Book** text gives only what Tolkien's published books say.
- **Film** text gives what the Peter Jackson films show or change.
- **Series** text gives the same for *The Rings of Power*.
- Each card shows a confidence level and where to read more.

An AI model wrote the card text in its own words. A second model then examined each card and corrected errors. The change logs are in `source/cards/review_A.md` to `review_D.md` (Middle-earth) and `source/cards-beleriand/review_X.md` to `review_Z.md` (Beleriand). Errors are still possible. Cards with low confidence need a check against the books.

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
| `source/` | `app.js`, `template.html`, `build.py`, `package.json`, and the card files in `source/cards/` and `source/cards-beleriand/` |
| `art/` | `out/` (processed images that `build.py` puts in the HTML file) and `process.py` |

`build.py` joins the data, the cards, and the script into the HTML file. It has paths from the build computer. Change the paths at the top before you run it.

## Known limits

- Close views are soft. The relief image has one pixel for each 600 m.
- The data set stops at straight lines in the east, the north, and the south-east. The map shows plain paper there.
- The data set has borders for Gondor, Rohan, and Mordor only. Other realms show a name at their centre.
- Some names in the data set do not come from the books. Their cards say this.
- Card pictures exist for 40 of the 675 cards.
- The file is about 15 MB. The first load can take some seconds.
- Beleriand terrain is modelled, not measured. It is smoother than the Middle-earth terrain.
- Not in this file yet: Númenor and Valinor.
