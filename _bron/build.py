#!/usr/bin/env python3
"""Bouwt de site van Bertrand Lafontaine als statische HTML.

Inhoud: _bron/inhoud.json (films, filmografie, tekst) + de vaste teksten hieronder.
Beelden: worden uit Input/ verkleind naar assets/beeld/ (enkel als ze nog ontbreken).

    python3 _bron/build.py
"""
import html
import json
import os
import shutil
import subprocess
import unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INPUT = os.path.join(ROOT, 'Input')
DATA = json.load(open(os.path.join(ROOT, '_bron', 'inhoud.json'), encoding='utf-8'))

E = html.escape
NIEUW_VENSTER = ' target="_blank" rel="noopener"'
HUIDIG = ' aria-current="page"'
NAAM = 'Bertrand Lafontaine'
ROL = 'Documentairemaker, auteur en moderator'


# ---------------------------------------------------------------- beelden

def _bronbestanden():
    """Map NFC-pad (relatief t.o.v. Input) -> echt pad. macOS bewaart namen in NFD."""
    m = {}
    for d, _, files in os.walk(INPUT):
        for f in files:
            echt = os.path.join(d, f)
            rel = unicodedata.normalize('NFC', os.path.relpath(echt, INPUT))
            m[rel] = echt
    return m

BRON = _bronbestanden() if os.path.isdir(INPUT) else {}


def beeld(bron, doel, maat, kwaliteit=74):
    """Verklein bron (pad in Input/) naar assets/beeld/<doel>.jpg en geef het publieke pad terug."""
    rel = f'assets/beeld/{doel}.jpg'
    uit = os.path.join(ROOT, rel)
    if not os.path.exists(uit):
        echt = BRON.get(unicodedata.normalize('NFC', bron))
        if not echt:
            raise SystemExit(f'Beeld niet gevonden in Input/: {bron}')
        os.makedirs(os.path.dirname(uit), exist_ok=True)
        subprocess.run(['sips', '-s', 'format', 'jpeg', '-s', 'formatOptions', str(kwaliteit),
                        '-Z', str(maat), echt, '--out', uit], check=True, capture_output=True)
    return rel


def video(bron, doel):
    rel = f'assets/video/{doel}.mp4'
    uit = os.path.join(ROOT, rel)
    if not os.path.exists(uit):
        os.makedirs(os.path.dirname(uit), exist_ok=True)
        shutil.copyfile(BRON[unicodedata.normalize('NFC', bron)], uit)
    return rel


# ---------------------------------------------------------------- vaste inhoud (uit masterdocument v05)

DISCIPLINES = [
    ('Film', 'film/', 'Documentaires over kunstenaars, architecten en de ideeën achter hun werk. Van persoonlijke portretten tot verhalen over de manier waarop we onze omgeving vormgeven.', 'Alle films'),
    ('Tekst', 'tekst/', 'Journalistieke artikels, interviews, publicaties en tentoonstellingsteksten. Over kunst en architectuur, maar ook over de mensen en maatschappelijke vragen die erachter schuilgaan.', 'Alle teksten'),
    ('Gesprek', 'gesprek/', 'Podcasts, interviews en panelgesprekken. Ontmoetingen waarin verschillende stemmen en perspectieven samenkomen.', 'Alle gesprekken'),
]

PODCASTS = [
    ('BINST: UNTITLED', 'Podcast · zes afleveringen', 'Met onder anderen Luc Deleu, Klaas Goris, Maarten Vanacker en Guy Mouton.', None),
    ('SILT podcast', 'Podcast', '', None),
    ('Sprekende Muren', 'Audioproject · Architectuurwijzer', '', 'In ontwikkeling'),
]

MODERATIES = [
    ('2026', 'De architect als landschapsmaker', 'Futurebuild Belgium'),
    ('2025', 'Net Zero Bouwen: hoe maken we het werkbaar en betaalbaar?', 'ARCHITECT@WORK'),
    ('2025', 'Lancering RECAST', '51N4E / M-gineers'),
    ('2024', 'Retrofit: de toekomst van duurzaam bouwen', 'ARCHITECT@WORK'),
]

