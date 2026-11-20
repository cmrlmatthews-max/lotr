"""Aman in the Years of the Trees: original control geometry modelled from the text.
Tolkien drew no detailed map of Aman. This sheet is a model built from what The Silmarillion says
(Valaquenta; chapters 1, 3, 5-9, 11, 24; the Akallabeth), with The History of Middle-earth
(Ambarkanta, Annals of Aman, Morgoth's Ring) for points the published book leaves open.
Fixed by the text: the Pelori are a curved wall near the east coast from north to south, with one pass,
the Calacirya; Tuna stands in the pass; the Bay of Eldamar lies east of the pass with Tol Eressea in it;
Alqualonde is on the coast north of the pass; Valmar is in the midst of the plain west of the mountains;
Araman (north) and Avathar (south) are narrow lands between the wall and the sea.
Scale is a judgment: the texts give no distances in Aman.
Coordinates are km: x east, y north, origin at the south-west corner."""
import math
W, H = 2300.0, 2600.0
R = 1.0
HSTEP = 2.5
OPEN = ['S', 'N']
COAST_NOISE = 0.7

def ell(cx, cy, rx, ry, n=20): return [(cx + rx * math.cos(2 * math.pi * k / n), cy + ry * math.sin(2 * math.pi * k / n)) for k in range(n)]

# Land outline, clockwise from the north-west. Land runs off the north and south edges.
COAST = [(330, 2600), (1985, 2600), (1945, 2480), (1905, 2380), (1865, 2250), (1835, 2100), (1810, 1950), (1795, 1800),
         (1805, 1700), (1850, 1640), (1800, 1590), (1735, 1540), (1692, 1470), (1675, 1390), (1668, 1310), (1672, 1235),
         (1690, 1160), (1730, 1095), (1800, 1040), (1832, 1012), (1812, 978), (1772, 935), (1748, 870), (1735, 760), (1725, 600),
         (1720, 450), (1715, 300), (1710, 150), (1705, 0),
         (240, 0), (258, 200), (238, 400), (262, 600), (252, 800), (276, 1000), (266, 1200), (292, 1400), (272, 1600),
         (246, 1800), (284, 2000), (302, 2200), (320, 2400)]
TOL_ERESSEA = [(1872, 1430), (1898, 1400), (1910, 1340), (1906, 1270), (1896, 1210), (1874, 1180), (1850, 1200),
               (1838, 1260), (1836, 1330), (1846, 1395)]
ENCHANTED = [ell(2120, 900, 13, 8, 12), ell(2140, 1020, 12, 9, 12), ell(2128, 1140, 14, 8, 12), ell(2150, 1260, 12, 9, 12),
             ell(2132, 1380, 14, 8, 12), ell(2146, 1500, 12, 8, 12), ell(2126, 1620, 13, 9, 12), ell(2140, 1740, 12, 8, 12)]
ISLANDS = [TOL_ERESSEA] + ENCHANTED

