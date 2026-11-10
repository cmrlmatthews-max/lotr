"""Beleriand, First Age: original control geometry written from the descriptions in The Silmarillion.
Coordinates are km: x east, y north, origin at the south-west corner. 1 league = 4.83 km.
Anchors from the text: Dorthonion 60 leagues east-west; East Beleriand 100 leagues Sirion to Gelion;
Sirion 130 leagues from the Pass to the Delta; Angband 150 leagues from Menegroth; Gelion 40 leagues
from the meeting of its arms to the Ascar."""
import math
W, H = 1320.0, 1420.0

def ell(cx, cy, rx, ry, n=20): return [(cx + rx * math.cos(2 * math.pi * k / n), cy + ry * math.sin(2 * math.pi * k / n)) for k in range(n)]

# Land outline, clockwise from the north-west. The east, north and south-east edges run off the sheet.
COAST = [(300, 1420), (292, 1300), (272, 1180), (286, 1060), (300, 985), (286, 935), (300, 902), (340, 898), (385, 890), (402, 879),
         (382, 869), (336, 872), (296, 872), (270, 842), (254, 802), (248, 762), (266, 730), (280, 690), (270, 650), (289, 606),
         (268, 580), (256, 548), (284, 526), (329, 507), (320, 470), (335, 420), (360, 370), (390, 320), (428, 268), (470, 245),
         (520, 240), (575, 232), (626, 222), (680, 228), (740, 215), (800, 180), (850, 130), (880, 60), (890, 0),
         (1320, 0), (1320, 1420)]
ISLE_BALAR = ell(590, 150, 27, 17)