# Concept: samengesteld uit de vertoningsdata in het masterdocument. Nog te bevestigen.
NIEUWS = [
    ('2026-10-17', '17.10.2026', 'Walter Leblanc in CINEMATEK',
     'Walter Leblanc: gedreven door licht wordt vertoond in CINEMATEK in Brussel, onder de titel Driven by Light.', 'film/walter-leblanc/'),
    ('2026-10-08', '08.10.2026', 'Drie films op AFFR Rotterdam',
     'Ontwerpen aan onze toekomst gaat in wereldpremière op het Architecture Film Festival Rotterdam. Heilige Huisjes? loopt er in het programma Atlas of Possibilities, en ook ARK is te zien.', 'film/ontwerpen-aan-onze-toekomst/'),
    ('2026-10-01', '01.10.2026', 'Houses for the Common Good bij WORKROOM',
     'Vijf korte documentaires over plekken die een nieuwe maatschappelijke betekenis krijgen, te zien in de tentoonstelling van WORKROOM in Brussel tot 31 maart 2027.', 'film/houses-for-the-common-good/'),
    ('2026-04-24', '24.04.2026', 'Leven in een ballon op UrbanEye',
     'De film over de ballonwoning van A.J. Lode Janssens wordt vertoond op het UrbanEye Film Festival.', 'film/leven-in-een-ballon/'),
    ('2026-01-14', '14.01.2026', 'Walter Leblanc op Canvas',
     'Het portret van de Belgische kunstenaar Walter Leblanc is te zien op Canvas en VRT MAX.', 'film/walter-leblanc/'),
    ('2025-11-17', '17.11.2025', 'Première Heilige Huisjes?',
     'Première in het Provinciehuis in Gent, tijdens de studiedag van het Departement Omgeving en Team Vlaams Bouwmeester.', 'film/heilige-huisjes/'),
]

TICKER = [
    ('', 'Nu te zien · Houses for the Common Good · WORKROOM Brussel · tot 31.03.2027', 'film/houses-for-the-common-good/'),
    ('rec', 'In productie · Unlock the Housing Stock', 'https://architectuurwijzer.be/unlock-the-housing-stock/'),
    ('', 'Onlangs op AFFR Rotterdam · Ontwerpen aan onze toekomst · Heilige Huisjes? · ARK', 'nieuws/'),
    ('', 'Onlangs in CINEMATEK · Walter Leblanc: gedreven door licht', 'film/walter-leblanc/'),
]

OVER_CITAAT = ('Life’s journey is marked by the stories we collect, not the ground we cover.', 'Francis Alÿs')
OVER = [
    'Het was nooit mijn bedoeling om documentairemaker te worden. Evenmin had ik ooit gedacht dat ik me zo zou verdiepen in de wereld van de beeldende kunst, architectuur of stedenbouw. Mijn parcours is er een van omwegen, onverwachte ontmoetingen en zijwegen die soms nergens naartoe leidden, maar evengoed deuren openden waarvan ik het bestaan niet vermoedde.',
    'Ik ben opgeleid als historicus. Misschien verklaart dat mijn fascinatie voor de verhalen achter mensen, plekken en ideeën. Daarbij schrik ik er niet voor terug om ook de meest eenvoudige vragen te stellen, of om toe te geven dat ik iets niet helemaal begrijp. Soms levert dat juist de interessantste gesprekken op.',
    'Bijna achttien jaar heb ik voor televisie gewerkt. Daar groeide mijn belangstelling voor kunst, vormgeving en architectuur en maakte ik documentaires over onder anderen Marcel Broodthaers, Francis Alÿs, René Heyvaert en Luc Deleu. Gaandeweg kwamen daar andere vertelvormen bij: journalistieke artikels, interviews, tentoonstellingsteksten, podcasts en panelgesprekken.',
    'Vandaag werk ik als onafhankelijk documentairemaker, auteur en moderator. Ik maak films, schrijf teksten en voer gesprekken. Drie disciplines die voor mij gelijkwaardig zijn en elkaar versterken. Wat ze verbindt, is de overtuiging dat achter elk betekenisvol werk een verhaal schuilgaat dat het verdient om onderzocht, bevraagd en verteld te worden.',
]
OPDRACHTGEVERS = ['VRT Canvas', 'VAi', 'KU Leuven', 'CRIT. architects', '51N4E', 'NU architectuuratelier', 'RECAST',
                  'Architectuurwijzer', 'Cera', 'VRT NWS', 'CIVA', 'WORKROOM', 'Stad Brugge', 'Stad Gent',
                  'Walter & Nicole Leblanc Foundation', 'Nederlandse Rijksoverheid', 'Louwers Mediagroep', 'NAV',
                  'bigtrees', 'Team Vlaams Bouwmeester', 'Departement Omgeving', 'Stad Leuven']

