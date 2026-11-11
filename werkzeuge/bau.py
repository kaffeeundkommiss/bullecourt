"""Erzeugt die HTML-Seiten der Bullecourt-Seite aus einer gemeinsamen Vorlage.
Aufruf: python3 werkzeuge/bau.py (im Repo-Wurzelverzeichnis)."""
import pathlib

BASE = "https://kaffeeundkommiss.github.io/bullecourt/"
ROOT = pathlib.Path(__file__).resolve().parent.parent

def q(*ids):
    return "".join(f'<a href="quellen.html#q{i}">Q{i}</a>' for i in ids)

def b(kind):
    return {"ok": '<span class="b ok">belegt</span>', "part": '<span class="b part">teilweise</span>',
            "one": '<span class="b one">eine Quelle</span>', "wid": '<span class="b wid">Widerspruch</span>'}[kind]

def meta(kind, *ids, text=""):
    return f'<div class="meta">{b(kind)}{text}{q(*ids)}</div>'

NAV = [("index.html", "Schlachten"), ("panzer.html", "Panzer"), ("grabungen.html", "Grabungen")]

def page(fn, title, desc, eyebrow, h1, body, current):
    nav = "\n".join(
        f'      <a href="{h}"{" aria-current=\"page\"" if h == current else (" aria-current=\"true\"" if current == "quellen" and False else "")}>{t}</a>'
        for h, t in NAV)
    html = f"""<!doctype html>
<html lang="de" class="kk-b-gesch">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{BASE}{'' if fn == 'index.html' else fn}">
<meta property="og:type" content="website">
<meta property="og:locale" content="de_DE">
<meta property="og:site_name" content="Erster Weltkrieg">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{BASE}{'' if fn == 'index.html' else fn}">
<meta name="theme-color" content="#23211C" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#12110E" media="(prefers-color-scheme: dark)">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="Bullecourt 1917">
<link rel="icon" href="icons/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" sizes="180x180" href="icons/apple-touch-icon.png">
<link rel="manifest" href="manifest.webmanifest">
<link rel="stylesheet" href="site.css">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@500;600;700&family=Source+Serif+4:opsz,wght@8..60,400;8..60,600&family=IBM+Plex+Sans:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500;600&display=swap">
<link rel="stylesheet" href="basis.css">
<link rel="stylesheet" href="seite.css">
<link rel="stylesheet" href="bereich.css">
</head>
<body>
<div class="kk-leiste"><div class="kk-in">
  <a class="kk-haus" href="https://kaffeeundkommiss.github.io/"><img src="kk-tasse.svg" alt="" width="22" height="22"><span>Kaffee und Kommiss</span></a>
  <nav class="kk-bereiche" aria-label="Bereiche"><a href="https://kaffeeundkommiss.github.io/geschichte/" aria-current="true">Geschichte</a><a href="https://kaffeeundkommiss.github.io/bundeswehr-Afghanistan-/"><span class="kk-lang">Sicherheitspolitik</span><span class="kk-kurz">Sicherheit</span></a><a href="https://kaffeeundkommiss.github.io/politik/">Politik</a></nav>
</div></div>
<div class="kk-kopf"><div class="kk-in">
  <a class="kk-schild" href="index.html"><img src="icons/favicon.svg" alt="" width="44" height="44"><span><span class="kk-name" style="display:block">Bullecourt 1917</span><span class="kk-unter" style="display:block">Panzer und Infanterie an der Hindenburglinie</span></span></a>
</div></div>
<div class="wrap">
  <header>
    <div class="brand"><div class="brand-text">
      <div class="eyebrow">{eyebrow}</div>
      <h1>{h1}</h1>
    </div></div>
    <nav class="pages" aria-label="Seiten">
{nav}
    </nav>
  </header>
{body}
  <p class="qnav"><a class="qbtn" href="quellen.html">Quellen</a></p>
</div>
<footer class="kk-fuss"><div class="kk-in">
  <p><a href="https://kaffeeundkommiss.github.io/">Kaffee und Kommiss</a>: Politik, Geschichte und Sicherheitspolitik mit Quellen. Private, nichtkommerzielle Zusammenstellung. Fehler gefunden? Bitte mit Quelle melden.</p>
</div></footer>
</body>
</html>
"""
    (ROOT / fn).write_text(html, encoding="utf-8")

