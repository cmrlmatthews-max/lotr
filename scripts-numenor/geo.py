"""Númenor (Elenna) in the Second Age, before the Downfall: original control geometry written from
"A Description of the Island of Númenor" (Unfinished Tales), with "Aldarion and Erendis", "The Line of Elros",
the Akallabêth and Appendix A.
Coordinates are km: x east, y north, origin at the south-west corner. 1 mile = 1.609 km.
Anchors from the text: the land is a five-pointed star; the Mittalmar is some 250 miles (about 400 km) across
north-south and east-west; five promontories, each about 100 miles (160 km) wide and more than 200 miles
(over 320 km) long: Forostar north, Andustar west, Hyarnustar south-west, Hyarrostar south-east, Orrostar east.
The Meneltarma stands near the middle of the Mittalmar; Rómenna lies at the head of a long firth in the east.
The promontory axes are set 72 degrees apart (a regular star); their exact bearings are a judgment."""
import math
W, H = 1300.0, 1250.0
R = 0.5
HSTEP = 1.5
OPEN = []                      # an island: sea on every side
COAST_NOISE = 0.55
MIN_ISLE_KM2 = 15              # keep the small isle of Tol Uinen
LEVEL = [[(606, 470), (668, 470), (676, 418), (598, 418)]]   # the reedy flats of the Siril delta

CX, CY = 650.0, 625.0          # middle of the Mittalmar
def ell(cx, cy, rx, ry, n=20): return [(cx + rx * math.cos(2 * math.pi * k / n), cy + ry * math.sin(2 * math.pi * k / n)) for k in range(n)]
def L(a, u, v):
    """point at distance u along bearing a (degrees, counter-clockwise from east) from the middle, offset v to the left"""
    c, s = math.cos(math.radians(a)), math.sin(math.radians(a))
    return (round(CX + u * c - v * s, 1), round(CY + u * s + v * c, 1))

# Promontory bearings (degrees from east, counter-clockwise)
A_OR, A_FO, A_AN, A_HN, A_HR = 20, 90, 160, 232, 300

def prom(a, tip, hw0, hw1, dents=(), side_bulge=(0, 0), capbay=None, capbays=None):
    """outline of one promontory in local (u, v): the right-hand coast outwards, the tip, the left-hand coast back.
    hw0 half-width at the base (u=175), hw1 half-width near the tip. dents: (u, side, depth, half-length) notches (bays)."""
    n = int((tip - 60 - 175) / 12); us = [175 + (tip - 60 - 175) * k / n for k in range(n + 1)]
    def hw(u, side):
        w = hw0 + (hw1 - hw0) * (u - 175) / (tip - 60 - 175)
        w += side_bulge[0 if side < 0 else 1] * math.sin(math.pi * (u - 175) / (tip - 175))
        for du, ds, dep, dl in dents:
            if ds == side and abs(u - du) < dl: w -= dep * (1 - abs(u - du) / dl)
        return w
    right = [(u, -hw(u, -1)) for u in us]
    cap = [(tip - 28, -hw1 * 0.78), (tip - 6, -hw1 * 0.42), (tip, 0), (tip - 6, hw1 * 0.42), (tip - 28, hw1 * 0.78)]
    if capbay:   # a bay cut into the end of the promontory: (v of its axis, depth, half-width)
        bv, dep, bw = capbay
        cap = [(tip - 28, -hw1 * 0.78), (tip - 4, bv - bw - 4), (tip - 4, bv - bw), (tip - dep * 0.6, bv - bw * 0.7), (tip - dep, bv - 4), (tip - dep, bv + 4),
               (tip - dep * 0.6, bv + bw * 0.7), (tip, bv + bw), (tip - 2, hw1 * 0.3), (tip - 8, hw1 * 0.52), (tip - 28, hw1 * 0.78)]
    if capbays:  # several small bays cut into the end of the promontory: each (v of its axis, depth, half-width)
        cap = []; e = hw1 * 0.78; k = -e
        while k <= e + 0.01:
            u = tip - 28 * (abs(k) / e) ** 2
            for bv, dep, bw in capbays:
                if abs(k - bv) < bw: u -= dep * (1 - (abs(k - bv) / bw) ** 2) ** 0.7
            cap.append((u, k)); k += 2.0
    left = [(u, hw(u, 1)) for u in reversed(us)]
    return [L(a, u, v) for u, v in right + cap + left]