NAV = [('Film', 'film/'), ('Tekst', 'tekst/'), ('Gesprek', 'gesprek/'), ('Nieuws', 'nieuws/'), ('Over', 'over/'), ('Contact', 'contact/')]


# ---------------------------------------------------------------- hulpfuncties

def ext(url):
    return url.startswith('http')


def href(url, r):
    return url if ext(url) else r + url


def a(url, tekst, r, cls=''):
    if ext(url):
        return f'<a class="{cls} extern" href="{E(url)}" target="_blank" rel="noopener">{tekst}</a>'
    return f'<a class="{cls}" href="{r}{url}">{tekst}</a>'


def kader(inner, cls=''):
    return f'<figure class="kader {cls}"><span class="hk"></span>{inner}</figure>'


def ticker(r):
    items = ''.join(
        f'<span class="{c}"><a href="{E(href(u, r))}"{NIEUW_VENSTER if ext(u) else ""}>{E(t)}</a></span>'
        for c, t, u in TICKER)
    return f'<div class="ticker"><div class="band">{items}<span aria-hidden="true"></span>{items}</div></div>'


def pagina(pad, titel, body, actief='', beschrijving=ROL + '. Films, teksten en gesprekken over kunst, vormgeving en architectuur.', ogbeeld=None):
    diepte = pad.count('/')
    r = '../' * diepte
    nav = ''.join(
        f'<a href="{r}{u}"{HUIDIG if actief == n else ""}>{n}</a>' for n, u in NAV)
    voetnav = ''.join(f'<a href="{r}{u}">{n}</a>' for n, u in NAV[:5])
    volledig = f'{titel} · {NAAM}' if titel != NAAM else f'{NAAM} · {ROL}'
    og = f'<meta property="og:image" content="{r}{ogbeeld}">' if ogbeeld else ''
    doc = f'''<!doctype html>
<html lang="nl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(volledig)}</title>
<meta name="description" content="{E(beschrijving)}">
<meta property="og:title" content="{E(volledig)}">
<meta property="og:description" content="{E(beschrijving)}">
{og}
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter+Tight:ital,wght@0,300..600;1,300..500&family=IBM+Plex+Mono:wght@400;500&display=swap">
<link rel="stylesheet" href="{r}assets/site.css">
</head>
<body>
<a class="skip" href="#inhoud">Naar de inhoud</a>
<header class="kop">
  <a class="naam" href="{r}./">{NAAM}</a>
  <button class="menuknop" type="button" aria-expanded="false">Menu</button>
  <nav aria-label="Hoofdmenu">{nav}</nav>
</header>
<span class="hoek links meta">{ROL}</span>
<span class="hoek rechts"><a href="{r}contact/">Contact</a></span>
<main id="inhoud">
{body}
</main>
<footer class="voet">
  <div class="wrap raster">
    <div class="naam">{NAAM}</div>
    <nav aria-label="Voetmenu">{voetnav}</nav>
    <div class="contact"><a href="{r}contact/">Contact</a><span class="meta">E-mail en LinkedIn volgen</span></div>
    <div class="onder"><span class="meta">© 2026 {NAAM}</span><a class="meta" href="{r}styleguide.html">Stijlgids</a></div>
  </div>
</footer>
<script src="{r}assets/site.js"></script>
</body>
</html>
'''
    uit = os.path.join(ROOT, pad, 'index.html') if pad else os.path.join(ROOT, 'index.html')
    os.makedirs(os.path.dirname(uit), exist_ok=True)
    open(uit, 'w', encoding='utf-8').write(doc)