STATUS = """  <section class="sect" aria-labelledby="stH">
    <h2 id="stH">Belegstatus</h2>
    <ul class="status">
      <li><span class="b ok">belegt</span>zwei unabhängige Quellen</li>
      <li><span class="b part">teilweise</span>zwei Quellen, aber voneinander abhängig</li>
      <li><span class="b one">eine Quelle</span>nicht ausreichend belegt</li>
      <li><span class="b wid">Widerspruch</span>Quellen widersprechen sich</li>
    </ul>
    <p class="note">Stand der Recherche: 11.11.2026. Verlustzahlen sind Angaben der jeweiligen Seite; Abgrenzungen (Tote, Verwundete, Gefangene) unterscheiden sich je Quelle.</p>
  </section>
"""

def item(t, h, text, metas, key=False, why=""):
    w = f'\n          <p class="why">{why}</p>' if why else ""
    return f"""      <li{' class="key"' if key else ''}>
        <div class="t">{t}</div><div class="rail"></div>
        <div class="card">
          <h3>{h}</h3>
          <p>{text}</p>
          {''.join(metas)}{w}
        </div>
      </li>
"""

# ---------- index.html: Schlachten ----------
stats = f"""  <section class="sect" aria-labelledby="zH">
    <h2 id="zH">Zwei Angriffe in Zahlen</h2>
    <div class="stats">
      <div class="stat red"><div class="num">11</div><div class="lbl">Panzer im Angriff am 11.04.1917, geplant waren 12</div>{meta("ok", 2, 6, 7)}</div>
      <div class="stat red"><div class="num">9</div><div class="lbl">davon ausgeschaltet, zwei kamen zurück</div>{meta("ok", 2, 7)}<p class="why">Andere Fassung: alle zerstört (<a href="quellen.html#q5">Q5</a>).</p></div>
      <div class="stat"><div class="num">≈ 3.300</div><div class="lbl">australische Verluste am 11.04., davon rund 1.170 Gefangene</div>{meta("wid", 3, 5, 13)}<p class="why">Q5: 3.330 einschließlich 1.170 Gefangener; Q13: 3.289 einschließlich 1.166; Q3: 3.000 Tote und Verwundete plus 1.170 Gefangene.</p></div>
      <div class="stat"><div class="num">2.339</div><div class="lbl">Verluste der 4. australischen Brigade, von rund 3.000 Mann</div>{meta("ok", 3, 6)}</div>
      <div class="stat"><div class="num">≈ 7.000</div><div class="lbl">australische Verluste im Mai 1917</div>{meta("ok", 3, 4, 5)}</div>
      <div class="stat"><div class="num">8.119</div><div class="lbl">britische Verluste im Mai 1917</div>{meta("one", 5)}</div>
    </div>
  </section>
"""

tl1 = "".join([
    item("März 1917", "Rückzug auf die Hindenburglinie",
         "Das deutsche Heer zieht sich auf eine vorbereitete Stellung zurück, die die Alliierten Hindenburglinie nennen. Bullecourt liegt in einem vorspringenden Bogen dieser Linie, zwischen den Dörfern Riencourt und Quéant.",
         [meta("ok", 3, 13)]),
    item("April 1917", "Plan ohne Artillerie",
         "Die britische Offensive bei Arras beginnt am 9. April. Als Ergänzung soll die 5. Armee unter General Hubert Gough bei Bullecourt angreifen. Weil Geschütze und Munition fehlen, sollen zwölf Panzer den Stacheldraht für die 4. australische Division öffnen.",
         [meta("ok", 4, 1)], why="Q1 nennt als Ursachen auch zu kurze Vorbereitung und Planänderungen am Vorabend."),
    item("10.04.1917", "Angriff abgesagt",
         "Die Panzer kommen im Schneetreiben nicht rechtzeitig nach vorn. Der Angriff wird kurzfristig abgesagt; die australischen Bataillone ziehen sich zurück. Die britische 62. Division schickt Patrouillen vor und erleidet Verluste.",
         [meta("ok", 1, 4, 6)]),
    item("11.04.1917, 04:30", "Nullstunde", "Elf Panzer der 11. Kompanie, D-Bataillon, gehen vor, mehrere verspätet. Auf dem verschneiten Feld sind sie bei Tagesanbruch gut zu sehen. Die australische Infanterie dringt in die ersten beiden Gräben der Hindenburglinie ein.",
         [meta("ok", 1, 6, 13, text="Nullstunde, Schnee, Einbruch: "), meta("wid", 7, 13, text="Wie viele pünktlich: Q7 elf im Einsatz, Q13 nur vier an der Ausgangslinie: ")], key=True),
    item("11.04.1917, vormittags", "Panzer brennen, Infanterie abgeschnitten",
         "Die meisten Panzer werden bis etwa 7 Uhr von Artillerie und panzerbrechender MG-Munition ausgeschaltet. Die Australier halten Teile der Gräben, bekommen aber weder Nachschub noch Artillerieunterstützung. Deutsche Gegenangriffe drängen sie zurück; viele geraten in Gefangenschaft.",
         [meta("ok", 1, 3, 4)], key=True),
    item("11.04.1917", "Bilanz",
         "Die 4. australische Division verliert rund 3.300 Mann, davon etwa 1.170 als Gefangene. Bullecourt bleibt in deutscher Hand. Verteidiger ist die 27. (württembergische) Division.",
         [meta("ok", 3, 13, text="Verteidiger: "), meta("wid", 3, 5, 13, text="Verlustzahl: ")]),
])

