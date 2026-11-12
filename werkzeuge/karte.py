"""Erzeugt die Grundkarte für karte.html (werkzeuge/karte-grund.svg).

Daten:
- Höhen: AWS Terrain Tiles (Terrarium, Zoom 14), Kacheln im Ordner KACHELN (nicht im Repo).
- Gemeindegrenzen: france-geojson (gregoiredavid), Département 62, Datei GEMEINDEN (nicht im Repo).
- Stellungen, Angriffs- und Gegenstoßpfeile: digitalisiert aus der Karte
  „27. I.D. 6.4.–5.5.17 bei Bullecourt. Schlacht am 11.4.“ in Georg von Moser:
  Die Württemberger im Weltkrieg, S. 76 (Wikimedia Commons, gemeinfrei).
  Die Karte wurde über sieben Ortslagen (Gemeindemittelpunkte) affin eingepasst;
  Restabweichung 130–780 m. Die Linien sind daher nur auf einige hundert Meter genau.
Aufruf: python3 werkzeuge/karte.py KACHELN GEMEINDEN
"""
import json, math, sys, pathlib
import numpy as np
from PIL import Image
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

KACHELN, GEMEINDEN = sys.argv[1], sys.argv[2]
OUT = pathlib.Path(__file__).resolve().parent / "karte-grund.svg"

LON0, LON1, LAT0, LAT1 = 2.885, 3.005, 50.152, 50.224
SW = 800
KX = SW / (LON1 - LON0)
KY = KX / math.cos(math.radians((LAT0 + LAT1) / 2))
SH = round((LAT1 - LAT0) * KY)

def P(lo, la):
    return ((lo - LON0) * KX, (LAT1 - la) * KY)

def f(v):
    return f"{v:.1f}"

def path(pts):
    return "M" + "L".join(f"{f(x)},{f(y)}" for x, y in pts)

# ---- Moser-Karte einpassen (Pixel der Vorlage -> lon/lat) ----
def centroid(geom):
    polys = [geom["coordinates"]] if geom["type"] == "Polygon" else geom["coordinates"]
    A = Cx = Cy = 0
    for poly in polys:
        r = poly[0]
        for i in range(len(r) - 1):
            x0, y0 = r[i]; x1, y1 = r[i + 1]; c = x0 * y1 - x1 * y0
            A += c; Cx += (x0 + x1) * c; Cy += (y0 + y1) * c
    return Cx / (3 * A), Cy / (3 * A)

gj = json.load(open(GEMEINDEN))
gem = {ft["properties"]["nom"]: ft for ft in gj["features"]}
# Ortslagen in der Vorlage (Pixel einer 3-fach vergrößerten Ansicht, Ursprung 140/150)
ORTE = {"Hendecourt-lès-Cagnicourt": (680, 100), "Cagnicourt": (1330, 90), "Riencourt-lès-Cagnicourt": (800, 290),
        "Bullecourt": (440, 430), "Écoust-Saint-Mein": (180, 620), "Quéant": (1130, 730), "Noreuil": (500, 860)}
def vor(X, Y):
    return (X / 3 + 140, Y / 3 + 150)
src = np.array([[*vor(*xy), 1] for xy in ORTE.values()])
dst = np.array([centroid(gem[n]["geometry"]) for n in ORTE])
M = np.linalg.lstsq(src, dst, rcond=None)[0]
def MP(X, Y):
    lo, la = np.array([*vor(X, Y), 1]) @ M
    return P(lo, la)

# ---- Höhenlinien ----
z, x0, x1, y0, y1, T = 14, 8321, 8329, 5539, 5546, 256
el = np.zeros(((y1 - y0 + 1) * T, (x1 - x0 + 1) * T))
for x in range(x0, x1 + 1):
    for y in range(y0, y1 + 1):
        a = np.asarray(Image.open(f"{KACHELN}/{z}_{x}_{y}.png").convert("RGB")).astype(float)
        el[(y - y0) * T:(y - y0 + 1) * T, (x - x0) * T:(x - x0 + 1) * T] = a[:, :, 0] * 256 + a[:, :, 1] + a[:, :, 2] / 256 - 32768
