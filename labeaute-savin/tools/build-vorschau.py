#!/usr/bin/env python3
"""
Erzeugt aus den Produktionsdateien eine Vorschaufassung, die sich per
Doppelklick oeffnen laesst, also ohne lokalen Webserver.

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


def main() -> int:
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()

    # Bilder und Symbole unveraendert uebernehmen, Schriften werden nicht mehr gebraucht
    shutil.copytree(ROOT / "assets" / "img", OUT / "assets" / "img")
    shutil.copytree(ROOT / "assets" / "icons", OUT / "assets" / "icons")
    (OUT / "assets" / "css").mkdir(parents=True)

    css = (ROOT / "assets" / "css" / "style.css").read_text(encoding="utf-8")
    css, n_fonts = schriften_einbetten(css, ROOT / "assets" / "fonts")
    (OUT / "assets" / "css" / "style.css").write_text(css, encoding="utf-8")

    (OUT / "assets" / "js").mkdir()
    shutil.copy2(ROOT / "assets" / "js" / "main.js", OUT / "assets" / "js" / "main.js")

    n_links = 0
    for seite in SEITEN:
        html = (ROOT / seite).read_text(encoding="utf-8")
        html, k = preloads_entfernen(html)
        n_links += k
        (OUT / seite).write_text(html, encoding="utf-8")

    groesse = sum(f.stat().st_size for f in OUT.rglob("*") if f.is_file())
    print(f"Vorschau erzeugt in {OUT}")
    print(f"  {n_fonts} Schriften eingebettet")
    print(f"  {n_links} preload-Zeilen entfernt")
    print(f"  Stylesheet: {len(css) // 1024} KB")
    print(f"  Gesamt:     {groesse / 1024 / 1024:.1f} MB")
    print("\nZum Ansehen: vorschau/index.html doppelklicken.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