def paginakop(label, titel, intro=''):
    i = f'<p class="intro">{E(intro)}</p>' if intro else ''
    return f'<section class="wrap paginakop"><span class="meta">{E(label)}</span><h1>{E(titel)}</h1>{i}</section>'


def sectiekop(label, titel, intro=''):
    i = f'<p class="intro">{E(intro)}</p>' if intro else ''
    return f'<div class="raster sectie-kop"><span class="meta">{E(label)}</span><h2>{E(titel)}</h2>{i}</div>'


# ---------------------------------------------------------------- data voorbereiden

FILMS = DATA['film_uitgelicht']
FG = DATA['filmografie']
TEKST = DATA['tekst']
FILM_PER_TITEL = {f['titel']: f for f in FILMS}
# Volgorde van de uitgelichte films = volgorde in de filmografie (nieuwste eerst)
FILMS = [FILM_PER_TITEL[x['titel']] for x in FG if x['titel'] in FILM_PER_TITEL]
LIJSTBEELD = {x['titel']: x['beeld'] for x in FG}

for f in FILMS:
    f['img'] = beeld(f['beeld'], f'film/{f["slug"]}', 1600)
    f['img_s'] = beeld(LIJSTBEELD[f['titel']], f'film/{f["slug"]}-lijst', 900)
for x in FG:
    x['img'] = beeld(x['beeld'], f'filmografie/{x["nr"]:02d}', 480, 70)
for t in TEKST:
    t['img_kop'] = beeld(t['header'], f'tekst/{t["slug"]}', 2000)
    t['img_s'] = beeld(t['lijst'], f'tekst/{t["slug"]}-lijst', 900)
    if t.get('extra'):
        t['img_extra'] = beeld(t['extra'], f'tekst/{t["slug"]}-extra', 1400)


def jaar_van(meta):
    for deel in meta.split('·'):
        d = deel.strip()
        if d[:2] in ('19', '20'):
            return d.replace('HEDEN', 'heden')
    return ''


def soort_van(meta):
    return meta.split('·')[0].strip().capitalize()


# ---------------------------------------------------------------- kaarten

def filmkaart(f, r):
    duur = f.get('duur', '')
    still = f'<div class="still"><img src="{r}{f["img_s"]}" alt="" loading="lazy"></div>'
    return (f'<a class="kaart" href="{r}film/{f["slug"]}/">{still}'
            f'<span class="meta">Film · {E(f["jaar"])}{" · " + E(duur) if len(duur) < 14 else ""}</span>'
            f'<h3><span>{E(f["titel"])}</span></h3></a>')


def tekstkaart(t, r):
    still = f'<div class="still"><img src="{r}{t["img_s"]}" alt="" loading="lazy"></div>'
    return (f'<a class="kaart" href="{r}tekst/{t["slug"]}/">{still}'
            f'<span class="meta">{E(soort_van(t["meta"]))} · {E(jaar_van(t["meta"]))}</span>'
            f'<h3><span>{E(t["titel"])}</span></h3></a>')


def gesprekkaart(titel, soort, r):
    vlak = f'<div class="tekstvlak"><span class="meta">{E(soort)}</span><strong>{E(titel)}</strong></div>'
    return (f'<a class="kaart" href="{r}gesprek/">{vlak}'
            f'<span class="meta">Gesprek</span><h3><span>{E(titel)}</span></h3></a>')


def nieuwsrij(n, r):
    _, datum, titel, tekst, url = n
    return (f'<li><a class="rij" href="{r}{url}"><span class="meta">{datum}</span>'
            f'<span class="t">{E(titel)}<small>{E(tekst)}</small></span><span class="meta">→</span></a></li>')