from numpy.lib.stride_tricks import sliding_window_view
k = 7
sm = sliding_window_view(np.pad(el, k // 2, mode="edge"), (k, k)).mean((2, 3))
n2 = 2 ** z
def px2ll(px, py):
    X = x0 + px / T; Y = y0 + py / T
    return X / n2 * 360 - 180, math.degrees(math.atan(math.sinh(math.pi * (1 - 2 * Y / n2))))
cs = plt.contour(sm, levels=list(range(60, 125, 5)))
minor = major = ""
for lev, segs in zip(cs.levels, cs.allsegs):
    d = ""
    for s in segs:
        pts = [P(*px2ll(c[0], c[1])) for c in s]
        pts = [p for p in pts if -10 < p[0] < SW + 10 and -10 < p[1] < SH + 10]
        if len(pts) < 10:
            continue
        q = [pts[0]]
        for p in pts[1:]:
            if math.hypot(p[0] - q[-1][0], p[1] - q[-1][1]) > 4:
                q.append(p)
        if len(q) > 3:
            d += path(q)
    if int(lev) % 20 == 0:
        major += d
    else:
        minor += d

# ---- Gemeindegrenzen ----
grenzen = ""
for ft in gj["features"]:
    g = ft["geometry"]
    polys = [g["coordinates"]] if g["type"] == "Polygon" else g["coordinates"]
    for poly in polys:
        pts = [P(lo, la) for lo, la in poly[0]]
        if all(not (-50 < x < SW + 50 and -50 < y < SH + 50) for x, y in pts):
            continue
        grenzen += path(pts) + "Z"

# ---- Linien aus der Moser-Karte (Pixel der vergrößerten Ansicht) ----
OG1 = [(135,290),(240,320),(300,345),(340,400),(370,460),(430,495),(480,500),(530,460),(570,430),(620,440),(680,465),(760,480),(840,490),(880,505),(905,540),(920,600),(930,660),(960,720),(1015,800)]
OG2 = [(250,300),(330,330),(420,355),(490,378),(560,382),(640,380),(700,410),(780,432),(850,440),(910,470),(945,520),(965,590),(990,660),(1010,710)]
ART = [(370,215),(470,245),(560,240),(620,265),(670,295),(740,330),(830,345),(950,390),(1060,440),(1170,480),(1240,530),(1290,580)]
ANGRIFF = {"links": [((300,600),(370,470)), ((430,640),(450,500))],
           "mitte": [((590,650),(665,360)), ((670,690),(800,410))],
           "rechts": [((800,665),(880,585)), ((820,820),(920,725))]}
GEGEN = [((500,340),(630,445)), ((665,205),(665,290)), ((770,335),(710,390)), ((800,345),(785,410)), ((940,345),(880,395)), ((950,455),(740,480))]

def pl(pts):
    return path([MP(*p) for p in pts])
def pfeil(a, b, cls, step):
    (ax, ay), (bx, by) = MP(*a), MP(*b)
    ang = math.atan2(by - ay, bx - ax); L = 17; w = 0.55
    h1 = (bx - L * math.cos(ang - w), by - L * math.sin(ang - w)); h2 = (bx - L * math.cos(ang + w), by - L * math.sin(ang + w))
    sx, sy = bx - 0.8 * L * math.cos(ang), by - 0.8 * L * math.sin(ang)
    return (f'<g class="{cls}" data-s="{step}"><path class="halo" d="M{f(ax)},{f(ay)}L{f(sx)},{f(sy)}"/><path d="M{f(ax)},{f(ay)}L{f(sx)},{f(sy)}"/>'
            f'<path class="spitze" d="M{f(h1[0])},{f(h1[1])}L{f(bx)},{f(by)}L{f(h2[0])},{f(h2[1])}Z"/></g>')

orte_svg = ""
LABEL = {"Hendecourt-lès-Cagnicourt": ("Hendecourt", 0, -12), "Cagnicourt": ("Cagnicourt", -30, -12), "Riencourt-lès-Cagnicourt": ("Riencourt", 26, -12),
         "Bullecourt": ("Bullecourt", -10, 24), "Écoust-Saint-Mein": ("Écoust", 0, 22), "Quéant": ("Quéant", 0, 24), "Noreuil": ("Noreuil", 0, 24)}
for n, xy in ORTE.items():
    x, y = MP(*xy); t, dx, dy = LABEL[n]
    orte_svg += f'<g class="ort"><circle cx="{f(x)}" cy="{f(y)}" r="9"/><text x="{f(x+dx)}" y="{f(y+dy)}">{t}</text></g>'

kx, ky = MP(665, 330); mx, my = MP(875, 415)
punkte = (f'<g class="pkt"><circle cx="{f(kx)}" cy="{f(ky)}" r="3"/><text x="{f(kx+6)}" y="{f(ky-5)}">Kapelle</text></g>'
          f'<g class="pkt"><circle cx="{f(mx)}" cy="{f(my)}" r="3"/><text x="{f(mx+6)}" y="{f(my-5)}">Sanssouci-Mühle</text></g>')

# ---- Truppensymbole (schematisch): Raute = Infanterie, Rechteck = Panzer ----
def inf(xy, seite, label, step, dx=0, dy=-18, titel=""):
    x, y = MP(*xy); r = 12
    t = f'<title>{titel or label}</title>'
    lab = f'<text x="{f(x+dx)}" y="{f(y+dy)}">{label}</text>' if label else ""
    return (f'<g class="u inf {seite}" data-s="{step}">{t}<path d="M{f(x)},{f(y-r)}L{f(x+r)},{f(y)}L{f(x)},{f(y+r)}L{f(x-r)},{f(y)}Z"/>{lab}</g>')
def pz(x, y, nr, step, aus=False):
    w, h = 20, 12
    kreuz = f'<path class="x" d="M{f(x-w/2-2)},{f(y-h/2-2)}L{f(x+w/2+2)},{f(y+h/2+2)}M{f(x+w/2+2)},{f(y-h/2-2)}L{f(x-w/2-2)},{f(y+h/2+2)}"/>' if aus else ""
    return (f'<g class="u pz{" aus" if aus else ""}" data-s="{step}"><title>Panzer {nr}{", ausgeschaltet" if aus else ""}</title>'
            f'<rect x="{f(x-w/2)}" y="{f(y-h/2)}" width="{w}" height="{h}" rx="1.5"/>{kreuz}</g>')

reg = ""
# Deutsche Regimenter (Moser), alle Schritte
for t, xy, tt in (("IR 120", (420, 300), "Infanterie-Regiment 120"), ("IR 124", (780, 190), "Infanterie-Regiment 124"), ("GR 123", (1035, 495), "Grenadier-Regiment 123")):
    reg += inf(xy, "de", t, "1 2 3 4 5", titel=tt)

# Panzer je Sektion: Lage am 11.04. früh (Schritt 3) und Endlage (Schritt 4), Anteil entlang des Sektionspfeils
SEKT_PZ = {"rechts": [("593", .15, True), ("711", .3, True), ("586", 1.05, True), ("799", .95, True)],
           "mitte": [("702", -.05, False), ("585", .25, True), ("590", .85, True), ("798", .12, False)],
           "links": [("796", 1.0, True), ("797", .9, True), ("531", .7, True), ("800", .45, True)]}
einheiten = ""
for sk, lst in SEKT_PZ.items():
    (a1, b1), (a2, b2) = ANGRIFF[sk]
    A = [(MP(*a1)[i] + MP(*a2)[i]) / 2 for i in (0, 1)]; B = [(MP(*b1)[i] + MP(*b2)[i]) / 2 for i in (0, 1)]
    ang = math.atan2(B[1] - A[1], B[0] - A[0]); nx, ny = -math.sin(ang), math.cos(ang)
    for i, (nr, t, aus) in enumerate(lst):
        o = (i - 1.5) * 22
        einheiten += pz(A[0] + (B[0] - A[0]) * .12 + nx * o, A[1] + (B[1] - A[1]) * .12 + ny * o, nr, "3")
        einheiten += pz(A[0] + (B[0] - A[0]) * t + nx * o, A[1] + (B[1] - A[1]) * t + ny * o, nr, "4", aus)

# 10.04.: Infanterie vor dem Draht, Panzer bleiben im Schnee zurück
einheiten += inf((560, 640), "al", "", "2", titel="Australische Infanterie, 10.04.") + inf((700, 660), "al", "4. austr. Div.", "2", dx=0, dy=24, titel="4. australische Division, 10.04.")
for i, x in enumerate((540, 590, 640, 690)):
    X, Y = MP(x, 1010); einheiten += pz(X, Y, "der 11. Kompanie, verspätet", "2")
nX, nY = MP(620, 1040)
einheiten += f'<text class="ulab" data-s="2" x="{f(nX)}" y="{f(nY+8)}">Panzer im Schnee verspätet</text>'
# 11.04.: australische Infanterie hinter den Panzern, dann in den Gräben
einheiten += inf((505, 665), "al", "4. austr. Div.", "3", dy=-18, titel="4. australische Division") + inf((735, 690), "al", "", "3", titel="4. australische Division")
einheiten += inf((560, 430), "al", "", "4", titel="Australier im Einbruch") + inf((640, 420), "al", "", "4", titel="Australier im Einbruch") + inf((740, 470), "al", "", "4", titel="Australier im Einbruch")
# Mai: 2. austr. Division und britische 62. Division
einheiten += inf((620, 650), "al", "", "5", titel="2. australische Division") + inf((760, 670), "al", "2. austr. Div.", "5", dy=24, titel="2. australische Division")
einheiten += inf((260, 640), "al", "62. brit. Div.", "5", dy=24, titel="Britische 62. Division") + inf((360, 660), "al", "", "5", titel="Britische 62. Division")
for i, (x, y) in enumerate(((230, 585), (275, 597), (320, 609), (365, 621))):
    X, Y = MP(x, y); einheiten += pz(X, Y, "der 12. Kompanie (bei der 62. Division)", "5")
MAI = [((640, 630), (640, 470)), ((760, 650), (760, 500)), ((300, 580), (390, 470))]
mai = "".join(pfeil(a, b, "angriff mai", "5") for a, b in MAI)
RUECK = [((630, 620), (630, 760))]
rueck = "".join(pfeil(a, b, "rueck", "2") for a, b in RUECK)

# Kennzeichnung der Seiten mit Hoheitszeichen (wie Richthofen-Karte)
def kreuz(x, y):
    return (f'<g class="emb" transform="translate({f(x)},{f(y)})"><rect x="-11" y="-11" width="22" height="22" fill="#fff" stroke="#000" stroke-width=".5"/>'
            '<path d="M-3.4,-10 L3.4,-10 L1.4,-1.4 L10,-3.4 L10,3.4 L1.4,1.4 L3.4,10 L-3.4,10 L-1.4,1.4 L-10,3.4 L-10,-3.4 L-1.4,-1.4 Z" fill="#111"/></g>')
def roundel(x, y):
    return (f'<g class="emb" transform="translate({f(x)},{f(y)})"><circle r="11" fill="#1f3a8a" stroke="#fff" stroke-width="1"/><circle r="7.3" fill="#fff"/><circle r="3.6" fill="#c8202f"/></g>')
seiten = ""
for xy in ((300, 180), (1050, 300)):
    x, y = MP(*xy); seiten += kreuz(x, y)
for xy in ((250, 820), (900, 920)):
    x, y = MP(*xy); seiten += roundel(x, y)
x, y = MP(300, 180); seiten += f'<text class="seite" x="{f(x+18)}" y="{f(y+5)}">deutsche Seite</text>'
x, y = MP(250, 820); seiten += f'<text class="seite" x="{f(x+18)}" y="{f(y+5)}">britische und australische Seite</text>'

ang = "".join(pfeil(a, b, "angriff " + sek, "3 4") for sek, lst in ANGRIFF.items() for a, b in lst)
geg = "".join(pfeil(a, b, "gegen", "4") for a, b in GEGEN)

# Sektionsschilder der Panzer am Ausgangspunkt der Angriffspfeile
sek = ""
for key, name in (("links", "Links"), ("mitte", "Mitte"), ("rechts", "Rechts")):
    (a, _), (c, _) = ANGRIFF[key]
    x = (MP(*a)[0] + MP(*c)[0]) / 2; y = max(MP(*a)[1], MP(*c)[1]) + 18
    sek += (f'<g class="sek" data-s="3 4" data-sek="{key}" tabindex="0" role="button" aria-label="Panzer der Sektion {name}">'
            f'<rect x="{f(x-34)}" y="{f(y-12)}" width="68" height="22" rx="2"/><text x="{f(x)}" y="{f(y+4)}">{name}</text></g>')

# Maßstab 1 km
km = KX / (111.32 * math.cos(math.radians((LAT0 + LAT1) / 2)))  # Pixel je km
mx0, my0 = 20, SH - 22
massstab = (f'<g class="mst"><path d="M{mx0},{my0}h{f(km)}M{mx0},{my0-4}v8M{f(mx0+km)},{my0-4}v8"/>'
            f'<text x="{f(mx0+km/2)}" y="{my0-8}">1 km</text></g>')
nord = f'<g class="nord"><path d="M{SW-26},{SH-20}l8,-26l8,26l-8,-6z"/><text x="{SW-18}" y="{SH-52}">N</text></g>'

svg = f"""<svg class="karte-svg" viewBox="0 0 {SW} {SH}" role="img" aria-labelledby="kTitel" xmlns="http://www.w3.org/2000/svg">
<title id="kTitel">Karte des Gefechtsfelds bei Bullecourt mit Siegfriedstellung, Angriffsrichtungen und Gegenstößen</title>
<rect class="grund" width="{SW}" height="{SH}"/>
<path class="hl-minor" d="{minor}"/>
<path class="hl-major" d="{major}"/>
<path class="gemeinde" d="{grenzen}"/>
{orte_svg}
<path class="art" d="{pl(ART)}"/>
<path class="og2" d="{pl(OG2)}"/>
<path class="og1" d="{pl(OG1)}"/>
<path class="og1-hi" data-s="4" d="{pl(OG1[3:13])}"/>
{punkte}
{seiten}
{rueck}
{ang}
{mai}
{geg}
{reg}
{einheiten}
{sek}
{massstab}
{nord}
</svg>"""
OUT.write_text(svg, encoding="utf-8")
print(OUT, len(svg), "Zeichen", SW, SH)
