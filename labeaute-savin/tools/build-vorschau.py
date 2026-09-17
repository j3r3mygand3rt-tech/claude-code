#!/usr/bin/env python3
"""
Erzeugt aus den Produktionsdateien Vorschaufassungen.

    python3 tools/build-vorschau.py            ->  vorschau/
    python3 tools/build-vorschau.py --hosting  ->  kundenvorschau/

vorschau/ ist fuer den eigenen Rechner gedacht und oeffnet sich per
Doppelklick, also ohne lokalen Webserver.

kundenvorschau/ ist fuer das Hochladen zu einem Hoster gedacht, etwa Netlify
Drop, damit die Kundin einen Link bekommt. Dieser Ordner ist zusaetzlich
gegen Suchmaschinen abgesichert: eine unveroeffentlichte Vorschau darf nicht
im Index landen, sonst konkurriert der Entwurf mit der echten Website der
Kundin um dieselben Suchbegriffe.

Hintergrund: Ueber das Protokoll file:// behandelt der Browser jede Datei als
eigenen Ursprung. Schriften unterliegen strengeren Regeln als Bilder und
werden deshalb als Cross-Origin-Anfrage blockiert. Die Seite faellt dann auf
Systemschriften zurueck.

Zwei Eingriffe loesen das:
  1. Die woff2-Dateien werden als Base64 direkt in das Stylesheet geschrieben.
     Eine data:-URL ist keine Anfrage und wird nicht blockiert.
  2. Die <link rel="preload" as="font" crossorigin>-Zeilen werden entfernt.
     Sie fordern ausdruecklich eine Cross-Origin-Anfrage an und wuerden auch
     dann noch einen Fehler in der Konsole erzeugen, wenn die Schrift bereits
     eingebettet ist.

Die Produktionsdateien bleiben unveraendert. Aufruf aus dem Projektordner:

    python3 tools/build-vorschau.py
"""
import base64
import mimetypes
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "vorschau"
SEITEN = ["index.html", "leistungen.html", "impressum.html", "datenschutz.html"]


def schriften_einbetten(css: str, font_dir: Path) -> tuple[str, int]:
    """Ersetzt url('../fonts/x.woff2') durch eine data:-URL."""
    treffer = 0

    def ersetze(m: re.Match) -> str:
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


def preloads_entfernen(html: str) -> tuple[str, int]:
    """Entfernt die Schrift-Vorabrufe, die ueber file:// zwangsweise scheitern."""
    muster = r'[ \t]*<link rel="preload"[^>]*as="font"[^>]*>\n?'
    return re.sub(muster, "", html), len(re.findall(muster, html))


def suchmaschinen_aussperren(html: str) -> str:
    """Setzt jede Seite auf noindex, unabhaengig von ihrem bisherigen Wert."""
    if re.search(r'<meta name="robots"[^>]*>', html):
        return re.sub(r'<meta name="robots"[^>]*>',
                      '<meta name="robots" content="noindex, nofollow">', html)
    return html.replace('</head>',
                        '<meta name="robots" content="noindex, nofollow">\n</head>', 1)


def main() -> int:
    hosting = "--hosting" in sys.argv
    out = ROOT / ("kundenvorschau" if hosting else "vorschau")

    global OUT
    OUT = out

    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()

    shutil.copytree(ROOT / "assets" / "img", OUT / "assets" / "img")
    shutil.copytree(ROOT / "assets" / "icons", OUT / "assets" / "icons")
    (OUT / "assets" / "css").mkdir(parents=True)
    (OUT / "assets" / "js").mkdir()
    shutil.copy2(ROOT / "assets" / "js" / "main.js", OUT / "assets" / "js" / "main.js")

    css = (ROOT / "assets" / "css" / "style.css").read_text(encoding="utf-8")
    n_fonts = 0

    if hosting:
        # Auf einem echten Server werden die Schriften normal geladen und
        # zwischengespeichert. Base64 im Stylesheet waere hier ein Nachteil.
        shutil.copytree(ROOT / "assets" / "fonts", OUT / "assets" / "fonts")
    else:
        css, n_fonts = schriften_einbetten(css, ROOT / "assets" / "fonts")

    (OUT / "assets" / "css" / "style.css").write_text(css, encoding="utf-8")

    n_links = 0
    for seite in SEITEN:
        html = (ROOT / seite).read_text(encoding="utf-8")
        if hosting:
            html = suchmaschinen_aussperren(html)
        else:
            html, k = preloads_entfernen(html)
            n_links += k
        (OUT / seite).write_text(html, encoding="utf-8")

    if hosting:
        (OUT / "robots.txt").write_text(
            "# Unveroeffentlichte Vorschau. Bitte nicht indexieren.\n"
            "User-agent: *\n"
            "Disallow: /\n", encoding="utf-8")

        # Netlify liest _headers, Apache und LiteSpeed lesen .htaccess.
        # Beide beilegen, damit derselbe Ordner auf beiden Wegen sicher ist.
        (OUT / "_headers").write_text(
            "/*\n  X-Robots-Tag: noindex, nofollow\n", encoding="utf-8")

        vorspann = """# ==========================================================================
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
# Wer die Vorschau nur der Kundin zeigen will, schaltet die folgenden vier
# Zeilen frei. Vorher im Hostinger-Panel unter "Passwortgeschuetzte
# Verzeichnisse" einen Zugang anlegen, oder eine .htpasswd hochladen und
# den absoluten Pfad unten eintragen. Ein relativer Pfad funktioniert nicht.
# --------------------------------------------------------------------------
# AuthType Basic
# AuthName "Vorschau La Beaute de Savin"
# AuthUserFile /home/BENUTZER/domains/IHRE-DOMAIN/.htpasswd
# Require valid-user

# ==========================================================================
# Ab hier unveraendert die Produktionskonfiguration
# ==========================================================================

"""
        prod = (ROOT / ".htaccess")
        if prod.exists():
            (OUT / ".htaccess").write_text(
                vorspann + prod.read_text(encoding="utf-8"), encoding="utf-8")
        else:
            (OUT / ".htaccess").write_text(vorspann, encoding="utf-8")

    groesse = sum(f.stat().st_size for f in OUT.rglob("*") if f.is_file())
    print(f"Erzeugt in {OUT.name}/")
    if hosting:
        n_noindex = sum(
            1 for s2 in SEITEN
            if 'content="noindex, nofollow"' in (OUT / s2).read_text(encoding="utf-8"))
        print(f"  {n_noindex} von {len(SEITEN)} Seiten auf noindex gesetzt")
        print("  robots.txt, _headers und .htaccess geschrieben")
        print(f"  Stylesheet: {len(css) // 1024} KB, Schriften separat")
    else:
        print(f"  {n_fonts} Schriften eingebettet")
        print(f"  {n_links} preload-Zeilen entfernt")
        print(f"  Stylesheet: {len(css) // 1024} KB")
    print(f"  Gesamt:     {groesse / 1024 / 1024:.1f} MB")
    if hosting:
        print("\nOrdner oder ZIP auf https://app.netlify.com/drop ziehen.")
    else:
        print("\nZum Ansehen: vorschau/index.html doppelklicken.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