# ---------------------------------------------------------------- pagina's

def home():
    r = ''
    loops = [
        {'src': video(FILM_PER_TITEL['ARK']['loop'], 'ark-loop'), 'poster': FILM_PER_TITEL['ARK']['img'],
         'titel': 'ARK (2023)', 'href': 'film/ark/'},
    ]
    lieb = next(f for f in FILMS if f['slug'] == 'leven-in-een-ballon')
    loops.append({'src': video(lieb['loop'], 'lieb-loop'), 'poster': lieb['img'],
                  'titel': 'Leven in een ballon (2022)', 'href': 'film/leven-in-een-ballon/'})
    loopdata = E(json.dumps(loops))
    disc = ''.join(
        f'<div class="discipline"><h2>{n}</h2><p>{E(t)}</p><a class="verder" href="{u}">{v}</a></div>'
        for n, u, t, v in DISCIPLINES)
    fs = {f['slug']: f for f in FILMS}
    ts = {t['slug']: t for t in TEKST}
    selectie = f'''
<div class="selectie">
  <div class="kolom"><span class="meta">Film</span>{filmkaart(fs['ark'], r)}{filmkaart(fs['leven-in-een-ballon'], r)}</div>
  <div class="kolom"><span class="meta">Tekst</span>{tekstkaart(ts['hier-wil-ik-wonen'], r)}{tekstkaart(ts['weg-met-de-soete'], r)}</div>
  <div class="kolom"><span class="meta">Gesprek</span>{gesprekkaart('RECAST', 'Moderatie lancering · 2025', r)}{gesprekkaart('BINST: UNTITLED', 'Podcast · zes afleveringen', r)}</div>
</div>'''
    body = f'''
<section class="wrap home-loop">
  <div class="kader"><span class="hk"></span>
    <video autoplay muted playsinline preload="auto" src="{loops[0]['src']}" poster="{loops[0]['poster']}" data-loops="{loopdata}" aria-label="Stille fragmenten uit de films"></video>
  </div>
  <div class="bijschrift"><span class="meta">Uit: <a class="loop-titel" href="{loops[0]['href']}">{loops[0]['titel']}</a></span><span class="meta">Film · Tekst · Gesprek</span></div>
</section>
<section class="wrap sectie home-intro raster">
  <h1>Ik maak films, schrijf teksten en voer gesprekken over kunst, vormgeving en architectuur.</h1>
  <p>Steeds op zoek naar de verhalen achter mensen, plekken en ideeën.</p>
</section>
{ticker(r)}
<section class="wrap sectie"><div class="drie">{disc}</div></section>
<section class="wrap sectie">{sectiekop('Geselecteerd werk', 'Twee per discipline')}{selectie}</section>
<section class="wrap sectie">{sectiekop('Nieuws', 'Premières en vertoningen')}<ul class="lijst">{''.join(nieuwsrij(n, r) for n in NIEUWS[:3])}</ul><p style="margin-top:24px"><a class="verder" href="nieuws/">Alle nieuws</a></p></section>
<section class="zand"><div class="wrap sectie raster sectie-kop" style="margin:0"><span class="meta">Contact</span><h2>Een film, een tekst of een gesprek in gedachten?</h2><p class="intro"><a class="verder" href="contact/">Neem contact op</a></p></div></section>
'''
    pagina('', NAAM, body, ogbeeld=FILM_PER_TITEL['ARK']['img'])


