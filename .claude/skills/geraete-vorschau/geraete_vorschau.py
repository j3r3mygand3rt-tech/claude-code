#!/usr/bin/env python3
"""
Geräte-Vorschau: zeigt eine Website im iPhone-, Android-, Kleinhandy- und iPad-Rahmen,
mit Drehen und Neu laden. Die Seite läuft im Rahmen in echter Gerätebreite (iframe srcdoc),
dadurch greifen die Handy-Layouts der Website.

Aufruf:
  python3 geraete_vorschau.py <website/index.html> <ausgabe.html> [--titel "Name Handy-Vorschau"]

Lokale Stylesheets, Scripts, Bilder und Schriften werden eingebettet, damit die Vorschau
als einzelne Datei (z. B. als Artifact) funktioniert. Externe Adressen bleiben unverändert.
"""
import argparse, base64, json, mimetypes, os, re

def daten_uri(pfad):
    typ = mimetypes.guess_type(pfad)[0] or "application/octet-stream"
    if pfad.endswith(".woff2"): typ = "font/woff2"
    with open(pfad, "rb") as f:
        return "data:%s;base64,%s" % (typ, base64.b64encode(f.read()).decode())

def lokal(basis, url):
    if re.match(r"^(https?:|data:|mailto:|tel:|#|//)", url): return None
    p = os.path.normpath(os.path.join(basis, url.split("?")[0].split("#")[0]))
    return p if os.path.isfile(p) else None

def css_einbetten(css, basis):
    def ersetze(m):
        p = lokal(basis, m.group(2))
        return "url(%s%s%s)" % (m.group(1), daten_uri(p), m.group(1)) if p else m.group(0)
    return re.sub(r"url\((['\"]?)([^'\")]+)\1\)", ersetze, css)

def einbetten(html, basis):
    def stylesheet(m):
        href = re.search(r'href="([^"]+)"', m.group(0))
        p = lokal(basis, href.group(1)) if href else None
        if not p: return m.group(0)
        css = css_einbetten(open(p, encoding="utf-8").read(), os.path.dirname(p))
        return "<style>\n%s\n</style>" % css
    html = re.sub(r'<link[^>]+rel="stylesheet"[^>]*>', stylesheet, html)
    # Preloads und Manifest-Verweise auf lokale Dateien entfernen (in srcdoc ohne Nutzen)
    html = re.sub(r'<link[^>]+rel="(preload|manifest|apple-touch-icon)"[^>]*>\n?', "", html)
    def skript(m):
        p = lokal(basis, m.group(1))
        if not p: return m.group(0)
        return "<script>\n%s\n</script>" % open(p, encoding="utf-8").read().replace("</script", "<\\/script")
    html = re.sub(r'<script[^>]*src="([^"]+)"[^>]*></script>', skript, html)
    def bild(m):
        p = lokal(basis, m.group(2))
        return '%s="%s"' % (m.group(1), daten_uri(p)) if p else m.group(0)
    html = re.sub(r'(src|href)="([^"]+\.(?:png|jpe?g|gif|webp|svg|avif))"', bild, html)
    html = re.sub(r"<style>(.*?)</style>", lambda m: "<style>%s</style>" % css_einbetten(m.group(1), basis), html, flags=re.S)
    return html

