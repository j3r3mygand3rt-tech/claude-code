#!/usr/bin/env python3
"""Prueft eine statische Website in einem Durchgang.

    python3 pruefen.py http://localhost:8000
    python3 pruefen.py http://localhost:8000 --geraete
    python3 pruefen.py http://localhost:8000 --quelle ./mein-projekt

Findet die Seiten selbst, indem es den internen Verweisen folgt, und
prueft je Seite:

  * axe-core, WCAG 2.0 und 2.1 Stufe A und AA plus Best Practices
  * horizontales Scrollen ueber die ueblichen Breiten
  * Konsolenfehler und fehlgeschlagene Anfragen
  * ob jedes Bild tatsaechlich laedt, nach vollstaendigem Durchscrollen
  * Trefferflaechen unter 44 px, ohne Verweise mitten im Satz
  * Geviert- und Halbgeviertstriche im Quelltext, falls --quelle gesetzt

Rueckgabewert 0, wenn nichts gefunden wurde, sonst 1. Damit laesst sich
das Skript auch in eine Pruefkette haengen.

Voraussetzung: playwright und eine Chromium-Installation.
    pip install playwright && playwright install chromium
"""
from __future__ import annotations

import argparse
import glob
import os
import re
import sys
import urllib.parse
import urllib.request

BREITEN = [320, 360, 390, 414, 600, 768, 1024, 1280, 1440, 1920]
AXE_BREITEN = [(390, 844), (1440, 900)]
GERAETE = ["iPhone SE", "iPhone 12", "iPhone 14 Pro Max", "Pixel 7",
           "iPad Mini", "iPad (gen 7)", "iPad Pro 11"]
AXE_CDN = "https://cdn.jsdelivr.net/npm/axe-core@4/axe.min.js"

AXE_LAUF = (
    "async()=>(await axe.run(document,{runOnly:{type:'tag',values:"
    "['wcag2a','wcag2aa','wcag21a','wcag21aa','best-practice']}})).violations"
)
KEIN_UEBERLAUF = "()=>document.documentElement.scrollWidth<=window.innerWidth+1"
ALLE_BILDER = "()=>[...document.images].every(i=>i.complete&&i.naturalWidth>0)"
DURCHSCROLLEN = """async()=>{
  const schritt = 350;
  for (let y = 0; y <= document.documentElement.scrollHeight; y += schritt) {
    window.scrollTo(0, y);
    await new Promise(r => setTimeout(r, 80));
  }
  window.scrollTo(0, 0);
}"""

# Zwei Ausnahmen, die WCAG 2.5.8 ausdruecklich vorsieht und die sonst als
# Rauschen jeden Lauf fuellen:
#
#   1. Verweise mitten im Fliesstext. Ein aufgeblasenes Inline-Ziel wuerde
#      den Zeilenabstand zerreissen.
#   2. Ein Eingabefeld, das in einem <label> steckt. Getroffen wird das
#      Label, nicht das 18px kleine Kaestchen. Gemessen wird deshalb die
#      Flaeche des Labels.
#
# Beruecksichtigt wird ausserdem die Abstandsregel: ein Ziel, um das
# herum genug unberuehrter Platz liegt, gilt als gross genug.
KLEINE_ZIELE = """()=>{
  const textbehaelter = '.legal,.prose,p,li,dd';
  const treffer = [];
  document.querySelectorAll('a,button,input,select,textarea,summary').forEach(el=>{
    let ziel = el;
    if (el.tagName === 'INPUT' && el.closest('label')) ziel = el.closest('label');

    const r = ziel.getBoundingClientRect();
    const cs = getComputedStyle(el);
    if (!r.width || !r.height || cs.display === 'none' || cs.visibility === 'hidden') return;
    if (el.tagName === 'A' && el.closest(textbehaelter)) return;
    if (r.height >= 44 && r.width >= 24) return;

    // Abstandsregel: senkrecht mindestens 24px ungestoerter Raum
    const eltern = ziel.parentElement;
    if (eltern) {
      const pr = eltern.getBoundingClientRect();
      const luft = Math.min(r.top - pr.top, pr.bottom - r.bottom);
      if (r.height + 2 * Math.max(0, luft) >= 24 && r.height >= 20) return;
    }

    treffer.push({
      text: (el.textContent || el.type || el.tagName).trim().slice(0, 30),
      h: Math.round(r.height), w: Math.round(r.width)
    });
  });
  return treffer;
}"""


def axe_holen() -> str:
    lokal = os.path.join(os.path.dirname(__file__), "axe.min.js")
    if os.path.exists(lokal):
        return open(lokal, encoding="utf-8").read()
    with urllib.request.urlopen(AXE_CDN, timeout=60) as r:
        text = r.read().decode("utf-8")
    try:
        open(lokal, "w", encoding="utf-8").write(text)
    except OSError:
        pass
    return text


def seiten_finden(pg, basis: str) -> list[str]:
    """Folgt den internen Verweisen ab der Startseite, eine Ebene tief."""
    gefunden = {basis.rstrip("/") + "/"}
    warteschlange = [basis.rstrip("/") + "/"]
    while warteschlange:
        u = warteschlange.pop()
        try:
            pg.goto(u, wait_until="networkidle", timeout=30000)
        except Exception:
            continue
        for h in pg.eval_on_selector_all("a[href]", "e=>e.map(x=>x.getAttribute('href'))"):
            if not h or h.startswith(("#", "mailto:", "tel:", "javascript:")):
                continue
            ziel = urllib.parse.urljoin(u, h.split("#")[0])
            if not ziel.startswith(basis.rstrip("/")):
                continue
            if any(ziel.endswith(e) for e in (".pdf", ".zip", ".jpg", ".png", ".webp")):
                continue
            if ziel not in gefunden:
                gefunden.add(ziel)
                warteschlange.append(ziel)
    return sorted(gefunden)


