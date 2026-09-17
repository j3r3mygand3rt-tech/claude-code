#!/usr/bin/env python3
"""
Erzeugt aus den Produktionsdateien Vorschaufassungen.

    python3 tools/build-vorschau.py            ->  vorschau/
    python3 tools/build-vorschau.py --hosting  ->  kundenvorschau/

vorschau/ ist fuer den eigenen Rechner gedacht und oeffnet sich per
Doppelklick, also ohne lokalen Webserver.

kundenvorschau/ ist fuer das Hochladen zu einem Hoster gedacht, etwa Netlify
Drop, damit die Kundschaft einen Link bekommt. Dieser Ordner ist zusaetzlich
gegen Suchmaschinen abgesichert: eine unveroeffentlichte Vorschau darf nicht
im Index landen, sonst konkurriert der Entwurf mit der echten Website um
dieselben Suchbegriffe.

Hintergrund zu den beiden Eingriffen fuer die Offline-Fassung:

  1. Ueber file:// behandelt der Browser jede Datei als eigenen Ursprung.
     Schriften unterliegen strengeren Regeln als Bilder und werden als
     Cross-Origin-Anfrage blockiert; die Seite faellt auf Systemschriften
     zurueck. Die woff2-Dateien werden deshalb als Base64 direkt in das
     Stylesheet geschrieben. Eine data:-URL ist keine Anfrage.
  2. Die <link rel="preload" as="font" crossorigin>-Zeilen werden entfernt.
     Sie fordern ausdruecklich eine Cross-Origin-Anfrage an und wuerden auch
     dann noch einen Konsolenfehler erzeugen, wenn die Schrift eingebettet ist.
  3. Das Symbol-Sprite wird in jede Seite hineingeschrieben. Ein
     <use href="sprite.svg#i-phone"> ist ueber file:// dieselbe verbotene
     Cross-Origin-Anfrage wie eine Schrift; ohne diesen Schritt fehlt in der
     Offline-Vorschau jedes Symbol. Auf einem Server bleibt das Sprite eine
     eigene Datei, die fuer alle zehn Seiten nur einmal geladen wird.

Dasselbe gilt fuer die sauberen Adressen: /preise setzt einen Server voraus,
der die Zuordnung vornimmt. Ueber file:// gibt es keinen, deshalb bekommen
die Verweise dort ihre .html-Endung zurueck.

Aufruf aus dem Projektordner medalife/.
"""
import base64
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

SEITEN = [
    "index.html",
    "physiotherapie.html",
    "training.html",
    "preise.html",
    "team.html",
    "faq.html",
    "kontakt.html",
    "impressum.html",
    "datenschutz.html",
    "barrierefreiheit.html",
]

# Die Slugs, die in der Produktionsfassung ohne Endung verlinkt sind.
SLUGS = [s[:-5] for s in SEITEN if s != "index.html"]


def schriften_einbetten(css: str, font_dir: Path) -> tuple[str, int]:
    """Ersetzt url('../fonts/x.woff2') durch eine data:-URL."""
    treffer = 0

    def ersetze(m: "re.Match[str]") -> str:
        nonlocal treffer
        name = m.group(1)
        pfad = font_dir / name
        if not pfad.exists():
            print(f"  WARNUNG: {name} nicht gefunden, bleibt als Verweis", file=sys.stderr)
            return m.group(0)
        roh = base64.b64encode(pfad.read_bytes()).decode("ascii")
        treffer += 1
        return f"url('data:font/woff2;base64,{roh}')"

    return re.sub(r"url\('\.\./fonts/([^']+)'\)", ersetze, css), treffer


def endungen_zurueck(html: str) -> tuple[str, int]:
    """Macht die sauberen Adressen wieder zu Dateinamen."""
    ersatz = [('href="./#', 'href="index.html#'), ('href="./"', 'href="index.html"')]
    for slug in SLUGS:
        ersatz.append((f'href="{slug}#', f'href="{slug}.html#'))
        ersatz.append((f'href="{slug}"', f'href="{slug}.html"'))
    n = 0
    for alt, neu in ersatz:
        n += html.count(alt)
        html = html.replace(alt, neu)
    return html, n


def preloads_entfernen(html: str) -> tuple[str, int]:
    """Entfernt die Schrift-Vorabrufe, die ueber file:// zwangsweise scheitern."""
    muster = r'[ \t]*<link rel="preload"[^>]*as="font"[^>]*>\n?'
    return re.sub(muster, "", html), len(re.findall(muster, html))


def sprite_einsetzen(html: str, sprite: str) -> tuple[str, int]:
    """Schreibt das Sprite in die Seite und kuerzt die Verweise darauf."""
    n = html.count('href="assets/icons/sprite.svg#')
    if not n:
        return html, 0
    html = html.replace('href="assets/icons/sprite.svg#', 'href="#')
    return html.replace("<body>", "<body>\n" + sprite.rstrip() + "\n", 1), n


def suchmaschinen_aussperren(html: str) -> str:
    """Setzt jede Seite auf noindex, unabhaengig von ihrem bisherigen Wert."""
    if re.search(r'<meta name="robots"[^>]*>', html):
        return re.sub(r'<meta name="robots"[^>]*>',
                      '<meta name="robots" content="noindex, nofollow">', html)
    return html.replace("</head>",
                        '<meta name="robots" content="noindex, nofollow">\n</head>', 1)