tl2 = "".join([
    item("03.05.1917, 03:45", "Zweiter Angriff",
         "Die 2. australische Division greift über dasselbe Gelände an, diesmal mit Artillerievorbereitung. Links greift die britische 62. Division an, begleitet von acht Panzern der 12. Kompanie. Bei den Australiern fahren keine Panzer.",
         [meta("ok", 3, 4, 5, text="Angriff: "), meta("one", 3, text="keine Panzer bei den Australiern: "), meta("one", 14, text="acht Panzer, 03:45: ")], key=True),
    item("03.05.1917", "Panzer bei der 62. Division",
         "Drei der acht Panzer werden ausgeschaltet, mehrere durch panzerbrechende Geschosse beschädigt. Bullecourt bleibt an diesem Tag deutsch.",
         [meta("one", 14)], why="Q14 ist in sich widersprüchlich (fünf oder sechs Panzer zurück). Q6 bestätigt nur, dass Panzer mit der 62. Division die deutschen Linien erreichten."),
    item("Mai 1917", "Zermürbungskampf",
         "Die Australier halten einen Einbruch in die Hindenburglinie. Die 1. und später die 5. australische Division lösen die 2. ab. Bis zum 15. Mai wehren sie mehrere Gegenangriffe ab.",
         [meta("ok", 3, 4, 5)]),
    item("17. oder 20.05.1917", "Ende der Kämpfe",
         "Die Kämpfe enden. Australien verliert rund 7.000 Mann, Großbritannien gut 8.000.",
         [meta("wid", 5, 3, text="Ende 17.05. (Q5) oder 20.05. (Q3): "), meta("ok", 3, 4, 5, text="≈ 7.000: ")]),
])

intro = f"""  <section class="sect">
    <p class="lede">Bei Bullecourt in Nordfrankreich griffen im April und Mai 1917 australische und britische Truppen die Hindenburglinie an. Im ersten Angriff am 11. April sollten Panzer die fehlende Artillerie ersetzen. Der Angriff scheiterte, und die Australier gaben lange den Panzerbesatzungen die Schuld. Neuere Forschung und Grabungen von Veteranen zeichnen ein anderes Bild. Jede Aussage trägt ihren Belegstatus.</p>
  </section>
"""