def striche_pruefen(ordner: str) -> list[str]:
    """Geviert- und Halbgeviertstriche im sichtbaren Text finden."""
    treffer = []
    for pfad in glob.glob(os.path.join(ordner, "**", "*.html"), recursive=True):
        if os.sep + "vorschau" in pfad or os.sep + "kundenvorschau" in pfad:
            continue
        for nr, zeile in enumerate(open(pfad, encoding="utf-8"), 1):
            if "—" in zeile or "–" in zeile:
                treffer.append(f"{os.path.relpath(pfad, ordner)}:{nr}")
    return treffer


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("basis", help="Adresse des laufenden Servers")
    ap.add_argument("--geraete", action="store_true",
                    help="zusaetzlich sieben Geraeteprofile in beiden Lagen")
    ap.add_argument("--quelle", help="Projektordner, fuer die Strichpruefung")
    ap.add_argument("--chromium", default="/opt/pw-browsers/chromium-1194/chrome-linux/chrome")
    args = ap.parse_args()

    from playwright.sync_api import sync_playwright

    axe = axe_holen()
    maengel: list[str] = []

    with sync_playwright() as p:
        start = {"args": ["--no-sandbox"]}
        if os.path.exists(args.chromium):
            start["executable_path"] = args.chromium
        b = p.chromium.launch(**start)

        ctx = b.new_context(viewport={"width": 1440, "height": 900})
        seiten = seiten_finden(ctx.new_page(), args.basis)
        ctx.close()
        print(f"{len(seiten)} Seiten gefunden")
        for s in seiten:
            print("   ", s)

        print("\nBarrierefreiheit, Bilder, Trefferflaechen")
        for seite in seiten:
            for w, h in AXE_BREITEN:
                ctx = b.new_context(viewport={"width": w, "height": h})
                pg = ctx.new_page()
                fehler, gescheitert = [], []
                pg.on("console", lambda m: fehler.append(m.text) if m.type == "error" else None)
                pg.on("requestfailed", lambda r: gescheitert.append(r.url))
                pg.goto(seite, wait_until="networkidle")
                pg.add_style_tag(content="html{scroll-behavior:auto !important}")
                pg.evaluate(DURCHSCROLLEN)
                kurz = seite.replace(args.basis, "") or "/"

                try:
                    pg.wait_for_function(ALLE_BILDER, timeout=25000)
                except Exception:
                    offen = pg.evaluate(
                        "()=>[...document.images].filter(i=>!i.complete||!i.naturalWidth)"
                        ".map(i=>(i.currentSrc||i.src).split('/').pop())")
                    maengel.append(f"Bild laedt nicht: {kurz} {w}px {offen}")

                pg.add_script_tag(content=axe)
                for v in pg.evaluate(AXE_LAUF):
                    maengel.append(f"axe {v['impact']}: {kurz} {w}px {v['id']}")

                for z in pg.evaluate(KLEINE_ZIELE):
                    maengel.append(
                        f"Trefferflaeche {z['w']}x{z['h']}px: {kurz} {w}px \"{z['text']}\"")

                for f in sorted(set(fehler)):
                    maengel.append(f"Konsole: {kurz} {w}px {f}")
                for f in sorted(set(gescheitert)):
                    maengel.append(f"Anfrage gescheitert: {kurz} {w}px {f}")
                ctx.close()
            print(f"    {seite.replace(args.basis, '') or '/'} geprueft")

        print("\nHorizontales Scrollen")
        for seite in seiten:
            schlecht = []
            for w in BREITEN:
                ctx = b.new_context(viewport={"width": w, "height": 800})
                pg = ctx.new_page()
                pg.goto(seite, wait_until="networkidle")
                if not pg.evaluate(KEIN_UEBERLAUF):
                    breite = pg.evaluate("()=>document.documentElement.scrollWidth")
                    schlecht.append(f"{w}px (Dokument {breite}px)")
                ctx.close()
            kurz = seite.replace(args.basis, "") or "/"
            if schlecht:
                maengel.append(f"Querscroll: {kurz} bei {', '.join(schlecht)}")
            print(f"    {kurz:<24}{'ok' if not schlecht else 'FEHLER'}")

        if args.geraete:
            print("\nGeraeteprofile")
            for name in GERAETE:
                dev = p.devices[name]
                for lage in ("hoch", "quer"):
                    vp = dict(dev["viewport"]) if lage == "hoch" else {
                        "width": dev["viewport"]["height"],
                        "height": dev["viewport"]["width"]}
                    ctx = b.new_context(**{**dev, "viewport": vp})
                    for seite in seiten:
                        pg = ctx.new_page()
                        pg.goto(seite, wait_until="networkidle")
                        if not pg.evaluate(KEIN_UEBERLAUF):
                            maengel.append(f"Querscroll: {name} {lage} {seite}")
                        pg.close()
                    ctx.close()
                print(f"    {name} geprueft")

        b.close()

    if args.quelle:
        print("\nStriche im Quelltext")
        striche = striche_pruefen(args.quelle)
        for t in striche:
            maengel.append(f"Geviertstrich: {t}")
        print(f"    {len(striche)} Fundstellen")

    print("\n" + "=" * 60)
    if not maengel:
        print("Keine Maengel gefunden.")
        return 0
    print(f"{len(maengel)} Maengel:")
    for m in maengel:
        print(f"  {m}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