def film_index():
    r = '../'
    kaarten = ''.join(filmkaart(f, r) for f in FILMS)
    soorten = [('alles', 'Alles'), ('documentaire', 'Documentaires'), ('reeks', 'Reeksen'), ('expo', 'Expo en korte films')]
    knoppen = ''.join(f'<button class="label" type="button" data-filter="{k}" aria-pressed="{"true" if k == "alles" else "false"}">{n}</button>' for k, n in soorten)
    rijen = []
    for x in FG:
        if x['slug']:
            url, pijl, attr = f'{r}film/{x["slug"]}/', 'Lees meer →', ''
        elif x['link']:
            url, pijl, attr = x['link'], 'Extern ↗', ' target="_blank" rel="noopener"'
        else:
            url = None
        inner = (f'<div class="still"><img src="{r}{x["img"]}" alt="" loading="lazy"></div>'
                 f'<span class="meta jaar">{E(x["jaar"])}</span>'
                 f'<div><span class="t">{E(x["titel"])}</span><span class="meta soort">{E(x["meta"])}</span><p>{E(x["tekst"])}</p></div>')
        if url:
            rijen.append(f'<li><a class="fg-rij" data-soort="{x["soort"]}" href="{E(url)}"{attr}>{inner}<span class="pijl">{pijl}</span></a></li>')
        else:
            rijen.append(f'<li><div class="fg-rij" data-soort="{x["soort"]}">{inner}<span></span></div></li>')
    body = f'''
{paginakop('Film', 'Film', DISCIPLINES[0][2])}
<section class="wrap sectie">{sectiekop('Uitgelicht', f'{len(FILMS)} films')}<div class="raster-kaarten">{kaarten}</div></section>
<section class="wrap sectie" id="filmografie">
  {sectiekop('Filmografie', 'Alle producties', 'Documentaires, reeksen en korte films voor televisie, tentoonstellingen en opdrachtgevers.')}
  <div class="filter"><div class="labels" role="group" aria-label="Filter op soort">{knoppen}</div><span class="meta fg-teller">{len(FG)} producties</span></div>
  <ul class="lijst">{''.join(rijen)}</ul>
</section>'''
    pagina('film/', 'Film', body, 'Film', DISCIPLINES[0][2], FILMS[0]['img'])


KIJK = {'Kijklink': 'Bekijk de film', 'Bekijklink': 'Bekijk de film', 'VRT MAX': 'Bekijk op VRT MAX', 'Teaser': 'Bekijk de teaser'}


def film_detail(i, f):
    r = '../../'
    syn = f['synopsis']
    lopend = f'<p class="lead">{E(syn[0])}</p>' + ''.join(f'<p>{E(p)}</p>' for p in syn[1:])
    if f.get('pers'):
        lopend += f'<figure class="citaat"><blockquote>“{E(f["pers"][0])}”</blockquote><figcaption>{E(f["pers"][1])}</figcaption></figure>'
    kijk = [(KIJK[k], u) for k, u in f['links'] if k in KIJK]
    if f['slug'] == 'houses-for-the-common-good':
        kijk = [('Bekijk de films', u) for _, u in kijk]
    meer = [(k, u) for k, u in f['links'] if k not in KIJK]
    knoppen = ''.join(
        f'<a class="knop {"vol" if n == 0 else ""} extern" href="{E(u)}" target="_blank" rel="noopener">{E(t)}</a>'
        for n, (t, u) in enumerate(kijk))
    regie = next((v for k, v in f.get('credits', []) if 'regie' in k.lower()), '')
    slate = f'<dt>Jaar</dt><dd>{E(f["jaar"])}</dd><dt>Duur</dt><dd>{E(f["duur"])}</dd>'
    if regie:
        slate += f'<dt>Regie</dt><dd>{E(regie)}</dd>'
    aside = f'<dl class="slate">{slate}</dl>'
    if knoppen:
        aside += f'<div class="knoppen">{knoppen}</div>'
    blokken = ''
    if f.get('delen'):
        blokken += '<div class="blok"><span class="meta">De vijf films</span><dl class="credits">' + ''.join(
            f'<dt>{E(n)}</dt><dd>{E(d)}</dd>' for n, d in f['delen']) + '</dl></div>'
    if f.get('credits'):
        blokken += '<div class="blok"><span class="meta">Credits</span><dl class="credits">' + ''.join(
            f'<dt>{E(k)}</dt><dd>{E(v)}</dd>' for k, v in f['credits']) + '</dl></div>'
    if f.get('vertoningen'):
        blokken += '<div class="blok"><span class="meta">Vertoningen</span><ul class="simpel">' + ''.join(
            f'<li>{E(v)}</li>' for v in f['vertoningen']) + '</ul></div>'
    if meer:
        blokken += '<div class="blok"><span class="meta">Meer</span><ul class="simpel">' + ''.join(
            f'<li><a class="verder extern" href="{E(u)}" target="_blank" rel="noopener">{E(k)}</a></li>' for k, u in meer) + '</ul></div>'
    vierkant = f.get('vierkant')
    bijschrift = f'<figcaption class="meta">{E(f["beeldcredit"])}</figcaption>' if f.get('beeldcredit') else ''
    beeldhtml = kader(f'<img src="{r}{f["img"]}" alt="Still uit {E(f["titel"])}">{bijschrift}', 'detail-beeld' + (' vierkant' if vierkant else ''))
    alt = f'<p class="meta alt">{E(f["alt_titel"])}</p>' if f.get('alt_titel') else ''
    vorige, volgende = FILMS[i - 1], FILMS[(i + 1) % len(FILMS)]
    body = f'''
<article>
  <header class="wrap detail-kop"><span class="meta"><a href="{r}film/">Film</a> · {E(f["jaar"])}</span><h1>{E(f["titel"])}</h1>{alt}</header>
  <div class="wrap">{beeldhtml}</div>
  <div class="wrap detail-body raster">
    <aside>{aside}</aside>
    <div class="lopend">{lopend}<div style="display:grid;gap:36px;margin-top:48px">{blokken}</div></div>
  </div>
  <nav class="wrap buren" aria-label="Andere films">
    <a href="{r}film/{vorige['slug']}/"><span class="meta">← Vorige</span><span class="t"><span>{E(vorige['kort'])}</span></span></a>
    <a href="{r}film/{volgende['slug']}/"><span class="meta">Volgende →</span><span class="t"><span>{E(volgende['kort'])}</span></span></a>
  </nav>
</article>'''
    pagina(f'film/{f["slug"]}/', f['titel'], body, 'Film', syn[0][:180], f['img'])