deut = f"""  <section class="sect" aria-labelledby="dH">
    <h2 id="dH">Warum scheiterte der erste Angriff?</h2>
    <div class="theses">
      <article class="th lead">
        <h3>Die Panzer versagten</h3>
        <p class="who2">zeitgenössische australische Sicht</p>
        <dl>
          <dt>Kern</dt><dd>Die Panzer kamen zu spät, blieben liegen oder fuhren zurück. Ohne sie lief die Infanterie ungeschützt in den Draht. Australische Offiziere warfen den Besatzungen Feigheit vor.</dd>
          <dt>Folge</dt><dd>Die Australier misstrauten Panzern bis zur Schlacht bei Hamel im Juli 1918 (nur <a href="quellen.html#q3">Q3</a>).</dd>
        </dl>
        <div class="meta">{q(1, 4, 9)}</div>
      </article>
      <article class="th">
        <h3>Der Plan war das Problem</h3>
        <p class="who2">Watson 1920; Brown und Brooks 2023</p>
        <dl>
          <dt>Kern</dt><dd>Zu hastige Vorbereitung, Planänderung am Vorabend, schwache Artillerie und zu wenige, veraltete Panzer gegen einen schmalen Frontbogen. Die Panzer handelten fast ohne Führung und einzeln.</dd>
          <dt>Einschränkung</dt><dd>Auch diese Sicht bestreitet nicht, dass die Panzer ihren Auftrag nicht erfüllten.</dd>
        </dl>
        <div class="meta">{q(1)}</div>
      </article>
      <article class="th">
        <h3>Führungsfehler oben</h3>
        <p class="who2">AWM, WFA</p>
        <dl>
          <dt>Kern</dt><dd>Gough plante schlecht und drängte zum Angriff. Die WFA sieht das erste Scheitern auch bei australischer Führung. Bean schrieb, Bullecourt habe das Vertrauen der Australier in die britische Führung erschüttert.</dd>
        </dl>
        <div class="meta">{q(4, 3, 6)}</div>
      </article>
    </div>
    <p class="note">Gesichert sind die Abläufe; die Gewichtung der Ursachen ist Deutung.</p>
  </section>
"""

body = intro + STATUS + stats + f"""  <section class="sect" aria-labelledby="t1H">
    <h2 id="t1H">Erster Angriff: April 1917</h2>
    <ol class="tl">
{tl1}    </ol>
  </section>
  <section class="sect" aria-labelledby="t2H">
    <h2 id="t2H">Zweiter Angriff: Mai 1917</h2>
    <ol class="tl">
{tl2}    </ol>
  </section>
""" + deut
page("index.html", "Bullecourt 1917", "Die Schlachten bei Bullecourt im April und Mai 1917, Schwerpunkt Panzer: Ablauf, Zahlen, Deutungen, mit Belegstatus je Aussage.",
     "Westfront · April und Mai 1917", "Die Schlachten bei Bullecourt", body, "index.html")

# ---------- panzer.html ----------
rows = [
    ("Rechts", "593", "Lt. Morris", "Im Anmarsch festgefahren, später getroffen; Wrack an der Tank Avenue", "lost"),
    ("Rechts", "711", "Lt. Puttock", "Zog 796 über den Bahndamm, Kupplung defekt, aufgegeben", "lost"),
    ("Rechts", "586", "Lt. Clarkson", "Über die erste Linie bis zur zweiten, beim Rückweg getroffen; Teile der Besatzung gefangen", "lost"),
    ("Rechts", "799", "Lt. Davies", "Über die erste Linie, vor der zweiten getroffen; erbeutet, von den Deutschen untersucht", "lost"),
    ("Mitte", "702", "Lt. Head", "Vor dem Angriff liegen geblieben", "back"),
    ("Mitte", "585", "Lt. McElvaine", "Kurz nach dem Start getroffen", "lost"),
    ("Mitte", "590", "Lt. Money", "Im Draht der ersten Linie festgefahren, mit Handgranaten in Brand gesetzt", "lost"),
    ("Mitte", "798", "Lt. Bernstein", "Früh getroffen, Fahrer getötet; kam nicht ins Gefecht", "back"),
    ("Links", "796", "Lt. Skinner", "Spät über den Bahndamm, bis Bullecourt; im Trichter liegen geblieben, Besatzung zurück", "lost"),
    ("Links", "797", "Lt. Birkett", "Gegen 06:30 vorn, bekämpfte ein MG in Bullecourt, später am Bahndamm ausgeschaltet", "lost"),
    ("Links", "531", "unbekannt", "Vor dem Draht östlich Bullecourt getroffen; Endlage unsicher", "lost"),
    ("Links", "800", "Lt. Richards?", "Beim Rückweg bei Vraucourt Copse ausgeschaltet", "lost"),
]
trs = "\n".join(f'        <tr class="{c}"><td>{s}</td><td class="num">{n}</td><td>{k}</td><td>{t}</td></tr>' for s, n, k, t, c in rows)

