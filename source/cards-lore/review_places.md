# Review of new-place cards (newplaces_me_a, newplaces_me_b, newplaces_bel)

Positions checked against map_index.tsv, data/vectors.json (rivers, roads, polygons) and bel/geo.py. Moved places have the same x, y in the card and in master_places.json; every moved place is on land and at least 3 km from every other place.

## newplaces_me_a.json
- NP001 | serious | film text was wrong (no Black Rider in Maggot's fields; Maggot chases Merry and Pippin) -> rewrote film line.
- NP002 | serious | Merry did not wait at the ferry, and the Rider appears after the boat leaves -> Merry meets them near the ferry; the Rider is seen on the far landing; noted the Bridge twenty miles north.
- NP003 | serious | "the Mayor is the only ruler" was wrong (Thain), and "west of Bywater" was doubtful -> rewrote; location now "on the East Road near Bywater"; sources set to the Shire map and Prologue. Position not moved (under 30 km doubt).
- NP004 | serious | invented "lower end of the village" detail -> gate is where the Road leaves Bree; added the departure past Bill Ferny's house; Realm set to Bree-land.
- NP005 | minor | confidence low -> medium (facts are plain in The Hobbit and LotR).
- NP006 | serious | film line wrong (Bilbo stalls the trolls, Gandalf splits the rock); trolls stand in a clearing near, not beside, the Road -> fixed both.
- NP007 | serious | invented claim about trolls threatening "the North Road" -> removed; text now follows Strider's description; English name "Troll-fells".
- NP009 | serious | Gandalf did not blame Saruman in the book -> Boromir blames the Enemy, Gimli blames Caradhras.
- NP010 | serious | position was east of the Anduin (wrong bank); "Naith Lórien" is not a book name; links to the Nimrodel and its bridge were outside the Naith -> moved from (1245, 1201) to (1204, 1215), inside the angle north of the Silverlode; names English "The Gore" only; related now TO018, HI014, RI014, RI003 plus persons.
- NP012 | serious | order of events wrong (orc attack and Legolas's shot came the night before the portage) -> rewrote; moved from (1377, 948) onto the Anduin at (1387, 949); facts Realm "Wilderland" replaced with Kind "Rapids".
- NP013 | serious | the hunters did not meet the Rohirrim at the cliff -> they ran for days across the plains first.
- NP014 | serious | position lay inside The Wold polygon -> moved from (1220, 946) to (1245, 900), south of the Wold between Entwash and Emyn Muil; added the Three Hunters and person:aragorn.
- NP015 | minor | doubtful "Edoras near its southern edge" -> plain wording; added the ride to the Fords of Isen.
- NP016 | serious | Aldburg lies in the Folde, not the Eastfold; the Eastfold muster claim was unsupported -> removed both; added Éomund of Eastfold (Appendix A) and the road east to Gondor; moved from (1114, 826) next to the Snowbourn to (1168, 810), east of the Folde toward Anórien; related TO002, FT009 -> RI087, RD044, person:eomund.
- NP018 | serious | invented "cliffs run south from its feet" -> Helm's Deep is a gorge under the mountain, guarded by the Hornburg.
- NP020 | minor | Legolas, Gimli and the Grey Company went with Aragorn, not after him -> fixed.
- NP023 | serious | the hobbits did not take part in the Ents' decision -> rewrote; added the meeting with Gandalf on the same hill; related added FI005, person:gandalf.
- NP024 | serious | point sat at the head of the delta, not at the mouths -> moved from (1316, 828) to (1348, 834) on the delta channels toward the Anduin; Entwash flows out of Fangorn.
- NP026 | serious | grass claim wrong -> grass grew long on the Howe, the ground where the Nazgûl's beast was burned stayed bare; added the dart.

## newplaces_me_b.json
- NP028 | minor | clarified that Frodo coaxed Gollum and the law is Gondor's.
- NP031 | serious | the region was not named after Amroth (the city was) -> removed; Imrahil described as brother of Finduilas; blurb reworded.
- NP032 | minor | removed doubtful claim that the Cross-roads lie in North Ithilien; ambushes were on the Southrons.
- NP034 | serious | doubtful Sam passage and invented name meaning -> removed; added Elessar's gift of the Núrnen lands to the freed slaves; related person:frodo-baggins -> person:aragorn.
- NP035 | serious | invented route of Gollum across the Noman-lands -> rewrote from the map; related persons removed, added HI022, FI004, realm:brown-lands.
- NP038 | serious | invented claim about the forest bending back from Erebor; point lay 16 km inside the Mirkwood polygon -> removed claim; moved from (1553, 1399) to (1578, 1375), in the bight on the forest's east edge; related MT029, TO024 removed, realm:rhovanion added.
- NP042 | minor | blurb listed Michel Delving and "the capital" as two places -> fixed.
- NP043 | serious | link to Pippin had no basis -> added Battle of Greenfields and Bandobras; related now TO075, TO058, battle:greenfields, person:bandobras-took.
- NP044 | serious | "Maggot's farm near Bamfurlong" wrong (Bamfurlong is the farm) -> fixed; related added NP001.
- NP046 | serious | point lay inside the Old Forest beyond the High Hay; "lock their doors" unsupported -> moved from (614, 1400) to (604, 1407) between the river and the Hay; text now says the gate in the Hay is shut at night; horn-call of Buckland in the Scouring.
- NP047 | serious | Thain described as "head of the council in time of need" -> master of the Shire-moot and captain of the Shire-muster.
- NP052 | serious | overstated "Drúedain lived there" and wrong source (Appendix F) -> softened to the Unfinished Tales statement; sources fixed; related added RI043 (Lefnui).

## newplaces_bel.json
- b:NP001 | serious | Ered Wethrin does not wall Dor-lómin on the west (that is Ered Lómin) -> south only.
- b:NP002 | serious | invented "played near it" -> Urwen called Lalaith, died young.
- b:NP003 | serious | gate "guarded by Noldor" not supported -> made by the Noldor and kept secret.
- b:NP004 | serious | order wrong (captured and enslaved, escaped, then outlaw) -> fixed.
- b:NP005 | minor | Voronwë led Tuor along the Dry River; old outflow of Tumladen; related person:turgon -> person:voronwe.
- b:NP007 | serious | the Eagles did not raise the cairn; Thorondor bore up the body and the refugees built the mound -> fixed blurb and text.
- b:NP008 | serious | Túrin and Nienor were not buried together; her body was never found, her name was carved on the stone -> fixed.
- b:NP009 | minor | vague crossing claim replaced with Níniel's shudder at Nen Girith and the watch for Glaurung.
- b:NP010 | minor | removed "small and hidden realm" wording.
- b:NP014 | serious | wrong claim about Green-elves living from its source to the sea -> replaced with Rerir, Helevorn and Caranthir; related b:RG16 removed, b:LA02 and person:caranthir added.
- b:NP015 | serious | the Silmaril did not pass to Dior "after Thingol died" -> Beren took the Nauglamír at Sarn Athrad, Lúthien wore it, then Dior; related person:thingol removed, b:FJ03 and person:dior added.
- b:NP016 | minor | Túrin joined the outlaws and became leader; Beleg came back later; related added person:mim; confidence low -> medium.

No position changes in Beleriand; all 16 points match geo.py (rivers, ridges, girdle).