def tekst_index():
    r = '../'
    body = f'''
{paginakop('Tekst', 'Tekst', DISCIPLINES[1][2])}
<section class="wrap sectie">{sectiekop('Uitgelicht', 'Publicaties en projecten')}<div class="raster-kaarten drie-kol">{''.join(tekstkaart(t, r) for t in TEKST)}</div></section>'''
    pagina('tekst/', 'Tekst', body, 'Tekst', DISCIPLINES[1][2], TEKST[0]['img_s'])


def tekst_detail(i, t):
    r = '../../'
    tekst = f'<p class="lead">{E(t["tekst"][0])}</p>' + ''.join(f'<p>{E(p)}</p>' for p in t['tekst'][1:])
    if t.get('img_extra'):
        staand = 'cover' in t['extra'].lower()
        tekst += kader(f'<img src="{r}{t["img_extra"]}" alt="" loading="lazy">', 'extra-beeld' + (' staand' if staand else ''))
    info = ''.join(f'<dt>{E(k)}</dt><dd>{E(v)}</dd>' for k, v in t['info'])
    aside = f'<dl class="slate">{info}</dl>'
    if t['links']:
        aside += '<div class="knoppen">' + ''.join(
            f'<a class="knop {"vol" if n == 0 else ""} extern" href="{E(u)}" target="_blank" rel="noopener">{E(k)}</a>' for n, (k, u) in enumerate(t['links'])) + '</div>'
    vorige, volgende = TEKST[i - 1], TEKST[(i + 1) % len(TEKST)]
    body = f'''
<article>
  <img class="volbreed" src="{r}{t["img_kop"]}" alt="">
  <header class="wrap detail-kop"><span class="meta"><a href="{r}tekst/">Tekst</a> · {E(t["meta"])}</span><h1>{E(t["titel"])}</h1></header>
  <div class="wrap detail-body raster" style="padding-top:0">
    <aside>{aside}</aside>
    <div class="lopend">{tekst}</div>
  </div>
  <nav class="wrap buren" aria-label="Andere teksten">
    <a href="{r}tekst/{vorige['slug']}/"><span class="meta">← Vorige</span><span class="t"><span>{E(vorige['titel'])}</span></span></a>
    <a href="{r}tekst/{volgende['slug']}/"><span class="meta">Volgende →</span><span class="t"><span>{E(volgende['titel'])}</span></span></a>
  </nav>
</article>'''
    pagina(f'tekst/{t["slug"]}/', t['titel'], body, 'Tekst', t['tekst'][0][:180], t['img_kop'])