tech = f"""  <section class="sect" aria-labelledby="tH">
    <h2 id="tH">Die Fahrzeuge</h2>
    <div class="prose">
      <p>Eingesetzt wurde die 11. Kompanie des D-Bataillons der Heavy Branch, Machine Gun Corps, unter Major William H. L. Watson. Die neuen Mark IV waren noch nicht verfügbar. Die Kompanie fuhr ältere Mark I und Mark II; die Mark II waren als Ausbildungsfahrzeuge gebaut.</p>
      {meta("ok", 1, 2, text="Kompanie und Führer: ")}
      {meta("wid", 1, 6, 7, 15, text="Typ: Mark I und II (Q1, Q6) oder nur Mark II (Q7, Q15): ")}
      <p>Ein Mark II wog rund 28 Tonnen und fuhr höchstens 4 Meilen, rund 6 km/h. Die Besatzungen saßen nach Brown und Brooks in 35 bis 37 Stunden 14 bis 16 Stunden im Fahrzeug, mit Kohlenmonoxid und Hitze.</p>
      {meta("one", 7, text="Gewicht, Tempo: ")}{meta("one", 1, text="Belastung der Besatzung: ")}
    </div>
  </section>
"""

table = f"""  <section class="sect" aria-labelledby="pH">
    <h2 id="pH">Die zwölf Panzer am 11. April</h2>
    <p class="hint">Rote Kante: ausgeschaltet oder aufgegeben. Grüne Kante: nicht im Gefecht verloren. Einzelschicksale nach Kriegstagebuch-Auswertungen; Q1 und Q2 nutzen teils dieselben Akten.</p>
    <div class="meta">{b("part")}{q(1, 2)}</div>
    <div class="tblwrap"><table class="tbl">
      <thead><tr><th>Sektion</th><th>Nr.</th><th>Kommandant</th><th>Verlauf</th></tr></thead>
      <tbody>
{trs}
      </tbody>
    </table></div>
    <p class="why">Ob 797 und 800 Bullecourt erreichten, bestreiten Brown und Brooks gegen die Gefechtsskizze des Bataillons. Ältere Berichte, zwei Panzer seien bis Hendecourt gekommen, wies schon der australische Amtshistoriker zurück. Kommandant von 800 nur nach Walker, zitiert in Q1.</p>
    <p class="why">Sektionsführer Lt. Hugh Swears ging zu Fuß nach vorn, um 796 zu suchen, und blieb verschollen ({q(1, 2)}).</p>
  </section>
"""

ger = f"""  <section class="sect" aria-labelledby="gH">
    <h2 id="gH">Was die Deutschen lernten</h2>
    <ol class="tl">
{item("11.04.1917", "K-Munition durchschlägt die Panzer", "Leutnant Gotthold Schabel vom Grenadier-Regiment 123 beschießt Panzer 799 auf etwa 150 m mit panzerbrechender K-Munition aus einem Maschinengewehr, bis er liegen bleibt.", [meta("ok", 1, 12, 13, text="Wirkung der K-Munition: "), meta("wid", 1, 13, text="Schusszahl: 1.200 (Q1) oder 1.500 mit 77 Durchschlägen (Q13): ")], key=True)}
{item("April 1917", "Erster erbeuteter Panzer", "Panzer 799 bleibt hinter den deutschen Linien liegen. Die Deutschen vermessen und fotografieren ihn, bauen Teile aus und machen Beschussversuche. 799 wurde einer der meistfotografierten Panzer des Krieges.", [meta("ok", 1, 12)], why="Die Panzerung: nach Q12 war 799 „completely unarmoured“, nach Q15 war der Stahl eines Bullecourt-Fundstücks „apparently unhardened“. Wie stark der Stahl war, ist widersprüchlich.")}
{item("danach", "Schlussfolgerungen", "Ein deutscher Befehl verlangt, dass die Infanterie künftig K-Munition mitführt. Nach Einschätzung des Tank Museum hielten die Deutschen den Panzer nun für langsam und verwundbar und stellten eigene Panzerpläne zurück.", [meta("one", 1, text="Befehl: "), meta("one", 12, text="Einschätzung: ")], why="Die späteren Mark IV waren gegen K-Munition geschützt (Q1).")}
    </ol>
  </section>
"""