VORSPANN = """# ==========================================================================
# VORSCHAU, NICHT DIE LIVEFASSUNG
#
# Diese Datei ergaenzt die Produktionskonfiguration um zwei Dinge, die nur
# fuer eine unveroeffentlichte Vorschau gelten: Suchmaschinen werden
# ausgesperrt, und ein Passwortschutz liegt vorbereitet bei.
# ==========================================================================

# --------------------------------------------------------------------------
# Suchmaschinen aussperren
# Zusaetzlich zur robots.txt und zum noindex im <head>. Die Kopfzeile wirkt
# auch dann, wenn ein Crawler die robots.txt ignoriert.
# --------------------------------------------------------------------------
<IfModule mod_headers.c>
  Header set X-Robots-Tag "noindex, nofollow, noarchive"
</IfModule>

# --------------------------------------------------------------------------
# Passwortschutz, abgeschaltet
#
# Wer die Vorschau nur der Kundschaft zeigen will, schaltet die folgenden
# vier Zeilen frei. Vorher im Hoster-Panel unter "Passwortgeschuetzte
# Verzeichnisse" einen Zugang anlegen, oder eine .htpasswd hochladen und den
# absoluten Pfad unten eintragen. Ein relativer Pfad funktioniert nicht.
# --------------------------------------------------------------------------
# AuthType Basic
# AuthName "Vorschau MEDALIFE"
# AuthUserFile /home/BENUTZER/domains/IHRE-DOMAIN/.htpasswd
# Require valid-user

# ==========================================================================
# Ab hier unveraendert die Produktionskonfiguration
# ==========================================================================

"""


def main() -> int:
    hosting = "--hosting" in sys.argv
    out = ROOT / ("kundenvorschau" if hosting else "vorschau")

    if out.exists():
        shutil.rmtree(out)
    out.mkdir()

    shutil.copytree(ROOT / "assets" / "img", out / "assets" / "img")
    shutil.copytree(ROOT / "assets" / "icons", out / "assets" / "icons")
    (out / "assets" / "css").mkdir(parents=True)
    (out / "assets" / "js").mkdir()
    shutil.copy2(ROOT / "assets" / "js" / "main.js", out / "assets" / "js" / "main.js")

    css = (ROOT / "assets" / "css" / "style.css").read_text(encoding="utf-8")
    n_fonts = 0

    if hosting:
        # Auf einem echten Server werden die Schriften normal geladen und
        # zwischengespeichert. Base64 im Stylesheet waere hier ein Nachteil.
        shutil.copytree(ROOT / "assets" / "fonts", out / "assets" / "fonts")
    else:
        css, n_fonts = schriften_einbetten(css, ROOT / "assets" / "fonts")

    (out / "assets" / "css" / "style.css").write_text(css, encoding="utf-8")

    sprite = (ROOT / "assets" / "icons" / "sprite.svg").read_text(encoding="utf-8")

    n_links = 0
    n_pfade = 0
    n_symbole = 0
    for seite in SEITEN:
        html = (ROOT / seite).read_text(encoding="utf-8")
        if hosting:
            # Netlify und die beiliegende .htaccess loesen /preise selbst auf,
            # die Verweise bleiben also wie sie sind.
            html = suchmaschinen_aussperren(html)
        else:
            html, k = preloads_entfernen(html)
            html, p = endungen_zurueck(html)
            html, y = sprite_einsetzen(html, sprite)
            n_links += k
            n_pfade += p
            n_symbole += y
        (out / seite).write_text(html, encoding="utf-8")

    if hosting:
        (out / "robots.txt").write_text(
            "# Unveroeffentlichte Vorschau. Bitte nicht indexieren.\n"
            "User-agent: *\n"
            "Disallow: /\n", encoding="utf-8")

        # Netlify liest _headers, Apache und LiteSpeed lesen .htaccess.
        # Beide beilegen, damit derselbe Ordner auf beiden Wegen sicher ist.
        (out / "_headers").write_text(
            "/*\n  X-Robots-Tag: noindex, nofollow\n", encoding="utf-8")

        prod = ROOT / ".htaccess"
        (out / ".htaccess").write_text(
            VORSPANN + (prod.read_text(encoding="utf-8") if prod.exists() else ""),
            encoding="utf-8")
    else:
        shutil.copy2(ROOT / "robots.txt", out / "robots.txt")

    groesse = sum(f.stat().st_size for f in out.rglob("*") if f.is_file())
    print(f"Erzeugt in {out.name}/")
    if hosting:
        n_noindex = sum(
            1 for s in SEITEN
            if 'content="noindex, nofollow"' in (out / s).read_text(encoding="utf-8"))
        print(f"  {n_noindex} von {len(SEITEN)} Seiten auf noindex gesetzt")
        print("  robots.txt, _headers und .htaccess geschrieben")
        print(f"  Stylesheet: {len(css) // 1024} KB, Schriften separat")
    else:
        print(f"  {n_fonts} Schriften eingebettet")
        print(f"  {n_links} preload-Zeilen entfernt")
        print(f"  {n_pfade} Verweise auf Dateinamen zurueckgesetzt")
        print(f"  {n_symbole} Symbolverweise auf das eingesetzte Sprite umgestellt")
        print(f"  Stylesheet: {len(css) // 1024} KB")
    print(f"  Gesamt:     {groesse / 1024 / 1024:.1f} MB")
    if hosting:
        print("\nOrdner oder ZIP auf https://app.netlify.com/drop ziehen.")
    else:
        print("\nZum Ansehen: vorschau/index.html doppelklicken.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
