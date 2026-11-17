# Brief for writers of knowledge entries (Tolkien explorer)

You write knowledge entries for a personal, non-commercial 3D map of J.R.R. Tolkien's world. The map has an AI assistant that answers questions from these entries, and a reader can also search and read them. Accuracy matters more than length.

## Hard rules
1. Write every sentence in your own words. Do NOT quote the books, films, or any wiki. No copied phrases. A summary tells what happens; it never reproduces text.
2. Do NOT invent lore. If you are not sure of a fact, leave it out. A short correct entry is better than a long entry with one error. When the books give more than one account, or Tolkien left a point open, say so plainly.
3. Keep book facts and screen facts apart:
   - "book" = only what Tolkien's published books say (The Hobbit, The Lord of the Rings and its Appendices, The Silmarillion, Unfinished Tales, and where you name it, The Children of Húrin or Tolkien's letters).
   - "film" = Peter Jackson's films (The Lord of the Rings 2001-2003, The Hobbit 2012-2014) and other films you name. Empty string "" if not relevant or you are not sure.
   - "series" = the Amazon series The Rings of Power. Empty string "" if not relevant or you are not sure.
4. Style: plain English, short sentences (25 words or fewer), active voice, no contractions, no slang. Use correct diacritics (Barad-dûr, Lothlórien, Éowyn, Túrin).
5. Dates use "T.A. 3019" (Third Age), "S.A. 1600", "F.A. 455", "Fo.A. 120", "Y.T." (Years of the Trees), and Shire Reckoning as "S.R. 1418" when useful. Give a date only when you are sure of it.
6. "confidence": "high" when every fact is plain in the books; "medium" when some detail comes from later or less certain texts or from your memory of small details; "low" when you are unsure.
7. Do not use web search. Work from your own knowledge. Do not edit any file other than your output file.
8. Output must be one valid JSON list (UTF-8, double quotes, no trailing commas, no comments). After you write the file, run the check command from your task and fix every error it reports.

## What exists already
`/home/claude/me/new/all_index.tsv` lists every card that exists: columns sheet ("me" = Middle-earth in the Third Age, "bel" = Beleriand in the First Age, "-" = no sheet), type (place, realm, battle, people, journey, person, thing), id, title. Read it before you write.
- Do not write an entry about a single subject that already has a card (for example a person, a place, a people such as "Hobbits", or a thing). Your entries cover what the cards do not: chapters, periods, ideas, groups, lists, lands off the map, screen versions, and questions.
- Use the exact ids from this index for "places" and "related".

## Entry format
```json
{"id": "lore:fotr-1-02", "title": "The Shadow of the Past", "group": "The Fellowship of the Ring",
 "kind": "Book I, chapter 2",
 "aka": [],
 "blurb": "One sentence, 25 words or fewer: what this entry is about.",
 "book": "The main text. Short paragraphs separated by \n\n. Length as your task says.",
 "film": "", "series": "",
 "facts": {"Book": "The Fellowship of the Ring", "Dates": "April T.A. 3018"},
 "places": [{"id": "TO050", "role": "other", "note": "Gandalf tells Frodo the history of the Ring at Bag End."}],
 "related": ["person:frodo-baggins", "person:gandalf", "thing:one-ring"],
 "sources": ["The Fellowship of the Ring, Book I, chapter 2"],
 "confidence": "high"}
```
- "id": "lore:" + the prefix from your task + a short slug (lowercase ASCII letters, digits, hyphens). Each id is unique.
- "group": exactly the group name from your task.
- "kind": a short label (2 to 8 words).
- "aka": other names a reader can search by (0 to 5).
- "facts": 0 to 6 short key/value pairs that you are sure of. Values are strings that are not empty.
- "places": 0 to 8 links to map items (type place, realm or battle in the index), where the entry's events happen. "role" is one of: born, lived, ruled, travelled, fought, died, buried, made, kept, found, lost, destroyed, other (use "other" when no other role fits). "note" is one sentence of 20 words or fewer. Never invent an id. Leave the list empty when no place in the index fits.
- "related": 2 to 10 ids of persons (type person), things (type thing) or other cards from the index that the entry is about. Exact ids only.
- "sources": where a reader can find this in the books (book, part, chapter or appendix).

## Final reply (fixed format, nothing else)
`DONE <output file path> | items: <count> | low-confidence ids: <comma list or none> | notes: <one short line>`
