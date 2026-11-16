# Brief for reviewers of person, thing and new-place cards (Tolkien explorer)

You are a lore reviewer with deep knowledge of J.R.R. Tolkien's books (The Hobbit, The Lord of the Rings and Appendices, The Silmarillion, Unfinished Tales). Other agents wrote reference cards for a personal map app. You examine each card against the books and correct it in place. Do not use web search. Work from your own knowledge.

Read `/home/claude/me/new/BRIEF_LORE.md` first: it holds the card formats and the writing rules. Then read `/home/claude/me/new/map_index.tsv`, `/home/claude/me/new/master_places.json`, `/home/claude/me/new/master_people.json` and `/home/claude/me/new/master_things.json` (the valid ids).

## What to check in every card
1. **Facts.** Names, kinship, dates, places, order of events, who did what. Correct every error. If a statement is doubtful and you cannot confirm it, remove it.
2. **Book / film / series separation.** "book" holds book facts only. Film or series inventions must not be in "book". In "film" and "series", remove any claim you are not sure of (an empty string is correct when unsure). Check actor names.
3. **Place links (most important for the map).** Each entry in "places" must point to the correct id for the place meant (read the title of that id in the index), and the books must support that the person or thing was there in that role. Remove a wrong link, or change the id to the correct one. Add an obvious missing link when a major place of the person's story is in the index but not linked (for example the place of death, the seat of rule). Use the most exact id. Check that First Age links use "b:" ids and that a Third Age place is not linked for a First Age event at a different site with the same name. Check "offmap" the same way.
4. **facts, aka, related.** Remove wrong values. "related" ids must exist in the master lists and must be truly related.
5. **Quotations.** If a sentence looks copied from the books or a wiki, rewrite it in plain words.
6. **Style.** Short sentences, active voice, no contractions. Correct only clear breaks; do not rewrite good text.
7. **Confidence.** Set "high", "medium" or "low" to match the card after your corrections.

For new-place cards also check the position: read "x", "y", "near", "basis" in master_places.json and the neighbours in map_index.tsv. If a position is wrong by more than about 30 km and you know a better one, correct "x" and "y" in the card AND in master_places.json (same values), and say so in your log. Do not move a place for a small doubt.

## How to work
- Edit the card files in place. Keep each file one valid JSON list with the same ids and the same order. Do not add or delete cards. Do not change "id", "title" or "group".
- After your edits, run the check command given in your task for each file and correct every problem until it prints OK.
- Write a change log as markdown to the path given in your task: one line for each changed card, `id | severity (serious / minor) | what was wrong -> what you did`. A wrong fact, a wrong place link, or a film/series invention in "book" is serious. Style changes are minor; group them in one line per file.

## Final reply (fixed format, nothing else)
`REVIEWED <files> | cards: <count> | changed: <count> | serious: <count> | links removed: <n>, changed: <n>, added: <n> | notes: <at most two short lines>`
