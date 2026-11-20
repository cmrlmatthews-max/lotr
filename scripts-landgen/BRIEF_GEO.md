# Brief for the map maker of a new sheet (Tolkien explorer)

You make the control geometry for one new map sheet of a personal, non-commercial 3D map of J.R.R. Tolkien's world. A script turns your geometry into terrain, a parchment relief image and map labels. Card writers then write a card for each named feature, and reviewers check your positions against the books. Position errors are the main risk of this job. Be exact where the books are exact, and plain about what is a guess.

## Inputs to read first
1. `/home/claude/me/bel/geo.py` — the Beleriand sheet. Your `geo.py` uses the SAME variable names and tuple formats. Read it completely.
2. `/home/claude/me/landgen/terrain.py` and `/home/claude/me/landgen/make_vectors.py` — the scripts that read your file (skim them so that you know what each variable does).
3. `/home/claude/me/new/offmap_names.tsv` — names of places that existing person and thing cards mention as "not on the map".
4. `/home/claude/me/new/all_index.tsv` — every existing card (sheet, type, id, title). Ids of persons and things there can be used in your plan.

## Rules
- Coordinates are km: x east, y north, origin at the south-west corner of the sheet. 1 league = 4.83 km. 1 mile = 1.609 km.
- Write original geometry from what the books SAY (distances, directions, shapes, "north of", "at the mouth of"). Sources in order of authority: The Silmarillion, Unfinished Tales, The Lord of the Rings Appendices; then The History of Middle-earth for points the published books leave open. You can use web search to confirm a fact about position, distance or shape. Use what you find as facts only. Do not trace or copy any published map or atlas drawing.
- Do not invent places. Every named feature must be a name from Tolkien's texts. If a name comes only from The History of Middle-earth or The Nature of Middle-earth, say so in its hint.
- Each hint (the last string of a tuple) is one short phrase for the card writer: what the feature is and the key fact. Start the hint with "approx:" when the books do not fix the position and you placed it by judgment.
- Layers you can use for POINTS: Towns, Harbors, Fortresses, Doors_Gates, Buildings, Bridges, Fords, Cave_entrances, Falls, Graves_Tombs, Islands, Bays, Fields, Valleys, Walls. Ridges use Mountains or Hills. A single peak is a ridge with two points 1 to 3 km apart (see Mount Taras in the Beleriand file).
- Ids: two capital letters and a number, unique in your file (MT01, HI01, RI01, LA01, FO01, SW01, RD01, TO01, HA01, FT01, BU01, GR01, VA01, FI01, IS01, BA01, RG01...). An id that ends in "b" (RI01b) is a second part of the feature with the same number and has no card of its own; give it name None.
- REGIONS: (id, name, 'realm' or 'region', tier 1 to 3, x, y, radius km). Tier 1 = the main lands of the sheet.
- Extra optional variables that the scripts read: `R` (km per pixel of the relief image; use the value in your task), `HSTEP` (km per cell of the height grid; use the value in your task), `ISLANDS` (list of island outlines), `OPEN` (list of sheet edges where land runs off the sheet and fades to plain paper: any of 'N', 'S', 'E', 'W'), `CLOSED_RIDGES` (set of ridge ids that form a closed ring), `PLATEAU_SIGMA` (dict plateau name -> blur in km), `LEVEL` (list of polygons that are level plains), `COAST_NOISE` (0.4 to 1.0: how much the script roughens the coast; use a low value when narrow capes must keep their shape), `BORDERS` (list of (id, name, polygon) drawn as a dashed realm border).
- COAST is the outline of the main land as one polygon. Heights: peak height in metres and half-width in km for each ridge; PLATEAUS add metres inside a polygon.
- Rivers go from source to mouth and must end at the sea, a lake or another river. Roads join the points they serve.

## How to work
1. Write `geo.py` in your sheet folder (given in your task).
2. Run `sh /home/claude/me/landgen/run.sh <your sheet folder>`. It writes `data/preview_labels.jpg` in that folder: the relief with your lines, points and names, and a 200 km grid.
3. Open `data/preview_labels.jpg` with the Read tool and examine it. Check: the shape of the coast, that each mountain range stands where you meant, that rivers run downhill to the sea and do not cross a ridge, that towns sit on the coast or river they belong to, that labels do not pile up, that nothing lies in the sea that must be on land.
4. Correct `geo.py` and run again. Do at least three rounds. Stop when the picture agrees with the texts.

## Second output: `plan.json` in your sheet folder
One JSON object:
```json
{
 "meta": {"name": "<sheet name>", "age": "<for example The Second Age>", "sub": "<one line under the title, 8 words or fewer>",
          "compass": [x, y, r_km], "sea": [["NAME IN CAPITALS", x, y, letter_size_km, letter_gap_km, angle_radians]],
          "orn": {"border": <km>, "corner": <km>, "items": [["ship", x, y, width_km], ["serpent", x, y, width_km]], "cartouche": [x, y, width_km]}},
 "peoples": [{"id": "people:<slug>", "title": "...", "hint": "who they are; which regions they live in", "realms": ["RG01"]}],
 "battles": [{"id": "battle:<slug>", "title": "...", "date": "...", "near": "<feature or region id>", "dx": 0, "dy": 0, "tier": 1, "hint": "what happened; sources"}],
 "journeys": [{"id": "journey:<slug>", "title": "...", "travellers": "...", "dates": "...", "hint": "...",
               "stages": [{"near": "<id>", "dx": 0, "dy": 0, "title": "short stage title", "hint": "what happens here"}]}],
 "offmap_map": {"<name exactly as in offmap_names.tsv>": "<feature or region id on this sheet>"},
 "lore_links": {"<lore id from all_index.tsv, for example lore:land-armenelos>": ["<feature or region id>"]},
 "art": [{"key": "<short lowercase key>", "for": "<feature id, region id, people id or battle id>", "subject": "one sentence that describes the picture in plain words: the place or scene, the land around it, the time of day"}],
 "notes": ["<each position that is a guess, and why; each point where texts differ>"]
}
```
- "meta": put the compass, the sea names, the ship or serpent ornaments and the title cartouche in open sea where they cover no land and no label. Look at the Beleriand values in `/home/claude/me/build/build.py` (search for "LANDS.append") for typical sizes relative to the sheet, and scale them to your sheet.
- "peoples": 4 to 8 peoples or groups of this land. Do not repeat a people that has a card with the same title in all_index.tsv unless this sheet is their main home (then use a new id and a title that names the land, for example "Númenóreans").
- "battles": every fight or violent event on this sheet that the books tell (2 to 6).
- "journeys": 3 or 4 journeys whose main part is on this sheet, each with 4 to 10 stages in order. A stage position is a feature or region id plus an offset in km (dx east, dy north). A journey that arrives from or leaves to another land starts or ends at the sheet edge: use the nearest sea feature with an offset.
- "offmap_map": for each name in offmap_names.tsv that is on your sheet, the id of the feature or region. Leave out names that are not on your sheet.
- "lore_links": for each "Lands beyond the map" lore entry (ids start with lore:land-) that is about a place on your sheet, the 1 to 3 ids it must link to.
- "art": exactly 12 pictures: about 7 places, 2 or 3 peoples, 2 or 3 battles or events. Subjects must be scenes and places, not portraits of named characters. No film scenes.
Validate: `python3 -c "import json;print(json.load(open('<folder>/plan.json')).keys())"`.

## Final reply (fixed format, nothing else)
`DONE <folder> | features with cards: <n> | regions: <n> | approx positions: <n> | notes: <at most three short lines on the main doubts>`
