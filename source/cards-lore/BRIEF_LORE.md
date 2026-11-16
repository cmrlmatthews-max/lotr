# Brief for writers of person, thing and new-place cards (Tolkien explorer)

You write reference cards for a personal, non-commercial 3D map of J.R.R. Tolkien's world. A reader searches a name and reads your card. The card also tells the map which places to mark. Accuracy matters more than length.

## Hard rules (all card types)
1. Write every sentence in your own words. Do NOT quote the books, films, or any wiki. No copied phrases.
2. Do NOT invent lore. If you are not sure of a fact, leave it out. A short correct card is better than a long card with one error.
3. Keep book facts and screen facts apart:
   - "book" = only what Tolkien's published books say (The Hobbit, The Lord of the Rings and its Appendices, The Silmarillion, Unfinished Tales).
   - "film" = how Peter Jackson's films (The Lord of the Rings 2001-2003, The Hobbit 2012-2014) show it or change it. For a person you can name the actor if you are sure. Empty string "" if it does not appear or you are not sure.
   - "series" = how the Amazon series The Rings of Power shows it or changes it. Empty string "" if it does not appear or you are not sure.
4. Style: plain English, short sentences (25 words or fewer), active voice, no contractions, no slang. Past tense is fine for history. Use correct diacritics (Barad-dûr, Lothlórien, Éowyn, Túrin).
5. Dates use "T.A. 3019" (Third Age), "S.A. 1600" (Second Age), "F.A. 455" (First Age), "Fo.A. 120" (Fourth Age), "Y.T." (Years of the Trees). Give a date only when you are sure of it.
6. "confidence": "high" when every fact is plain in the books; "medium" when some detail comes from later or less certain texts; "low" when you are unsure.
7. Do not use web search. Work from your own knowledge. Do not edit any file other than your output file.
8. Output must be one valid JSON list (UTF-8, double quotes, no trailing commas, no comments). After you write the file, run the check command given in your task and fix every error it reports.

## The map index
`/home/claude/me/new/map_index.tsv` lists every item on the two map sheets: columns land ("me" = Middle-earth in the Third Age, "bel" = Beleriand in the First Age), type (place, realm, battle, people, journey), id, title, layer, x_km, y_km. New places that other writers add at this time are in `/home/claude/me/new/master_places.json` (ids NP001... and b:NP001...).
Read the index before you write. When a card links to a place, it uses the exact `id` from the index or from master_places.json (for example "TO050", "realm:the-shire", "b:TO01", "b:RG01", "battle:...", "NP014"). Only ids with type place, realm or battle are valid links. Never invent an id.

## Person card (also for named creatures)
```json
{"id": "person:frodo-baggins", "title": "Frodo Baggins", "group": "Hobbits",
 "kind": "Hobbit of the Shire, Ring-bearer",
 "aka": ["Mr. Underhill", "Ring-bearer"],
 "blurb": "One sentence, 25 words or fewer: who this is.",
 "book": "3 to 6 short paragraphs separated by \n\n: who they are, their line or kin, what they did in order of time, how their story ends. 120 to 260 words for a major person, 60 to 120 for a minor one.",
 "film": "", "series": "",
 "facts": {"Race": "Hobbit", "Born": "T.A. 2968", "Died": "", "Parents": "", "Spouse": "", "Children": "", "Realm or home": ""},
 "places": [{"id": "TO050", "role": "lived", "note": "Lives at Bag End from T.A. 2989 to 3018."}],
 "offmap": [{"name": "Valinor", "role": "other", "note": "Sails west from the Grey Havens in T.A. 3021."}],
 "related": ["person:samwise-gamgee", "thing:the-one-ring"],
 "sources": ["The Lord of the Rings", "The Lord of the Rings, Appendix B"],
 "confidence": "high"}
```
- Use the id, title and group from the master list exactly. "kind" is a short label (3 to 7 words).
- "aka": other names and titles the books use (0 to 6). A reader can search by these.
- "facts": only keys you can fill with certainty. Remove a key if you do not know the value. Allowed keys: Race, Born, Died, Age at death, Parents, Spouse, Children, Siblings, House or line, Title, Realm or home, Weapon or steed, Made by, Kind.
- "places": 2 to 10 links for a major person, 1 to 4 for a minor one, in order of time. Each link is a place where the person did something that the books state. "role" is one of: born, lived, ruled, travelled, fought, died, buried, made, kept, found, lost, destroyed, other. "note" is one sentence, 20 words or fewer, that says what happened there. Link the most exact place that exists in the index (the town before the realm). Link a battle id when the person fought in that battle. Use a realm id only when no smaller place fits. Do not link a place only because it is near.
- "offmap": places that are not on the two sheets (for example Valinor, Númenor, Harad, Rhûn, the far north, the Blue Mountains in the Third Age if not in the index), same fields with "name" in place of "id". 0 to 4 entries.
- "related": 2 to 8 ids of other persons and things from `/home/claude/me/new/master_people.json` and `/home/claude/me/new/master_things.json` (exact ids). Never invent an id.

## Thing card
Same fields as a person card, with these differences: id "thing:...", "group" from the master list, "kind" such as "Ring of Power" or "Sword of the kings of Gondor". "book" tells what it is, who made it and when, who held it in order, what it did, and what became of it (80 to 220 words). "facts" allowed keys: Kind, Made by, Made in, Date made, Material, Owners, Fate. "places" roles made, kept, found, lost, destroyed, other fit best: where it was made, kept, found, lost and destroyed, in order of time. "related": the makers and holders (person ids) and linked things.

## New-place card
```json
{"id": "NP014", "title": "Bywater", "land": "me", "layer": "Towns", "tier": 2, "x": 556.0, "y": 1424.0,
 "kind": "Village of the Shire",
 "blurb": "One sentence, 25 words or fewer.",
 "book": "2 to 4 short paragraphs separated by \n\n, 60 to 160 words: what it is, where it lies, what happens there.",
 "film": "", "series": "",
 "names": {"Sindarin": "", "English": ""},
 "facts": {"Realm": "The Shire", "Location": "Westfarthing, on the Water east of Hobbiton"},
 "related": ["TO050", "person:samwise-gamgee"],
 "sources": ["The Lord of the Rings, Book VI"],
 "confidence": "high"}
```
- Copy id, title, land, layer, tier, x and y from master_places.json exactly. Do not change a position.
- "names": only names in other tongues or their meaning that you are sure of; remove the field if there is none.
- "facts": 2 to 4 keys you are sure of (Realm, Location, Built by, Date, Meaning, Kind).
- "related": 1 to 6 ids: nearby or linked map items from the index, and persons or things from the master lists.

## Final reply (fixed format, nothing else)
`DONE <output file path> | items: <count> | low-confidence ids: <comma list or none> | notes: <one short line>`