blame = f"""  <section class="sect" aria-labelledby="sH">
    <h2 id="sH">Der Vorwurf der Feigheit</h2>
    <div class="prose">
      <p>Nach dem Angriff beschuldigten australische Kommandeure die Panzerbesatzungen der Feigheit und Unfähigkeit. Ein Bataillonskommandeur beklagte, Panzer hätten auf eigene Truppen geschossen. Major Watson hielt dagegen, seine Panzer seien nicht schuld.</p>
      {meta("ok", 1, 9, 4)}
      <p>Brown und Brooks kommen 2023 zu dem Schluss, dass sich die Vorwürfe nicht halten lassen: Etwa die Hälfte der Besatzungen fiel aus, die Panzer kamen bis an und in die Hindenburglinie. Die Grabungen von Breaking Ground Heritage stützen diese Sicht.</p>
      {meta("part", 1, 9, 16)}
      <p class="why">Deutung, keine gesicherte Tatsache. Die Ausfallquote der Besatzungen ist widersprüchlich: ca. 50 % Ausfälle (Q1) oder die Hälfte getötet (Q7).</p>
    </div>
  </section>
"""

page("panzer.html", "Bullecourt 1917: Panzer", "Die zwölf britischen Panzer am 11. April 1917 bei Bullecourt: Fahrzeuge, Einzelschicksale, deutsche Abwehr und der Vorwurf der Feigheit.",
     "Bullecourt · 11. April 1917", "Die Panzer", STATUS + tech + table + ger + blame, "panzer.html")

# ---------- grabungen.html ----------
gr = f"""  <section class="sect">
    <p class="lede">Hundert Jahre nach der Schlacht gruben britische Veteranen auf dem Schlachtfeld nach den Panzern. Organisiert wurden die Grabungen von Breaking Ground Heritage zusammen mit dem Programm Operation Nightingale des britischen Verteidigungsministeriums.</p>
  </section>
""" + STATUS + f"""  <section class="sect" aria-labelledby="bH">
    <h2 id="bH">Breaking Ground Heritage</h2>
    <div class="prose">
      <p>Breaking Ground Heritage ist eine von Veteranen geführte gemeinnützige Organisation in Großbritannien. Sie vermittelt verwundete, verletzte und kranke Soldaten und Veteranen in archäologische Projekte; im Mittelpunkt steht ihr Wohlbefinden.</p>
      {meta("ok", 8, 7)}
      <p>Gegründet wurde sie 2015 von Richard Bennett, einem früheren Royal-Marines-Unteroffizier. Bis Anfang 2019 vermittelte sie über 300 Plätze in mehr als 35 Projekten.</p>
      {meta("one", 8, text="Gründung, Zahlen: ")}
      <p class="why">Bennett ist Mitautor von Q8, die Angaben sind Selbstauskunft. Die Website der Organisation ließ sich nicht automatisch abrufen.</p>
      <p>Operation Nightingale gründeten 2011 Diarmaid Walshe und Richard Osgood, Archäologe der Defence Infrastructure Organisation. Das Programm arbeitet häufig mit Breaking Ground Heritage zusammen.</p>
      {meta("ok", 8, 7, 10)}
    </div>
  </section>
  <section class="sect" aria-labelledby="xH">
    <h2 id="xH">Die Grabungen</h2>
    <ol class="tl">
{item("Juni 2017", "Suche nach Panzer 796", "Ziel ist das Wrack des Mark II Nr. 796 von Lt. Skinner. Gefunden werden mehrere Kettenglieder, Farbreste und deutsches Wellblech („Elephant Iron“). Unter der Kette liegen zwei deutsche Soldaten.", [meta("ok", 9, 10, text="Grabung, Funde: ")], key=True, why="Q10 nennt 796 als Ziel. Ob die Kette sicher zu 796 gehört, sagt Q10 nicht.")}
{item("2017", "Zwei deutsche Soldaten", "Nach Osgood waren es vermutlich MG-Schützen, die das Wrack nach dem Ausfall als Deckung nutzten. Die Überreste wurden nach Deutschland überführt bzw. umgebettet.", [meta("ok", 9, 10, text="Funde, Umbettung: "), meta("one", 9, text="Deutung MG-Schützen: ")])}
{item("August 2017", "„Find dispels cowardice claim“", "Australische Zeitungen berichten: Die Funde zeigten, dass die Panzer im Gefecht waren und nicht geflohen sind. Osgood: Es seien Ausbildungspanzer gewesen, ungeeignet für den Einsatz.", [meta("one", 9)], why="Zeitungsbericht, gestützt auf den Grabungsleiter selbst.")}
{item("Juni 2018", "Zweite Kampagne", "Die Grabungsfläche wird erweitert. Funde: Antriebsteile, Zahnräder und eine abgefeuerte Kartusche einer 6-Pfünder-Kanone mit Prägung 1917. Das Projekt umfasst auch einen Abschnitt der Hindenburglinie. Ein Veteran legt Fuß und Stiefel eines britischen Soldaten frei.", [meta("ok", 8, 11, text="Panzer und Hindenburglinie: "), meta("one", 11, text="Einzelfunde: "), meta("one", 8, text="britischer Soldat: ")], key=True)}
{item("2018", "Kettenstück und Nachbau", "Osgood berichtet: Neben dem Granattrichter, in dem 796 liegen blieb, fanden sich Teile des Panzers, darunter rund zwei Meter Kette mit Originalfarbe, „British Racing Green“. Veteranen bauen 796 im Maßstab 2:3 aus Holz nach, gefördert vom Heritage Lottery Fund.", [meta("part", 7, 9, text="Kette, Farbe: "), meta("one", 7, text="Fundlage, Nachbau: ")])}
{item("2019", "Weitere Grabung", "Ein Vortrag des MoD-Archäologen Alex Sotheran nennt Grabungen 2017, 2018 und 2019. Sie hätten klare Belege für den Panzerangriff erbracht, die frühere Darstellungen der Schlacht umwarfen.", [meta("one", 16)])}
    </ol>
  </section>
  <section class="sect" aria-labelledby="oH">
    <h2 id="oH">Offene Punkte</h2>
    <ul class="prose">
      <li>Der Grabungsbericht „Bullecourt 2018“ von Breaking Ground Heritage liegt als PDF auf deren Website, war aber nicht abrufbar. Er dürfte Fundlage und Zuordnung zu 796 genauer belegen.</li>
      <li>Fundstücke von Mark-II-Panzern aus Bullecourt besitzt auch das Australian War Memorial; sie stammen von Anwohnern, nicht aus diesen Grabungen ({q(15)}).</li>
    </ul>
  </section>
"""
page("grabungen.html", "Bullecourt 1917: Grabungen", "Breaking Ground Heritage und Operation Nightingale: Veteranen graben 2017 bis 2019 bei Bullecourt nach Panzer 796.",
     "Bullecourt · 2017 – 2019", "Grabungen nach Panzer 796", gr, "grabungen.html")

