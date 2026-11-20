# Brief for card writers of a new map sheet (Tolkien explorer)

You write reference cards for a personal, non-commercial 3D map of J.R.R. Tolkien's world. A person selects a label on the map and reads your card. An AI assistant in the app also answers questions from your cards. Accuracy matters more than length.

Your task names a **sheet folder** (for example `/home/claude/me/num`). In that folder:
- `data/gaz_index.tsv` lists every mapped feature and region of the sheet: id, name, layer, x_km_east, y_km_north, hint. Use these ids when a field asks for an id. A hint that starts with "approx:" means that the books do not fix the position; the map maker placed it by judgment.
- `slices/slice_NN.json` are the place lists for place writers. `slices/regions.json` is the list of regions.
- `plan.json` holds the plan of the map maker: peoples, battles, journeys (with stages), and notes on doubts.
`/home/claude/me/new/all_index.tsv` lists every card that exists already on the other sheets (sheet, type, id, title), including persons (`person:...`) and things (`thing:...`).

## Hard rules
1. Write every sentence in your own words. Do NOT quote the books, films, or any wiki. No copied phrases. No verse.
2. Do NOT invent lore. If you are not sure of a fact, leave it out. A short correct card is better than a long card with one error. Where Tolkien's texts differ, follow the published Silmarillion and Unfinished Tales, and say in a few words that other versions exist.
3. Keep book facts and screen facts apart:
   - "book" = only what Tolkien's books say (The Silmarillion, Unfinished Tales, The Lord of the Rings and its Appendices; The History of Middle-earth only when you name it as the source).
   - "film" = Peter Jackson's films. They almost never show these lands. Use "" unless you are sure of a real appearance or mention.
   - "series" = the Amazon series The Rings of Power. It shows Númenor at length and Valinor in short scenes. Write what the series shows or changes only when you are sure; otherwise "".
4. A position that the hint marks "approx:" must be called approximate in the card ("The books do not give its exact place."). Do not state a distance or direction that the books do not give.
5. Style: plain English, short sentences (25 words or fewer), active voice, no contractions, no slang. Present tense for descriptions; past tense for history. Use correct diacritics (Númenor, Andúnië, Rómenna, Meneltarma, Ar-Pharazôn, Pelóri, Alqualondë, Fëanor, Eärendil).
6. Dates: "S.A. 3319" (Second Age), "F.A. 455" (First Age), "Y.T." (Years of the Trees), "T.A." (Third Age). Give a date only if you are sure.
7. Do not use web search. Work from your own knowledge. Do not edit any file other than your output file. Put any helper script in the session scratch folder with a file name that starts with your output file name.
8. Output must be valid JSON (UTF-8, double quotes, no trailing commas, no comments). Then run the check command given in your task and correct every problem until it prints OK.

## Place cards: `cards/places_NN.json`
A JSON array with exactly one object for every entry in your slice, same order:
```json
{"id": "<same id as the slice entry>", "title": "<display name with correct diacritics>",
 "kind": "<2 to 5 words, for example 'Royal city of Númenor', 'Haven of the Teleri', 'Mountain range'>",
 "tier": 1,
 "blurb": "<one sentence, 18 words or fewer, says what it is>",
 "book": "<main text. tier 1: 130-210 words. tier 2: 70-120 words. tier 3: 30-60 words. Use \n\n between paragraphs.>",
 "film": "", "series": "",
 "names": {"Meaning": "...", "Other names": "..."},
 "facts": {"Region": "...", "People": "...", "Founded": "...", "Fate": "..."},
 "related": ["<id from gaz_index.tsv, or person:/thing: id from all_index.tsv>"],
 "sources": ["Unfinished Tales, 'A Description of the Island of Númenor'"],
 "confidence": "high"}
```
- tier 1 = a main setting of the tales or a great landmark (about a quarter of a slice). tier 2 = named and important in a tale. tier 3 = minor or named only in passing.
- "book" for tier 1 and 2: what it is and where, who lives or rules there, key history, what happens there in the tales, and its fate.
- "names": 0 to 4 short entries (values 10 words or fewer). "facts": 2 to 5 short entries (values 8 words or fewer). Leave out what you do not know.
- "related": 0 to 6 ids. "sources": 1 to 3 short pointers; add a chapter or part only if you are sure.

## Realm and people cards: `cards/realms.json`
One JSON object `{"realms": [...], "peoples": [...]}`.
- One realm object for every entry of `slices/regions.json`, same ids:
```json
{"id": "RG01", "title": "...", "type": "<copy from regions.json>", "kind": "<2 to 5 words>", "tier": 1, "status": "<short, for example 'Drowned S.A. 3319'>",
 "blurb": "<one sentence, 20 words or fewer>", "book": "<tier 1: 130-200 words; tier 2 or 3: 60-110 words>", "film": "", "series": "",
 "names": {"Meaning": "..."}, "facts": {"Ruler": "...", "Chief place": "...", "People": "..."},
 "peoples": ["people:..."], "related": ["<gaz ids>"], "sources": ["..."], "confidence": "high"}
```
- One people object for every entry of "peoples" in plan.json, same ids and titles:
```json
{"id": "people:...", "title": "...", "kind": "<2 to 5 words>", "blurb": "<one sentence>", "book": "<100-180 words>", "film": "", "series": "",
 "facts": {"Homeland": "...", "Language": "...", "Notable figures": "..."}, "realms": ["RG01"], "related": ["<gaz ids>"], "sources": ["..."], "confidence": "high"}
```

## Battle cards: `cards/battles.json`
A JSON array, one object for every entry of "battles" in plan.json, same ids and titles:
```json
{"id": "battle:...", "title": "...", "date": "...", "year_sort": 3319, "war": "<the larger conflict, or ''>",
 "at": {"near": "<copy 'near' from the plan>", "dx": 0, "dy": 0}, "tier": 1,
 "sides": {"a": ["..."], "b": ["..."]}, "outcome": "<one sentence>",
 "blurb": "<one sentence, 18 words or fewer>", "book": "<110-200 words>", "film": "", "series": "",
 "related": ["<gaz ids, person: ids>"], "sources": ["..."], "confidence": "high"}
```
"year_sort" is a number for ordering within the sheet (use the year; for Years of the Trees use negative numbers in order of time). Copy "at" from the plan; do not move it.

## Journey cards: `cards/journeys.json`
A JSON array, one object for every entry of "journeys" in plan.json, same ids, titles and the same stages in the same order:
```json
{"id": "journey:...", "title": "...", "travellers": "...", "source": "<book>", "dates": "...",
 "blurb": "<one sentence, 22 words or fewer>", "book": "<120-200 words: the whole journey in brief>", "film": "", "sources": ["..."], "confidence": "high",
 "stages": [{"at": {"near": "<copy from the plan>", "dx": 0, "dy": 0}, "title": "<copy or improve the stage title>", "date": "", "note": "<25 to 45 words: what happens at this stage>", "film": ""}]}
```
Copy each stage "at" from the plan (near, dx, dy); do not move a stage.

## Final reply (fixed format, nothing else)
`DONE <output file path> | items: <count> | low-confidence ids: <comma list or none> | notes: <one short line>`