def gesprek():
    def status(st):
        return f'<span class="label live">{E(st)}</span>' if st else '<span></span>'
    pods = ''.join(
        f'<li><div class="rij"><span class="meta">Podcast</span><span class="t">{E(n)}<small>{E(s)}{" · " + E(x) if x else ""}</small></span>'
        f'{status(st)}</div></li>'
        for n, s, x, st in PODCASTS)
    mods = ''.join(
        f'<li><div class="rij"><span class="meta">{j}</span><span class="t">{E(t)}<small>{E(c)}</small></span><span></span></div></li>'
        for j, t, c in MODERATIES)
    body = f'''
{paginakop('Gesprek', 'Gesprek', DISCIPLINES[2][2])}
<section class="wrap sectie">{sectiekop('Podcasts', 'Luisteren')}<ul class="lijst">{pods}</ul></section>
<section class="wrap sectie">{sectiekop('Moderaties', 'Panels en lanceringen')}<ul class="lijst">{mods}</ul></section>'''
    pagina('gesprek/', 'Gesprek', body, 'Gesprek', DISCIPLINES[2][2])


def nieuws():
    r = '../'
    body = f'''
{paginakop('Nieuws', 'Nieuws', 'Premières, vertoningen, publicaties en andere activiteiten.')}
<section class="wrap sectie" style="padding-top:0"><ul class="lijst">{''.join(nieuwsrij(n, r) for n in NIEUWS)}</ul></section>'''
    pagina('nieuws/', 'Nieuws', body, 'Nieuws')


def over():
    body = f'''
{paginakop('Over', NAAM)}
<section class="wrap sectie" style="padding-top:0">
  <div class="over-raster">
    <div class="portret"><span class="meta">Portret volgt</span></div>
    <div class="lopend">
      <figure class="citaat" style="margin-top:0"><blockquote>“{E(OVER_CITAAT[0])}”</blockquote><figcaption>{E(OVER_CITAAT[1])}</figcaption></figure>
      <p class="lead">{E(OVER[0])}</p>{''.join(f'<p>{E(p)}</p>' for p in OVER[1:])}
    </div>
  </div>
</section>
<section class="wrap sectie">{sectiekop('Opdrachtgevers en samenwerkingen', 'Met wie hij werkte')}<ul class="logolijst">{''.join(f'<li>{E(o)}</li>' for o in OPDRACHTGEVERS)}</ul></section>'''
    pagina('over/', 'Over', body, 'Over', OVER[3][:180])


def contact():
    body = f'''
{paginakop('Contact', 'Contact', 'Voor films, teksten, moderaties en podcasts.')}
<section class="wrap sectie" style="padding-top:0">
  <div class="drie">
    <div class="discipline"><span class="meta">E-mail</span><span class="contact-groot">Volgt</span></div>
    <div class="discipline"><span class="meta">Telefoon</span><span class="contact-groot">+32 …</span></div>
    <div class="discipline"><span class="meta">LinkedIn</span><span class="contact-groot">Volgt</span></div>
  </div>
</section>'''
    pagina('contact/', 'Contact', body, 'Contact')


if __name__ == '__main__':
    home()
    film_index()
    for i, f in enumerate(FILMS):
        film_detail(i, f)
    tekst_index()
    for i, t in enumerate(TEKST):
        tekst_detail(i, t)
    gesprek()
    nieuws()
    over()
    contact()
    print(f'Klaar: {len(FILMS)} films, {len(TEKST)} teksten, {len(FG)} producties in de filmografie.')