# ---------- quellen.html ----------
SRC = [
    (1, 'David Brown, Brenton J. Brooks: „The actions of the tanks at the Battle of Bullecourt, 11 April 1917“. British Journal for Military History 9/1 (März 2023), S. 109–137. DOI 10.25602/GOLD.bjmh.v9i1.1690.', "https://bjmh.gold.ac.uk/index.php/bjmh/article/view/1690", "Fachaufsatz. Wertet Kriegstagebuch, Watson, Bean und Luftbilder aus."),
    (2, "Landships: „11 Company, 11 April 1917“. Ohne Autor und Datum.", "https://sites.google.com/site/landships/home/narratives/1917/arras-narratives/11company11april1917", "Kompilation aus Kriegstagebuch (WO 95/97), Watson, Keech 1999, Nicholls 2005. Mit Q1 teils dieselben Primärquellen."),
    (3, "Peter Burness (Australian War Memorial): „The battles for Bullecourt“. Wartime 18 (2002).", "https://www.awm.gov.au/sites/default/files/the-battles-for-bullecourt-by-peter-burness.pdf", "Gleiche Institution wie Q4 und Q15."),
    (4, "Craig Tibbitts (Australian War Memorial): „The battles for Bullecourt“. Blog, 03.04.2007, aktualisiert 30.03.2021.", "https://www.awm.gov.au/articles/blog/the-battles-for-bullecourt", "Gleiche Institution wie Q3."),
    (5, "Department of Veterans' Affairs (Australien): „Battles of Bullecourt“. Media backgrounder, ohne Datum.", "https://www.dva.gov.au/media/media-backgrounders/battles-bullecourt", ""),
    (6, "Western Front Association: „The Bullecourt Controversy“. 17.10.2008, ohne Autor.", "https://www.westernfrontassociation.com/world-war-i-articles/2008/october/the-bullecourt-controversy/", ""),
    (7, "Richard Osgood (Defence Infrastructure Organisation): „On the right track – making a tank and commemorating soldiers“. Sanctuary 47 (2018), S. 24–26, britisches Verteidigungsministerium.", "https://assets.publishing.service.gov.uk/media/5f574317e90e07098f73ee65/Sanctuary_2018_web_secured.pdf", "Osgood ist auch Gewährsmann von Q9."),
    (8, "Paul Everill, Richard Bennett, Karen Burnell: „Dig in: an evaluation of the role of archaeological fieldwork for the improved wellbeing of military veterans“. Antiquity 94 (2020), S. 212–227. DOI 10.15184/aqy.2019.85.", "https://doi.org/10.15184/aqy.2019.85", "Bennett ist Gründer von Breaking Ground Heritage."),
    (9, "Townsville Bulletin (Australien): „Find of British WWI tank dispels cowardice claim“. 19.08.2017.", "https://www.pressreader.com/australia/townsville-bulletin/20170819/283575220569377", "Stützt sich auf Richard Osgood (Q7)."),
    (10, "Storm of Steel (Blog des archäologischen Grabungsaufsehers): „Ex Joan of Arc, Bullecourt 2017“. Juni 2017.", "https://stormofsteelwargaming.blogspot.com/2017/06/ex-joan-of-arc-bullecourt-2017.html", "Teilnehmerbericht, gleicher Autor wie Q11."),
    (11, "Storm of Steel: „Ex-Joan of Arc, an Operation Nightingale Excavation at Bullecourt in France“ (Juni 2018) und „Ex Joan of Arc 2018: Official Photographs“ (Juli 2018).", "https://stormofsteelwargaming.blogspot.com/2018/06/ex-joan-of-arc-operation-nightingale.html", "Gleicher Autor wie Q10."),
    (12, "The Tank Museum, Bovington: „German Responses to the Tank“. 12.07.2017.", "https://tankmuseum.org/article/german-responses-tank", ""),
    (13, "Wikipedia (englisch): „First attack on Bullecourt“. Abruf 11.11.2026.", "https://en.wikipedia.org/wiki/First_attack_on_Bullecourt", "Tertiärquelle, stützt sich u. a. auf Bean, Walker, Sheldon."),
    (14, "Landships: „12 Company, 3 May 1917“. Ohne Autor und Datum.", "https://sites.google.com/site/landships/home/narratives/1917/arras-narratives/12company3may1917", "Kompilation, in sich teils widersprüchlich."),
    (15, "Australian War Memorial, Sammlung: REL47914 (Plattenfragment), REL47917 (Antriebsrad), REL47918 (Leitrad) eines Mark II aus Bullecourt.", "https://www.awm.gov.au/collection/C2086141", "Gleiche Institution wie Q3 und Q4."),
    (16, "Revitalising Redesdale: Ankündigung des Vortrags „Bullecourt – the search for tanks“ von Alex Sotheran (MoD). 28.01.2021.", "https://www.revitalisingredesdale.org.uk/online-archaeology-talk-video-bullecourt-the-search-for-tanks/", "MoD-Archäologe wie Osgood (Q7)."),
]
def dep(d):
    return '<br><span class="dep">' + d + '</span>' if d else ''