VORLAGE = r"""<title>%TITEL%</title>
<meta name="description" content="%TITEL% im Handy- und Tablet-Rahmen">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Manrope:wght@500;600;700&display=swap">
<style>
:root {
  color-scheme: dark;
  --grund: #0b0f18;
  --flaeche: #141a26;
  --linie: #263043;
  --tinte: #e6edf5;
  --leise: #95a1b3;
  --akzent: #38bdf8;
  --rahmen: #1b1b1f;
}
* { box-sizing: border-box; }
html, body { height: 100%; }
body {
  margin: 0;
  background: var(--grund);
  color: var(--tinte);
  font-family: "Manrope", "Segoe UI", system-ui, sans-serif;
  padding-inline: 16px;
}
.buehne {
  min-height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 18px;
  padding-block: 20px 28px;
}
.leiste {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  align-items: center;
  gap: 8px;
}
.gruppe {
  display: inline-flex;
  padding: 4px;
  gap: 4px;
  background: var(--flaeche);
  border: 1px solid var(--linie);
  border-radius: 999px;
}
.gruppe button, .knopf {
  font: inherit;
  font-size: 0.88rem;
  font-weight: 600;
  min-height: 40px;
  padding: 0 16px;
  border-radius: 999px;
  border: 0;
  background: transparent;
  color: var(--leise);
  cursor: pointer;
}
.gruppe button[aria-pressed="true"] { background: var(--akzent); color: #06101f; }
.gruppe button:hover:not([aria-pressed="true"]), .knopf:hover { color: var(--tinte); }
.knopf {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: var(--flaeche);
  border: 1px solid var(--linie);
}
button:focus-visible { outline: 2px solid var(--akzent); outline-offset: 2px; }
.masse {
  font-size: 0.8rem;
  color: var(--leise);
  font-variant-numeric: tabular-nums;
}
.platz {
  flex: 1;
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: flex-start;
  min-height: 0;
}
.halter { position: relative; }
.geraet {
  position: absolute;
  top: 0;
  left: 0;
  transform-origin: top left;
  background: var(--rahmen);
  border-radius: 54px;
  padding: 14px;
  box-shadow:
    0 0 0 2px #3a3a42,
    0 0 0 5px #111114,
    0 30px 80px rgba(0, 0, 0, 0.55);
  transition: width .25s, height .25s;
}
.geraet--tablet { border-radius: 36px; padding: 22px; }
.bildschirm {
  position: relative;
  width: 100%;
  height: 100%;
  border-radius: 40px;
  overflow: hidden;
  background: #070b14;
}
.geraet--tablet .bildschirm { border-radius: 16px; }
.bildschirm iframe {
  display: block;
  border: 0;
  width: 100%;
  height: 100%;
  background: #070b14;
}
.hinweis {
  max-width: 60ch;
  text-align: center;
  font-size: 0.85rem;
  color: var(--leise);
  line-height: 1.55;
  margin: 0;
}
</style>

<div class="buehne">
  <div class="leiste">
    <div class="gruppe" role="group" aria-label="Gerät wählen">
      <button type="button" data-geraet="iphone" aria-pressed="true">iPhone</button>
      <button type="button" data-geraet="android" aria-pressed="false">Android</button>
      <button type="button" data-geraet="klein" aria-pressed="false">Kleines Handy</button>
      <button type="button" data-geraet="ipad" aria-pressed="false">iPad</button>
    </div>
    <button type="button" class="knopf" id="drehen" aria-label="Gerät drehen">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 12a9 9 0 0 1 15.5-6.2L21 8"/><path d="M21 3v5h-5"/><path d="M21 12a9 9 0 0 1-15.5 6.2L3 16"/><path d="M3 21v-5h5"/></svg>
      Drehen
    </button>
    <button type="button" class="knopf" id="neu">Neu laden</button>
  </div>
  <p class="masse" id="masse" aria-live="polite"></p>

  <div class="platz" id="platz">
    <div class="halter" id="halter">
      <div class="geraet" id="geraet">
        <div class="bildschirm">
          <iframe id="seite" title="Website-Vorschau"></iframe>
        </div>
      </div>
    </div>
  </div>

  <p class="hinweis">Die Website läuft im Rahmen in echter Gerätebreite, also mit Handy-Menü und Handy-Layout. Scrollen, Menü öffnen und Knöpfe antippen funktioniert wie auf dem Gerät. Formulare verschicken in der Vorschau nichts.</p>
</div>

<script>
(function () {
  "use strict";
  var SEITE = %SEITE%;

  var GERAETE = {
    iphone:  { name: "iPhone 14",        b: 390, h: 844,  tablet: false },
    android: { name: "Pixel 7",          b: 412, h: 915,  tablet: false },
    klein:   { name: "Kleines Handy",    b: 320, h: 640,  tablet: false },
    ipad:    { name: "iPad Mini",        b: 768, h: 1024, tablet: true }
  };

  var aktuell = "iphone";
  var quer = false;
  var geraet = document.getElementById("geraet");
  var halter = document.getElementById("halter");
  var platz = document.getElementById("platz");
  var rahmen = document.getElementById("seite");
  var masse = document.getElementById("masse");

  function laden() { rahmen.srcdoc = SEITE; }

  function anordnen() {
    var g = GERAETE[aktuell];
    var b = quer ? g.h : g.b;
    var h = quer ? g.b : g.h;
    var rand = g.tablet ? 22 : 14;
    var aussenB = b + rand * 2;
    var aussenH = h + rand * 2;

    geraet.className = "geraet" + (g.tablet ? " geraet--tablet" : "");
    geraet.style.width = aussenB + "px";
    geraet.style.height = aussenH + "px";

    // So verkleinern, dass das Gerät ganz in das Fenster passt
    var verfuegbarB = platz.clientWidth - 12;
    var verfuegbarH = window.innerHeight - platz.getBoundingClientRect().top - 90;
    var faktor = Math.min(1, verfuegbarB / aussenB, Math.max(verfuegbarH, 320) / aussenH);
    geraet.style.transform = "scale(" + faktor + ")";
    halter.style.width = aussenB * faktor + "px";
    halter.style.height = aussenH * faktor + "px";

    masse.textContent = g.name + (quer ? " quer" : " hochkant") + " · " + b + " × " + h + " px" +
      (faktor < 1 ? " · auf " + Math.round(faktor * 100) + " % verkleinert" : "");
  }

  document.querySelectorAll("[data-geraet]").forEach(function (knopf) {
    knopf.addEventListener("click", function () {
      aktuell = knopf.getAttribute("data-geraet");
      document.querySelectorAll("[data-geraet]").forEach(function (k) {
        k.setAttribute("aria-pressed", k === knopf ? "true" : "false");
      });
      anordnen();
    });
  });
  document.getElementById("drehen").addEventListener("click", function () { quer = !quer; anordnen(); });
  document.getElementById("neu").addEventListener("click", laden);
  window.addEventListener("resize", anordnen);

  anordnen();
  laden();
})();
</script>
"""

def main():
    a = argparse.ArgumentParser()
    a.add_argument("eingabe"); a.add_argument("ausgabe")
    a.add_argument("--titel", default="Handy-Vorschau")
    args = a.parse_args()
    html = open(args.eingabe, encoding="utf-8").read()
    if "<html" not in html.lower():
        html = '<!doctype html><html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"></head><body>%s</body></html>' % html
    html = einbetten(html, os.path.dirname(os.path.abspath(args.eingabe)))
    seite = json.dumps(html).replace("</", "<\\/")
    with open(args.ausgabe, "w", encoding="utf-8") as f:
        f.write(VORLAGE.replace("%TITEL%", args.titel).replace("%SEITE%", seite))
    print("Vorschau geschrieben:", args.ausgabe, "(%d KB)" % (os.path.getsize(args.ausgabe) // 1024))

if __name__ == "__main__":
    main()