# Andustar: three small bays face west in its high western end; the northernmost is the Bay of Andúnië (position review, Nov 2026)
AN = prom(A_AN, 512, 86, 70, side_bulge=(0, 6), capbays=[(-16, 42, 15), (14, 30, 11), (40, 28, 10)])
# Forostar: the narrowest and stoniest
FO = prom(A_FO, 498, 80, 62, side_bulge=(4, 4))
OR = prom(A_OR, 505, 84, 66, side_bulge=(5, 0))
HN = prom(A_HN, 515, 84, 70, side_bulge=(4, 8))
HR = prom(A_HR, 522, 84, 68, side_bulge=(0, 6))

def bay(a, r): return [L(a, r, 0)]
# The Firth of Rómenna: a long narrow inlet from the eastern bay (between Orrostar and Hyarrostar) into Arandor
FIRTH = [L(-20, 232, -34), L(-20, 214, -16), L(-20, 196, -13), L(-20, 178, -13), L(-20, 160, -13), L(-20, 144, -13), L(-20, 130, -11), L(-20, 120, -6), L(-20, 116, 0),
         L(-20, 120, 6), L(-20, 130, 11), L(-20, 144, 13), L(-20, 160, 13), L(-20, 178, 13), L(-20, 196, 13), L(-20, 214, 16), L(-20, 232, 34)]

# Land outline, counter-clockwise, starting at the base of the Orrostar on the Firth side.
COAST = (OR + bay(55, 212) + FO + bay(125, 210) + AN + [L(196, 205, 0)] + HN + [L(266, 214, 0)] + HR + FIRTH)
ISLANDS = [ell(*L(-20, 238, 4), 6, 4, 14)]          # Tol Uinen in the Bay of Rómenna

MEN = (CX - 12, CY + 8)                              # the Meneltarma, near the middle of the Mittalmar
def root(a, r0, r1, n=4): return [(round(MEN[0] + (r0 + (r1 - r0) * k / (n - 1)) * math.cos(math.radians(a)), 1), round(MEN[1] + (r0 + (r1 - r0) * k / (n - 1)) * math.sin(math.radians(a)), 1)) for k in range(n)]

# id, name, layer, label point, points, peak height m, half-width km, hint
RIDGES = [
 ('MT01', 'Meneltarma', 'Mountains', (MEN[0] + 8, MEN[1] + 10), [(MEN[0] - 1, MEN[1]), (MEN[0] + 1, MEN[1] + 1)], 2500, 16, 'the Pillar of Heaven, tall mountain near the middle of the Mittalmar; the Hallow of Eru on its flat summit'),
 ('HI01', 'Tarmasundar', 'Hills', (MEN[0] - 40, MEN[1] - 34), root(A_HN, 14, 58), 480, 9, 'the Roots of the Pillar: five long low ridges running out from the Meneltarma toward the five promontories'),
 ('HI02', None, 'Hills', None, root(A_HR, 14, 58), 480, 9, ''),
 ('HI03', None, 'Hills', None, root(A_OR, 14, 55), 460, 9, ''),
 ('HI04', None, 'Hills', None, root(A_FO, 14, 55), 460, 9, ''),
 ('HI05', None, 'Hills', None, root(A_AN, 14, 55), 460, 9, ''),
 ('MT02', 'Sorontil', 'Mountains', L(A_FO, 470, -4), [L(A_FO, 470, -6), L(A_FO, 472, -4)], 1500, 11, 'great height in the north of the Forostar rising sheer from the sea in tall cliffs; eagles nested here'),
 ('MT03', 'Highlands of the Forostar', 'Hills', L(A_FO, 380, 12), [L(A_FO, 300, 10), L(A_FO, 360, 6), L(A_FO, 420, 0), L(A_FO, 455, -4)], 650, 16, 'descriptive name: the rocky, stony uplands of the Forostar, the least fertile part of the isle'),
 ('HI06', 'Oromet', 'Hills', L(A_AN, 462, 30), [L(A_AN, 460, 28), L(A_AN, 462, 30)], 560, 6, 'hill near the haven of Andúnië in the far west; Tar-Minastir built a tower on it to gaze west'),
 ('HI07', 'Highlands of the Andustar', 'Hills', L(A_AN, 360, -38), [L(A_AN, 250, -46), L(A_AN, 310, -48), L(A_AN, 370, -46), L(A_AN, 430, -40)], 720, 18, 'descriptive name: the rocky northern Andustar, high land with fir-woods above the northern cliffs'),
 ('HI08', 'Hills of Orrostar', 'Hills', L(A_OR, 400, 30), [L(A_OR, 320, 40), L(A_OR, 380, 42), L(A_OR, 440, 34), L(A_OR, 475, 22)], 620, 17, 'approx: descriptive name; the highlands toward the northern end of the Orrostar'),
 ('MT04', 'Cliffs of Hyarnustar', 'Mountains', L(A_HN, 420, -48), [L(A_HN, 300, -50), L(A_HN, 360, -54), L(A_HN, 420, -52), L(A_HN, 480, -40)], 1100, 18, 'descriptive name: the mountainous west of the Hyarnustar, ending in great cliffs on the sea'),
]
# raised ground: polygon, metres added
PLATEAUS = [
 ('mittalmar', [L(a, 182 if a % 72 == A_OR % 72 else 185, 0) for a in range(A_OR, A_OR + 360, 24)], 280),
 ('arandor', ell(735, 605, 45, 35, 14), 60),
]
PLATEAU_SIGMA = {'mittalmar': 22, 'arandor': 14}