# id, name, layer, label point, points, peak height m, half-width km, hint
RIDGES = [
 ('MT01', 'Ered Engrin', 'Mountains', (560, 1392), [(300, 1396), (450, 1393), (600, 1389), (700, 1381), (770, 1369), (850, 1381), (1000, 1389), (1150, 1393), (1320, 1398)], 2700, 26, 'Iron Mountains, the wall of the far north, raised by Morgoth'),
 ('MT02', 'Thangorodrim', 'Mountains', (770, 1364), [(752, 1366), (770, 1356), (788, 1366), (770, 1380)], 3300, 11, 'three volcanic peaks piled above the gates of Angband'),
 ('MT03', 'Ered Lómin', 'Mountains', (345, 965), [(350, 1095), (334, 1045), (350, 990), (366, 940), (392, 906)], 1500, 15, 'Echoing Mountains, the west wall of Hithlum'),
 ('MT03b', None, 'Mountains', None, [(404, 864), (409, 838), (412, 814)], 1400, 14, ''),
 ('MT04', 'Ered Wethrin', 'Mountains', (520, 800), [(412, 812), (450, 800), (500, 798), (548, 804), (585, 822), (600, 860), (606, 920), (603, 985), (594, 1045), (578, 1095), (548, 1130), (500, 1150), (440, 1150), (385, 1128), (350, 1095)], 1900, 17, 'Mountains of Shadow, the south and east wall of Hithlum'),
 ('MT05', 'Mountains of Mithrim', 'Mountains', (497, 866), [(556, 816), (522, 845), (486, 875), (456, 900)], 1100, 9, 'spur that parts Dor-lómin from Mithrim'),
 ('MT06', None, 'Hills', None, [(410, 812), (370, 791), (326, 773), (286, 765)], 700, 9, ''),
 ('MT07', 'Mount Taras', 'Mountains', (262, 760), [(261, 762), (264, 763)], 1300, 8, 'great headland mountain at the south-west of Nevrast; Vinyamar lies below it'),
 ('MT08', 'Echoriath', 'Mountains', (748, 742), ell(708, 742, 34, 34, 28) + [(742, 742)], 2100, 9, 'Encircling Mountains around Tumladen and Gondolin'),
 ('MT09', 'Ered Gorgoroth', 'Mountains', (840, 770), [(752, 770), (800, 765), (850, 767), (900, 772), (942, 785)], 1500, 9, 'Mountains of Terror, the southern precipices of Dorthonion'),
 ('MT10', None, 'Hills', None, [(1015, 825), (1045, 832), (1076, 828)], 620, 12, ''),
 ('MT11', 'Ered Luin', 'Mountains', (1262, 720), [(1256, 1120), (1251, 980), (1247, 860), (1244, 720), (1241, 600), (1240, 545), (1237, 420), (1233, 300), (1230, 180), (1226, 60), (1224, 0)], 2300, 22, 'Blue Mountains, the eastern wall of Beleriand; Ered Lindon'),
 ('MT12', 'Mount Rerir', 'Mountains', (1172, 842), [(1246, 852), (1206, 846), (1172, 840)], 1700, 11, 'western shoulder of the Blue Mountains above Lake Helevorn; source of Greater Gelion'),
 ('MT13', 'Mount Dolmed', 'Mountains', (1240, 545), [(1239, 545), (1241, 546)], 2700, 10, 'peak above the pass of the Dwarf-road, between Belegost and Nogrod'),
 ('HI01', 'Taur-en-Faroth', 'Hills', (458, 585), [(452, 628), (457, 588), (467, 548), (481, 510)], 430, 12, 'High Faroth, wooded highlands west of the Narog above Nargothrond'),
 ('HI02', 'Andram', 'Hills', (800, 456), [(506, 520), (580, 497), (655, 481), (760, 463), (860, 447), (925, 433)], 190, 8, 'the Long Wall, a line of hills and falling land from Nargothrond to Ramdal'),
 ('HI03', 'Amon Rûdh', 'Hills', (562, 575), [(561, 575), (563, 576)], 520, 5, 'the Bald Hill; Bar-en-Danwedh, the house of Mîm, refuge of Túrin'),
 ('HI04', 'Amon Ereb', 'Hills', (966, 425), [(965, 425), (967, 426)], 400, 7, 'the Lonely Hill in East Beleriand; Denethor of the Green-elves fell here'),
 ('HI05', 'Ramdal', 'Hills', (925, 433), [(923, 433), (927, 433)], 260, 6, "the Wall's End, where Andram ends"),
 ('HI06', 'Amon Ethir', 'Hills', (496, 568), [(495, 568), (497, 568)], 210, 3, 'the Hill of Spies, a league east of the doors of Nargothrond'),
 ('CR01', 'Crissaegrim', 'Mountains', (716, 706), [(690, 713), (708, 708), (728, 714)], 2400, 7, 'the southern peaks of Echoriath, the eyries of Thorondor'),
]
# raised ground: polygon, metres added
PLATEAUS = [
 ('hithlum', [(360, 1080), (366, 1005), (382, 905), (412, 832), (452, 812), (560, 817), (594, 860), (598, 1000), (580, 1085), (540, 1125), (440, 1135), (390, 1115)], 340),
 ('dorthonion', [(668, 800), (682, 878), (760, 905), (860, 902), (950, 882), (976, 832), (966, 792), (900, 772), (820, 768), (745, 772), (692, 782)], 640),
 ('tumladen', ell(708, 742, 26, 26, 16), 260),
 ('north_of_andram', [(500, 525), (580, 500), (655, 484), (760, 466), (860, 450), (930, 436), (1000, 520), (1000, 760), (640, 780), (470, 780), (440, 620)], 110),
 ('ossiriand', [(1150, 0), (1160, 520), (1180, 760), (1200, 1100), (1320, 1100), (1320, 0)], 190),
 ('north_plain', [(610, 930), (1200, 930), (1320, 1000), (1320, 1420), (300, 1420), (300, 1200), (610, 1200)], 150),
 ('himring', ell(1040, 826, 44, 22, 16), 180),
]
# id, name, label point, points, hint  (drawn source to mouth)
RIVERS = [
 ('RI01', 'Sirion', (628, 400), [(617, 905), (626, 880), (640, 850), (646, 800), (649, 760), (655, 705), (651, 662), (652, 628), (642, 603), (650, 588), (648, 560), (660, 514), (655, 484)], 'the great river of Beleriand, 130 leagues from the Pass to the Delta'),
 ('RI01b', None, None, [(655, 469), (648, 420), (640, 345), (636, 290), (630, 245), (627, 224)], ''),
 ('RI02', 'Narog', (520, 460), [(478, 792), (486, 740), (490, 690), (492, 640), (492, 565), (505, 500), (540, 430), (590, 372), (639, 346)], 'chief river of West Beleriand, from Ivrin past Nargothrond to Sirion in Nan-tathren'),
 ('RI03', 'Teiglin', (540, 742), [(515, 790), (545, 730), (572, 672), (592, 646), (615, 620), (642, 603)], 'river from Ered Wethrin round the forest of Brethil to Sirion'),
 ('RI04', 'Esgalduin', (722, 610), [(812, 772), (806, 718), (800, 670), (790, 625), (740, 605), (690, 592), (651, 588)], 'the river of Doriath, past Menegroth; divides Neldoreth from Region'),
 ('RI05', 'Aros', (838, 572), [(955, 795), (905, 705), (880, 650), (860, 590), (800, 530), (720, 505), (668, 512)], 'river that bounds Doriath on the east and south'),
 ('RI06', 'Celon', (952, 730), [(1005, 812), (960, 740), (915, 670), (878, 632)], 'river from Himring to Aros, past Nan Elmoth'),
 ('RI07', 'Mindeb', (700, 700), [(716, 722), (704, 702), (686, 686), (666, 672), (651, 662)], 'river from the mountains to Sirion; Dimbar lies between it and Sirion'),
 ('RI08', 'Gelion', (1085, 380), [(1165, 835), (1130, 770), (1085, 705), (1100, 620), (1112, 512), (1105, 430), (1090, 340), (1075, 250), (1060, 140), (1050, 0)], 'the great river of East Beleriand, twice as long as Sirion'),
 ('RI08b', None, None, [(1030, 815), (1060, 760), (1085, 705)], ''),
 ('RI09', 'Ascar', (1175, 525), [(1236, 528), (1175, 518), (1114, 511)], 'northernmost of the seven rivers of Ossiriand; later Rathlóriel'),
 ('RI10', 'Thalos', (1175, 468), [(1236, 472), (1172, 462), (1109, 456)], 'second river of Ossiriand'),
 ('RI11', 'Legolin', (1170, 414), [(1234, 422), (1168, 409), (1103, 400)], 'third river of Ossiriand'),
 ('RI12', 'Brilthor', (1165, 362), [(1232, 372), (1164, 358), (1097, 348)], 'fourth river of Ossiriand'),
 ('RI13', 'Duilwen', (1160, 312), [(1230, 322), (1160, 308), (1089, 298)], 'fifth river of Ossiriand'),
 ('RI14', 'Adurant', (1205, 270), [(1228, 264), (1185, 262), (1168, 266), (1150, 262), (1079, 246)], 'sixth and southernmost river of Ossiriand, with the isle of Tol Galen'),
 ('RI14b', None, None, [(1185, 262), (1168, 250), (1150, 262)], ''),
 ('RI15', 'Ginglith', (452, 700), [(430, 722), (468, 672), (492, 640)], 'tributary that joins the Narog above Nargothrond'),
 ('RI16', 'Ringwil', (470, 572), [(462, 570), (492, 565)], 'short stream that falls into the Narog at Nargothrond'),
 ('RI17', 'Brithon', (325, 640), [(352, 662), (318, 630), (292, 603)], 'river of the Falas that reaches the sea at Brithombar'),
 ('RI18', 'Nenning', (372, 590), [(402, 645), (364, 565), (331, 508)], 'river of the Falas that reaches the sea at Eglarest'),
 ('RI20', None, None, [(615, 668), (599, 662), (585, 656)], ''),
 ('RI19', 'Rivil', (676, 846), [(706, 836), (672, 848), (642, 852)], "stream from Rivil's Well in Dorthonion to Sirion at the Fen of Serech"),
]
LAKES = [
 ('LA01', 'Lake Mithrim', ell(518, 928, 20, 11), 'lake in the east of Hithlum; first camps of the Noldor'),
 ('LA02', 'Lake Helevorn', ell(1150, 798, 14, 8), 'dark deep lake under Mount Rerir; Caranthir lived beside it'),
 ('LA03', 'Tarn Aeluin', ell(870, 835, 6, 4), 'clear mountain lake in Dorthonion; refuge of Barahir and his outlaws'),
 ('LA04', 'Eithel Ivrin', ell(478, 794, 5, 4), 'pools and falls of Ivrin, the source of the Narog'),
 ('LA05', 'Linaewen', ell(342, 813, 11, 6), 'great mere of birds in the middle of Nevrast'),
 ('LA06', 'Aelin-uial', ell(664, 512, 13, 6), 'Meres of Twilight, where Aros meets Sirion'),
]
FORESTS = [
 ('FO01', 'Neldoreth', [(662, 662), (720, 685), (790, 690), (800, 640), (780, 615), (730, 600), (680, 590), (655, 600), (652, 640)], 'the northern beech-forest of Doriath; Lúthien was born here'),
 ('FO02', 'Region', [(660, 585), (730, 598), (785, 612), (805, 640), (850, 685), (882, 648), (860, 592), (800, 532), (720, 508), (668, 516), (652, 550)], 'the greater southern forest of Doriath, around Menegroth'),
 ('FO03', 'Nivrim', [(625, 522), (650, 518), (648, 596), (630, 598), (616, 560)], 'the West March of Doriath, oak-woods on the west bank of Sirion'),
 ('FO04', 'Brethil', [(585, 700), (640, 705), (648, 640), (640, 608), (610, 618), (585, 650), (575, 680)], 'forest between Teiglin and Sirion; home of the Haladin'),
 ('FO05', 'Nan Elmoth', [(905, 650), (940, 668), (965, 640), (950, 610), (915, 608), (898, 628)], 'dark wood east of Celon; Thingol met Melian here; later the home of Eöl'),
 ('FO06', 'Taur-im-Duinath', [(720, 400), (800, 410), (900, 400), (1000, 380), (1040, 300), (1020, 180), (960, 90), (890, 60), (860, 130), (800, 185), (740, 220), (690, 260), (680, 340)], 'the Forest between the Rivers, wild land south of Andram between Sirion and Gelion'),
 ('FO07', 'Nimbrethil', [(480, 290), (540, 300), (575, 270), (560, 245), (500, 250), (470, 265)], 'birchwoods of Arvernien; timber of Vingilot'),
 ('FO08', 'Taur-nu-Fuin', [(690, 800), (700, 868), (765, 892), (860, 890), (940, 870), (960, 820), (900, 785), (820, 780), (745, 784)], 'the pine forest of Dorthonion, later the Forest under Nightshade'),
 ('FO09', 'Nan-tathren', [(615, 370), (660, 372), (665, 320), (645, 300), (618, 318)], 'Land of Willows, where Narog meets Sirion'),
 ('FO10', None, [(1112, 505), (1225, 518), (1222, 262), (1086, 250), (1100, 380)], ''),
 ('FO11', None, [(445, 622), (478, 616), (490, 522), (466, 502), (448, 552)], ''),
]
SWAMPS = [
 ('SW01', 'Fen of Serech', [(628, 864), (660, 864), (662, 838), (632, 836)], 'marsh north of the Pass of Sirion, where Rivil meets Sirion'),
 ('SW02', None, [(640, 526), (690, 529), (692, 500), (642, 498)], ''),
 ('SW03', None, [(320, 826), (366, 829), (368, 800), (322, 798)], ''),
 ('SW04', 'Lisgardh', [(606, 252), (656, 254), (656, 228), (604, 226)], 'land of reeds at the Mouths of Sirion'),
]
ROADS = [
 ('RD01', 'Dwarf-road', (1010, 606), [(1264, 500), (1252, 530), (1240, 546), (1175, 530), (1112, 512), (1000, 600), (905, 705), (806, 718), (740, 706), (655, 705), (610, 690), (572, 672)], 'major', 'road of the Dwarves from Nogrod and Belegost over Sarn Athrad into Beleriand'),
 ('RD01b', None, None, [(1264, 605), (1252, 565), (1240, 546)], 'major', ''),
 ('RD02', 'Old South Road', (585, 742), [(645, 798), (625, 760), (600, 720), (572, 672), (535, 630), (495, 568)], 'major', 'road from Tol Sirion along the eaves of Brethil to the Crossings of Teiglin and Nargothrond'),
]
GIRDLE = [(652, 664), (720, 690), (790, 696), (852, 690), (886, 650), (863, 590), (802, 528), (720, 502), (668, 508), (624, 518), (613, 560), (627, 602), (650, 632)]
# id, name, layer, x, y, hint
POINTS = [
 ('TO01', 'Menegroth', 'Towns', 793, 617, 'the Thousand Caves, halls of Thingol and Melian on the Esgalduin'),
 ('TO02', 'Nargothrond', 'Towns', 489, 565, 'hidden cave-fortress of Finrod Felagund in the west bank of the Narog'),
 ('TO03', 'Gondolin', 'Towns', 708, 742, 'hidden city of Turgon on Amon Gwareth in the vale of Tumladen'),
 ('TO04', 'Vinyamar', 'Towns', 273, 777, "Turgon's first halls in Nevrast, under Mount Taras"),
 ('TO05', 'Brithombar', 'Towns', 293, 603, 'northern haven of the Falas, of Círdan and the Falathrim'),
 ('TO06', 'Eglarest', 'Towns', 333, 509, 'southern haven of the Falas'),
 ('TO07', 'Havens of Sirion', 'Towns', 629, 240, 'refuge at the Mouths of Sirion after the falls of Doriath and Gondolin; Elwing and Eärendil'),
 ('TO08', 'Ephel Brandir', 'Towns', 607, 651, 'stockaded home of the Haladin on Amon Obel in Brethil'),
 ('TO09', 'Belegost', 'Towns', 1265, 606, 'Gabilgathol, Dwarf-city in the Blue Mountains north of Mount Dolmed'),
 ('TO10', 'Nogrod', 'Towns', 1265, 500, 'Tumunzahar, Dwarf-city in the Blue Mountains south of Mount Dolmed'),
 ('FT01', 'Angband', 'Fortresses', 770, 1345, "Morgoth's fortress, the Hells of Iron, under Thangorodrim"),
 ('FT02', 'Barad Eithel', 'Fortresses', 619, 905, 'fortress of Fingolfin and Fingon at Eithel Sirion, the source of Sirion'),
 ('FT03', 'Tol Sirion', 'Fortresses', 646, 798, "island in the Pass of Sirion with Finrod's tower Minas Tirith; later Tol-in-Gaurhoth, Sauron's Isle of Werewolves"),
 ('FT04', 'Himring', 'Fortresses', 1015, 826, 'citadel of Maedhros on the cold Hill of Himring'),
 ('FT05', 'Barad Nimras', 'Fortresses', 259, 549, 'watch-tower that Finrod raised on the cape west of Eglarest'),
 ('GR01', 'Haudh-en-Ndengin', 'Graves_Tombs', 760, 1060, 'the Hill of Slain (Haudh-en-Nirnaeth) in the middle of Anfauglith'),
 ('GR02', 'Haudh-en-Elleth', 'Graves_Tombs', 579, 671, 'mound of Finduilas near the Crossings of Teiglin'),
 ('VA01', 'Cabed-en-Aras', 'Valleys', 592, 646, 'gorge of the Teiglin where Túrin slew Glaurung; later Cabed Naeramarth'),
 ('FA01', 'Nen Girith', 'Falls', 599, 662, 'Dimrost, the falls of the Celebros stream in Brethil'),
 ('FA02', 'Falls of Sirion', 'Falls', 655, 484, 'where Sirion falls over Andram and goes under the ground'),
 ('CA01', 'Gates of Sirion', 'Cave_entrances', 655, 469, 'rock arches where Sirion comes out again, three leagues south of the falls'),
 ('FA03', "Rivil's Well", 'Falls', 707, 836, 'source of the Rivil in Dorthonion; Beren avenged his father here'),
 ('HA01', 'Losgar', 'Harbors', 306, 884, 'landing of Fëanor at the mouth of Drengist; the burning of the ships'),
 ('VA02', 'Cirith Ninniach', 'Valleys', 405, 877, 'the Rainbow Cleft at the head of the Firth of Drengist'),
 ('FJ01', 'Brithiach', 'Fords', 655, 705, 'ford over Sirion north of Brethil'),
 ('FJ02', 'Crossings of Teiglin', 'Fords', 572, 672, 'ford where the old South Road crosses the Teiglin'),
 ('FJ03', 'Sarn Athrad', 'Fords', 1112, 512, 'the Ford of Stones on Gelion, where the Dwarf-road crosses'),
 ('FJ04', 'Arossiach', 'Fords', 905, 705, 'the Fords of Aros, near the north-east edge of Doriath'),
 ('BR01', 'Iant Iaur', 'Bridges', 806, 718, 'the Old Bridge over Esgalduin on the road through Nan Dungortheb'),
 ('VA03', 'Pass of Aglon', 'Valleys', 989, 807, 'narrow pass between Dorthonion and Himring; a gate into Doriath-ward lands'),
 ('VA04', 'Pass of Sirion', 'Valleys', 647, 818, 'the narrow vale of upper Sirion between Ered Wethrin and Dorthonion'),
 ('VA05', 'Anach', 'Valleys', 746, 774, 'pass that comes down from Taur-nu-Fuin toward Dimbar'),
 ('VA06', "Maglor's Gap", 'Valleys', 1105, 830, 'open land between Himring and the Blue Mountains'),
 ('DO01', 'Orfalch Echor', 'Doors_Gates', 681, 722, 'the ravine of the seven gates, the hidden way into Gondolin from the Dry River'),
 ('VA07', 'Cirith Thoronath', 'Valleys', 712, 777, "the Eagles' Cleft high in the north of Echoriath; the escape from Gondolin"),
 ('FI01', 'Tumhalad', 'Fields', 480, 668, 'field between Ginglith and Narog; the last battle of Nargothrond'),
 ('IS02', 'Tol Galen', 'Islands', 1167, 258, 'the Green Isle in the Adurant; Beren and Lúthien lived here'),
 ('BA01', 'Firth of Drengist', 'Bays', 345, 885, 'long sea-inlet through the Echoing Mountains'),
 ('BA02', 'Bay of Balar', 'Bays', 700, 130, 'great bay into which Sirion flows'),
 ('IS03', 'Cape Balar', 'Islands', 432, 266, 'the south-west cape of Beleriand'),
 ('IS01', 'Isle of Balar', 'Islands', 590, 150, 'island in the bay; last refuge of Círdan and Gil-galad'),
]
# id, name, type, tier, x, y, radius km
REGIONS = [
 ('RG01', 'Hithlum', 'realm', 1, 500, 975, 110), ('RG02', 'Dor-lómin', 'region', 2, 462, 842, 40), ('RG03', 'Mithrim', 'region', 2, 548, 900, 40),
 ('RG04', 'Nevrast', 'realm', 2, 332, 845, 55), ('RG05', 'The Falas', 'realm', 1, 322, 560, 80), ('RG06', 'Realm of Nargothrond', 'realm', 1, 545, 528, 110),
 ('RG07', 'Doriath', 'realm', 1, 762, 572, 110), ('RG08', 'Land of the Haladin', 'region', 3, 613, 682, 35), ('RG09', 'Dimbar', 'region', 3, 680, 697, 22),
 ('RG10', 'Nan Dungortheb', 'region', 2, 812, 738, 55), ('RG11', 'Dorthonion', 'realm', 1, 815, 848, 140), ('RG12', 'Himlad', 'region', 2, 948, 748, 25),
 ('RG13', 'March of Maedhros', 'realm', 2, 1045, 872, 80), ('RG14', 'Lothlann', 'region', 2, 1110, 965, 90), ('RG15', 'Thargelion', 'realm', 1, 1170, 690, 70),
 ('RG16', 'Ossiriand', 'realm', 1, 1170, 392, 110), ('RG17', 'Estolad', 'region', 2, 982, 572, 55), ('RG18', 'East Beleriand', 'region', 1, 885, 492, 150),
 ('RG19', 'West Beleriand', 'region', 1, 405, 455, 150), ('RG20', 'Anfauglith', 'region', 1, 800, 1105, 220), ('RG21', 'Dor Daedeloth', 'region', 2, 772, 1285, 60),
 ('RG22', 'Arvernien', 'region', 2, 545, 266, 50), ('RG23', 'Lammoth', 'region', 2, 318, 1012, 60), ('RG24', 'Talath Dirnen', 'region', 2, 542, 642, 45),
 ('RG25', 'Ladros', 'region', 3, 920, 866, 30), ('RG27', 'Dor Dínen', 'region', 3, 866, 738, 25), ('RG26', 'Hidden Realm of Gondolin', 'realm', 2, 708, 760, 40),
]
REGION_HINTS = {'RG06': 'label sits east of the Narog; the realm reaches from the Falas border to Sirion', 'RG08': 'Brethil', 'RG20': 'Ard-galen before the Dagor Bragollach', 'RG11': 'later Taur-nu-Fuin', 'RG15': 'Dor Caranthir', 'RG13': 'the hills about Himring held by Maedhros', 'RG26': 'Tumladen inside the Encircling Mountains'}