lis = "\n".join(f'      <li id="q{i}"><span class="id">Q{i}</span><span>{t} <a href="{u}">{u.split("//")[1]}</a>{dep(d)}</span></li>' for i, t, u, d in SRC)
qb = f"""  <section class="sect" aria-labelledby="qH">
    <h2 id="qH">Quellenverzeichnis</h2>
    <p class="hint">Alle Quellen am 11.11.2026 abgerufen. Darunter jeweils Abhängigkeiten, die beim Belegstatus berücksichtigt sind.</p>
    <ol class="srcs">
{lis}
    </ol>
  </section>
  <section class="sect" aria-labelledby="nH">
    <h2 id="nH">Nicht eingesehen</h2>
    <ul class="prose">
      <li>Breaking Ground Heritage: Website und Grabungsbericht „Bullecourt 2018“ (PDF), automatischer Abruf gesperrt.</li>
      <li>Charles Bean: Official History of Australia in the War of 1914–1918, Bd. IV.</li>
      <li>W. H. L. Watson: A Company of Tanks (1920).</li>
      <li>Jonathan Walker: The Blood Tub (1998).</li>
      <li>Deutsche Regimentsgeschichten (Grenadier-Regiment 123, Infanterie-Regiment 124) und Reichsarchiv.</li>
    </ul>
  </section>
"""
page("quellen.html", "Bullecourt 1917: Quellen", "Quellenverzeichnis der Bullecourt-Seiten mit Abruf-Stand und Abhängigkeiten.",
     "Bullecourt 1917", "Quellen", qb, "quellen")