# id, name, layer, label point, points, peak height m, half-width km, hint
RIDGES = [
 ('MT01', 'Pelóri', 'Mountains', (1500, 820), [(1600, 0), (1598, 250), (1590, 500), (1580, 750), (1570, 950), (1562, 1120), (1556, 1200), (1553, 1250)], 2350, 32,
  'the Mountains of Aman, highest of the world: a curved wall near the east coast from north to south, pierced only by the Calacirya'),
 ('MT01b', None, 'Mountains', None, [(1553, 1370), (1557, 1420), (1572, 1560), (1600, 1750), (1630, 1950), (1648, 2150), (1638, 2350), (1600, 2500), (1562, 2600)], 2350, 32, ''),
 ('MT02', 'Taniquetil', 'Mountains', (1587, 1191), [(1586, 1190), (1588, 1192)], 4300, 22,
  'Oiolossë, Mount Everwhite: highest mountain of the world, on the borders of the sea; Ilmarin on its summit. South of the pass after the HoME maps'),
 ('MT03', 'Hyarmentir', 'Mountains', (1604, 331), [(1603, 330), (1605, 332)], 3250, 15,
  'highest mountain of the southern Pelóri, above Avathar; Melkor and Ungoliant climbed it to look on Valinor'),
 ('HI01', 'Túna', 'Hills', (1554, 1310), [(1553, 1309), (1555, 1311)], 420, 7,
  'the green hill raised in the Calacirya; Tirion stands on its crown'),
 ('HI02', 'Ezellohar', 'Hills', (850, 1302), [(849, 1301), (851, 1303)], 110, 3,
  'Corollairë, the green mound before the western gate of Valmar where the Two Trees grew'),
 ('HI03', None, 'Hills', None, [(1140, 2205), (1200, 2255), (1275, 2275), (1345, 2250), (1400, 2275)], 760, 13, ''),
 ('HI05', None, 'Hills', None, [(1215, 2170), (1290, 2185), (1370, 2205), (1440, 2255), (1500, 2330)], 680, 12, ''),
]
# raised ground: polygon, metres added
PLATEAUS = [
 ('northhills', [(1050, 2100), (1250, 2160), (1500, 2260), (1560, 2420), (1400, 2420), (1150, 2320), (1020, 2220)], 220),
 ('araman', [(1650, 1600), (1780, 1640), (1820, 2000), (1880, 2350), (1940, 2600), (1600, 2600), (1660, 2200), (1640, 1800)], 120),
]
PLATEAU_SIGMA = {'northhills': 14, 'araman': 16}
LEVEL = [[(640, 1060), (1160, 1060), (1180, 1560), (640, 1560)]]
# id, name, label point, points, hint  (source to mouth). The streams are unnamed: the texts name no river in Aman.
RIVERS = [
]
LAKES = [
 ('LA01', 'Lórellin', ell(800, 820, 24, 14), "approx: the lake in the gardens of Lórien; Estë sleeps by day on the tree-grown isle in it"),
 ('LA02', 'Wells of Varda', ell(832, 1250, 6, 4), "approx: Varda's great vats of the dew of Telperion and the light of Laurelin, near the Trees; Ungoliant drank them"),
]
FORESTS = [
 ('FO01', 'Woods of Oromë', [(1240, 300), (1360, 260), (1480, 300), (1520, 450), (1505, 620), (1420, 690), (1290, 660), (1220, 520)],
  'the forests of the Huntsman in the south of Valinor, at the feet of Hyarmentir'),
 ('FO02', 'Gardens of Lórien', [(690, 760), (760, 720), (860, 735), (905, 800), (880, 880), (800, 915), (710, 895), (670, 830)],
  'approx: the gardens of Irmo, fairest place in the world, with the lake Lórellin; placed south of Valmar'),
]
SWAMPS = []
ROADS = []
# id, name, layer, x, y, hint
POINTS = [
 ('TO01', 'Valmar', 'Towns', 935, 1314, 'Valimar of many bells, city of the Valar in the midst of the plain of Valinor'),
 ('TO02', 'Tirion', 'Towns', 1553, 1306, 'white city of the Vanyar and Noldor on the crown of Túna in the Calacirya'),
 ('BU02', 'Mindon Eldaliéva', 'Buildings', 1546, 1282, 'the tower of Ingwë in Tirion, whose lamp shone far out to sea'),
 ('HA01', 'Alqualondë', 'Harbors', 1675, 1452, 'the Haven of the Swans, city of the Teleri on the coast of Eldamar north of the Calacirya'),
 ('HA02', 'Avallónë', 'Harbors', 1900, 1300, 'haven of the Eldar on the east side of Tol Eressëa, facing the sea; of the Second Age (Akallabêth)'),
 ('FT01', 'Formenos', 'Fortresses', 1255, 2235, "Fëanor's stronghold and treasury in the hills in the north of Valinor; Finwë was slain at its doors"),
 ('BU01', 'Ilmarin', 'Buildings', 1588, 1194, 'the halls of Manwë and Varda on the summit of Taniquetil'),
 ('BU03', 'Halls of Mandos', 'Buildings', 305, 1480, 'approx: the Halls of Awaiting in the west of Valinor by the shore of the Outer Sea'),
 ('BU04', 'Halls of Nienna', 'Buildings', 272, 1805, 'approx: halls west of West upon the borders of the world, near the Halls of Mandos'),
 ('BU05', 'Mansions of Aulë', 'Buildings', 1020, 1560, 'approx: the halls of the Smith of the Valar in Valinor; the text gives no place'),
 ('DO02', 'Door of Night', 'Doors_Gates', 30, 1320, 'approx: the door in the Walls of the Night beyond Ekkaia; the Ambarkanta (HoME IV) puts it in the far west, beyond the edge of this sheet; Morgoth was thrust through it into the Void after the War of Wrath (Silmarillion ch. 24)'),
 ('DO01', 'Gates of Valmar', 'Doors_Gates', 905, 1278, 'the golden gates of Valmar on its west side, facing Ezellohar and the Ring of Doom'),
 ('BU06', 'Máhanaxar', 'Buildings', 900, 1350, 'the Ring of Doom, where the Valar sat in council, near the golden gates of Valmar'),
 ('VA01', 'Calacirya', 'Valleys', 1582, 1320, 'the Pass of Light, the one cleft through the Pelóri, made for the Eldar; the light of the Trees flowed out through it'),
 ('IS01', 'Tol Eressëa', 'Islands', 1872, 1340, 'the Lonely Isle, ferry of the Eldar, rooted by Ulmo in the Bay of Eldamar'),
 ('IS02', 'Enchanted Isles', 'Islands', 2140, 1320, 'chain of isles set from north to south in the Shadowy Seas at the Hiding of Valinor (after the Flight of the Noldor)'),
 ('BA01', 'Bay of Eldamar', 'Bays', 1760, 1200, 'the great bay of Elvenhome east of the Calacirya, with Tol Eressëa in it'),
 ('BA02', 'Ekkaia', 'Bays', 120, 650, 'the Outer Sea that surrounds the world, west of Valinor'),
 ('BA03', 'Belegaer', 'Bays', 2000, 950, 'the Great Sea between Aman and Middle-earth; the Sundering Seas'),
 ('CA01', 'Caves of the Forgotten', 'Cave_entrances', 1592, 1270, 'approx: where Ar-Pharazôn and his warriors lie under the hills that fell on them about Túna (Second Age, Akallabêth)'),
]
# id, name, type, tier, x, y, radius km
REGIONS = [
 ('RG01', 'Aman', 'realm', 1, 640, 2380, 1100), ('RG02', 'Valinor', 'realm', 1, 950, 1700, 620), ('RG03', 'Eldamar', 'region', 1, 1625, 1395, 110),
 ('RG04', 'Araman', 'region', 1, 1735, 1980, 200), ('RG05', 'Avathar', 'region', 1, 1660, 620, 260), ('RG06', 'Oiomúrë', 'region', 2, 1830, 2400, 80),
 ('RG07', 'Helcaraxë', 'region', 2, 2140, 2470, 170), ('RG08', 'Shadowy Seas', 'region', 2, 2075, 1320, 260), ('RG09', 'Pastures of Yavanna', 'region', 2, 1020, 470, 170),
]
REGION_HINTS = {
 'RG01': 'the Blessed Realm, the Undying Lands in the West',
 'RG02': 'land of the Valar west of the Pelóri, from the mountains to the Outer Sea',
 'RG03': 'Elvenhome: the coast and bay east of the Calacirya, with Tirion and Alqualondë',
 'RG04': 'cold waste between the Pelóri and the sea in the north; the Doom of Mandos was spoken here',
 'RG05': 'narrow dark land between the Pelóri and the sea in the south; Ungoliant dwelt in a ravine here',
 'RG06': 'region of mists on the coast of Araman near the Helcaraxë',
 'RG07': 'the Grinding Ice between Araman and Middle-earth; Fingolfin crossed it',
 'RG08': 'dark seas east of Tol Eressëa, shadowed after the Hiding of Valinor (after the Flight of the Noldor)',
 'RG09': "the fields of Yavanna in the south of Valinor, west of the woods of Oromë",
}