ARM = (722, 602)             # Armenelos, in Arandor east of the mountain
ROM = L(-20, 117, 0)         # Rómenna at the head of its firth
AND_ = L(A_AN, 466, -14)     # Andúnië at the head of its bay in the far west of the Andustar
ELD = L(196, 194, 0)         # Eldalondë at the head of the Bay of Eldanna, at the mouth of the Nunduinë
OND = L(A_FO, 205, 4)        # Ondosto in the south of the Forostar
NOI = (MEN[0] + 2, MEN[1] - 24)   # Noirinan, the Valley of the Tombs, between the SW and SE roots

# id, name, label point, points, hint  (drawn source to mouth)
RIVERS = [
 ('RI01', 'Siril', (MEN[0] + 12, 520), [NOI, (MEN[0] + 2, 575), (640, 535), (637, 495), (639, 462), (636, 428), L(266, 222, 0)], 'chief river of Númenor: rises under the Meneltarma in Noirinan and runs south to the sea through marshes and reedy flats'),
 ('RI02', 'Nunduinë', (540, 588), [(588, 612), (560, 600), (532, 588), (511, 581), (494, 576), (474, 572), ELD, L(196, 214, 0)], 'river of the west that spreads into the lake Nísinen and reaches the sea at Eldalondë in the Bay of Eldanna'),
 ('RI03', None, None, [L(A_HR, 330, 10), L(A_HR, 380, 30), L(A_HR, 420, 58), L(A_HR, 440, 74)], ''),
 ('RI04', None, None, [L(A_OR, 260, -10), L(A_OR, 300, -40), L(A_OR, 330, -72), L(A_OR, 345, -86)], ''),
 ('RI05', None, None, [L(A_HN, 300, 10), L(A_HN, 340, 40), L(A_HN, 370, 70), L(A_HN, 382, 86)], ''),
 ('RI06', None, None, [L(A_AN, 300, -10), L(A_AN, 330, 40), L(A_AN, 350, 70), L(A_AN, 360, 88)], ''),
]
LAKES = [
 ('LA01', 'Nísinen', ell(503, 578, 9, 5), 'small lake on the Nunduinë above Eldalondë, in the land of Nísimaldar, famed for its sweet-scented flowers'),
]
FORESTS = [
 ('FO01', 'Forests of Hyarrostar', [L(A_HR, 230, -60), L(A_HR, 320, -66), L(A_HR, 420, -60), L(A_HR, 470, -40), L(A_HR, 480, 10), L(A_HR, 430, 50), L(A_HR, 330, 56), L(A_HR, 240, 50)], 'descriptive name: the great timber woods of the south-east, where Aldarion planted many trees for ship-building'),
 ('FO02', 'Fir-woods of the Andustar', [L(A_AN, 240, -70), L(A_AN, 300, -68), L(A_AN, 380, -66), L(A_AN, 440, -60), L(A_AN, 445, -28), L(A_AN, 380, -24), L(A_AN, 300, -26), L(A_AN, 240, -30)], 'descriptive name: fir forests on the high northern Andustar facing the sea'),
 ('FO03', None, [(470, 600), (520, 610), (540, 572), (500, 548), (462, 556)], ''),
]
SWAMPS = [
 ('SW01', 'Marshes of the Siril', [(608, 466), (666, 466), (672, 424), (602, 424)], 'descriptive name: the delta of the Siril, marshes and reedy flats at the sea'),
]
ROADS = [
 ('RD01', 'Road from Rómenna to Andúnië', (505, 752), [ROM, (760, 590), ARM, (690, 604), (664, 607), NOI, (622, 612), (606, 640), (612, 690), (630, 760), OND, (600, 790), (540, 762), (470, 748), (400, 762), (330, 785), (260, 800), AND_], 'major', 'the paved highway of the kings: Rómenna, Armenelos, the Valley of the Tombs, Ondosto in the Forostar, then west to Andúnië'),
 ('RD02', 'Ascent of the Meneltarma', (MEN[0] + 30, MEN[1] - 6), [NOI, (MEN[0] + 10, MEN[1] - 14), (MEN[0] + 12, MEN[1] - 2), (MEN[0] + 2, MEN[1] + 10), (MEN[0] - 9, MEN[1] + 2), (MEN[0] - 4, MEN[1] - 6), (MEN[0] + 3, MEN[1] - 2), MEN], 'minor', 'the path that wound up the mountain from the Valley of the Tombs to the Hallow on the summit'),
]
# id, name, layer, x, y, hint
POINTS = [
 ('TO01', 'Armenelos', 'Towns', ARM[0], ARM[1], 'City of the Kings in Arandor, founded by Elros; the King\'s House and later the Temple of Sauron'),
 ('BU01', "King's Court and Nimloth", 'Buildings', ARM[0] - 9, ARM[1] + 9, 'courts of the King\'s House in Armenelos where the White Tree Nimloth grew until Ar-Pharazôn had it burned'),
 ('BU02', 'Temple of Armenelos', 'Buildings', ARM[0] + 10, ARM[1] - 9, 'the great domed temple that Sauron raised on the hill in the midst of the city; human sacrifices to Melkor'),
 ('HA01', 'Rómenna', 'Harbors', ROM[0], ROM[1], 'the great eastern haven at the head of its firth; home of the Faithful in the last days'),
 ('IS01', 'Tol Uinen', 'Islands', L(-20, 238, 4)[0], L(-20, 238, 4)[1], 'small isle in the Bay of Rómenna, hallowed to Uinen'),
 ('BU03', 'Calmindon', 'Buildings', L(-20, 238, 4)[0] + 3, L(-20, 238, 4)[1] + 2, 'the Light-tower that Aldarion built on Tol Uinen'),
 ('BA01', 'Bay of Rómenna', 'Bays', L(-20, 250, -6)[0], L(-20, 250, -6)[1], 'the eastern bay between Orrostar and Hyarrostar, with the long firth of Rómenna at its head'),
 ('HA02', 'Andúnië', 'Harbors', AND_[0], AND_[1], 'haven in the far west of the Andustar, facing toward Eressëa; seat of the Lords of Andúnië'),
 ('BU04', 'House of the Lords of Andúnië', 'Buildings', AND_[0] + 12, AND_[1] - 8, 'approx: the hall of Valandil\'s line, Lords of Andúnië, until Ar-Gimilzôr moved them to Rómenna'),
 ('BA02', 'Bay of Andúnië', 'Bays', L(A_AN, 506, -14)[0], L(A_AN, 506, -14)[1], 'bay in the far west of the Andustar on which Andúnië stands'),
 ('BU05', 'Tower of Tar-Minastir', 'Buildings', L(A_AN, 466, 34)[0], L(A_AN, 466, 34)[1], 'tall tower that Tar-Minastir built on the hill of Oromet to look toward the West'),
 ('BA03', 'Western bays of the Andustar', 'Bays', L(A_AN, 520, 30)[0], L(A_AN, 520, 30)[1], 'three small bays facing west in the high western end of the Andustar; the northernmost is the Bay of Andúnië'),
 ('HA03', 'Eldalondë', 'Harbors', ELD[0], ELD[1], 'Eldalondë the Green, haven at the mouth of the Nunduinë where the ships of the Eldar of Eressëa came'),
 ('BA04', 'Bay of Eldanna', 'Bays', L(196, 300, 0)[0], L(196, 300, 0)[1], 'the great bay between the Andustar and the Hyarnustar, facing toward Eressëa'),
 ('TO02', 'Ondosto', 'Towns', OND[0], OND[1], 'town in the south of the Forostar on the road from Armenelos west to Andúnië; near the stone-quarries'),
 ('BU06', 'Tower of Tar-Meneldur', 'Buildings', L(A_FO, 448, 18)[0], L(A_FO, 448, 18)[1], 'approx: the tall tower in the north of the Forostar near Sorontil, from which King Meneldur watched the stars'),
 ('TO03', 'Nindamos', 'Towns', 656, 428, 'chief fishing village of the south coast, on the east side of the mouths of the Siril'),
 ('VA01', 'Noirinan', 'Valleys', NOI[0] + 4, NOI[1] - 4, 'the Valley of the Tombs, between the south-west and south-east roots of the Meneltarma'),
 ('GR01', 'Tombs of the Kings', 'Graves_Tombs', NOI[0] - 2, NOI[1] + 7, 'the tombs hewn in the rock at the head of Noirinan, under the mountain'),
 ('BU07', 'Hallow of Eru', 'Buildings', MEN[0], MEN[1] + 1, 'the unroofed high place on the summit of the Meneltarma, hallowed to Eru Ilúvatar; the Three Prayers'),
 ('BU08', 'White House of Erendis', 'Buildings', 532, 518, 'approx: the house that Aldarion built for Erendis in Emerië, where she later lived apart'),
 ('FI01', 'Vineyards of Hyarnustar', 'Fields', L(A_HN, 340, 32)[0], L(A_HN, 340, 32)[1], 'descriptive name: the vine-lands in the east and south of the Hyarnustar'),
 ('FI03', 'Pastures of the Mittalmar', 'Fields', 690, 700, 'descriptive name: the raised grass-lands of the Inlands, chiefly sheep and cattle country'),
 ('FI02', 'Grain-lands of Orrostar', 'Fields', L(A_OR, 300, -30)[0], L(A_OR, 300, -30)[1], 'descriptive name: the inner Orrostar, cool but good for grain'),
]
# id, name, type, tier, x, y, radius km
REGIONS = [
 ('RG01', 'Forostar', 'region', 1, *L(A_FO, 350, 0), 170),
 ('RG02', 'Andustar', 'region', 1, *L(A_AN, 350, 0), 170),
 ('RG03', 'Hyarnustar', 'region', 1, *L(A_HN, 350, 0), 170),
 ('RG04', 'Hyarrostar', 'region', 1, *L(A_HR, 350, 0), 170),
 ('RG05', 'Orrostar', 'region', 1, *L(A_OR, 350, 0), 170),
 ('RG06', 'Mittalmar', 'region', 1, CX - 20, CY + 60, 190),
 ('RG07', 'Arandor', 'realm', 2, 748, 615, 60),
 ('RG08', 'Emerië', 'region', 2, 545, 528, 40),
 ('RG09', 'Nísimaldar', 'region', 2, 490, 560, 40),
 ('RG10', 'Hyarastorni', 'region', 3, 575, 478, 25),
]
REGION_HINTS = {'RG01': 'the Northlands, rocky and least fertile; Sorontil and Ondosto', 'RG02': 'the Westlands; Andúnië, Oromet, fir-woods in the north',
                'RG03': 'the South-west lands; vineyards and great cliffs', 'RG04': 'the South-east lands; great forests',
                'RG05': 'the Eastlands; grain and northern hills', 'RG06': 'the Inlands, raised pasture-land around the Meneltarma',
                'RG07': 'the Kingsland, the eastern Mittalmar with Armenelos and Rómenna', 'RG08': 'the sheep-pastures of the south-west Mittalmar; home of Erendis',
                'RG09': 'the land of fragrant evergreen trees around Eldalondë and the Bay of Eldanna', 'RG10': 'approx: the sheep-lands of Hallatan, kinsman of Aldarion, near Emerië'}
