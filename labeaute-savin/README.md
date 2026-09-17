# La Beauté de Savin, Website-Relaunch

Neubau der Website des Kosmetikinstituts La Beauté de Savin, Brahmsallee 24, Hamburg.
Ersetzt die bestehende WordPress-Installation durch eine statische Seite ohne Build-Kette,
ohne Framework und ohne externe Abhängigkeiten.

---

## 1. Wettbewerbsvergleich

Verglichen wurden vier real erreichbare Seiten aus dem Umfeld: Malinka Hamburg,
Cosmetic Institut, SkinMed und Dr. Barbara Sturm. Geprüft wurde, welche Merkmale
dort vorhanden sind und bei uns fehlten.

| Merkmal | Wettbewerb | Umsetzung hier |
| --- | --- | --- |
| Anfahrt und Kontaktdaten gebündelt | 2 von 4 | Abschnitt „Anfahrt und Kontakt" mit Adresse, Karte, Zeiten, Sprachen |
| Technik und Markenbelege | 2 von 4 | Abschnitt „Womit wir arbeiten": HydraFacial, IONTO-COMED, eigene Pflegelinie |
| Häufige Fragen | 1 von 4 | Sechs Fragen, Antworten aus den bestehenden Inhalten |
| Eigene Produktlinie sichtbar | 2 von 4 | Als eigener Block im Institutsteil und in „Womit wir arbeiten" |
| Online-Buchung | 2 von 4 | Nicht umgesetzt, siehe Abschnitt 6 |
| Vorher und Nachher | 2 von 4 | Nicht umgesetzt, siehe Abschnitt 6 |
| Preisliste öffentlich | 0 von 4 | Vollständig, das ist hier ein Vorteil gegenüber allen vier |

Bemerkenswert: **keine** der vier Vergleichsseiten zeigt Preise offen. Die vollständige
Preisliste ist damit ein Unterscheidungsmerkmal und kein Nachteil.

---

## 2. Gestaltung

**Einordnung:** Redesign im Modus *Preserve*. Zielgruppe sind anspruchsvolle
Privatkundinnen und Privatkunden in Harvestehude und Eppendorf. Das Ziel der Seite
ist die Terminanfrage.

**Warum das Layout nicht nach Baukasten aussieht.** Die erste Fassung dieser Seite
arbeitete mit Karten, runden Ecken, weichen Schatten, Icon-Kreisen und Pillen-Buttons.
Das ist die Signatur, an der man generierte und geklickte Layouts sofort erkennt.
Diese Fassung verzichtet vollständig darauf:

| Statt | Hier |
| --- | --- |
| Kartenraster mit Icon-Kreisen | Behandlungsverzeichnis mit Führungspunkten, wie eine gedruckte Karte |
| Runde Ecken, weiche Schatten | Rechteckige Kanten, Ordnung über Haarlinien und Weißraum |
| Pillen-Buttons | Rechteckige Fläche, daneben ein unterstrichenes Wort als Nebenweg |
| Hakensymbole in Listen | Zeilen mit Haarlinie |
| Zentriertes Zitat mit Anführungsgrafik | Linksbündiges Zitat neben einem Bild |
| Bild in abgerundetem Rahmen | Bild bricht rechts aus dem Raster aus |
| Farbiges Akzentwort | Kursivsatz als Betonung |

**Schrift.** Bodoni Moda für Überschriften, Jost für Fließtext. Bodoni ist eine
klassizistische Antiqua mit starkem Strichkontrast, wie sie im Modejournalismus
seit zweihundert Jahren gesetzt wird. Sie wirkt in großen Graden, genau dort wird
sie eingesetzt. Jost geht auf die Futura zurück und bleibt in den Preiszeilen
auch klein lesbar. Beide Schriften werden selbst ausgeliefert.

**Farbe.** Die Markenfarben stammen unverändert aus der bestehenden Seite: Altrosa
`#c39391` und Taupe `#ac9f94`. Altrosa erreicht auf hellem Grund nur 2,66:1 und ist
als Textfarbe nicht barrierefrei. Es dient deshalb ausschließlich als Fläche oder
Linie. Für Text steht `#8f5a57` mit 5,57:1. Der Ton wird sparsam eingesetzt: die
Seite ist Tinte auf Papier, nicht rosa. Genau dieser Verzicht nimmt ihr den
Pastellton, an dem generierte Beauty-Layouts erkennbar sind.

**Bewegung.** Zurückhaltend. Inhalte fahren beim Erscheinen einmalig ein,
Zustandswechsel dauern 180 bis 320 ms. `prefers-reduced-motion` schaltet jede
Animation ab. Ohne JavaScript ist alles sofort sichtbar.

---

## 3. Aufbau

```
index.html          Startseite
leistungen.html     Alle Behandlungen mit Preisen
impressum.html      Impressum, Text von der bestehenden Seite übernommen
datenschutz.html    Datenschutzerklärung, Text übernommen, siehe Hinweis unten

assets/
  css/style.css     Ein Stylesheet, nach Abschnitten gegliedert
  js/main.js        Ein Skript, ohne Abhängigkeiten
  fonts/            5 woff2-Dateien, selbst gehostet
  img/              Originalbilder plus WebP-Varianten in 640/960/1280 px
  icons/sprite.svg  24 Symbole aus Phosphor Icons
```

Das Icon-Sprite ist zusätzlich in jede HTML-Datei eingebettet. Das spart einen
Ladevorgang und sorgt dafür, dass die Symbole auch ohne Webserver erscheinen.

**Zum Ansehen einen lokalen Server verwenden, nicht per Doppelklick öffnen.**
Über `file://` blockieren Browser das Laden der eigenen Schriftdateien aus
Sicherheitsgründen (CORS). Layout, Icons, Bilder und Skript funktionieren dann
zwar, die Seite fällt aber auf Systemschriften zurück und sieht falsch aus.
Ein Server genügt:

```bash
cd labeaute-savin
python3 -m http.server 8000
```

**Vorschaufassung ohne Server.** Wer die Seite ohne Terminal zeigen will, baut
sich eine Fassung, in der die Schriften als Base64 im Stylesheet stecken:

```bash
python3 tools/build-vorschau.py
```

Das erzeugt den Ordner `vorschau/`, dessen `index.html` sich per Doppelklick
öffnen lässt. Die Produktionsdateien bleiben unverändert. Der Ordner ist
Wegwerfware und gehört nicht ins Repository, entsprechend steht er in der
`.gitignore`. Für den Livegang immer die Dateien im Hauptordner verwenden:
dort werden die Schriften separat geladen und vom Browser zwischengespeichert,
statt bei jedem Seitenaufruf im 258 KB grossen Stylesheet mitzureisen.

Kopf- und Fußzeile sind in allen vier Dateien identisch. Bei vier Seiten ist das
tragbar. Wer sie ändert, ändert sie in allen vier Dateien.

---

## 4. Weg zur Terminanfrage

| Bereich | Mobil | Desktop |
| --- | --- | --- |
| Kontaktleiste oben | ausgeblendet | Adresse, Öffnungszeiten, E-Mail, Telefon |
| Kopfzeile, mitlaufend | Button „Termin" | Telefonnummer und Button „Termin" |
| Leiste unten | ab 420 px Scrolltiefe: Anrufen und Termin anfragen | nicht nötig |
| Im Inhalt | Hero, Preisseite, Kontaktabschnitt | ebenso |
| Fußzeile | Telefon, Mobil, E-Mail | ebenso |

---

## 5. Inhalte

Alle Texte, Leistungen, Preise und Kontaktdaten stammen von der bestehenden Website.
Sprachlich überarbeitet, inhaltlich unverändert. Die Antworten im Fragenteil,
einschließlich der Gegenanzeigen für Mikrodermabrasion und Ultraschall, sind wörtlich
aus den dortigen Behandlungsseiten übernommen.

**Korrektur gegenüber der ersten Fassung:** Im Hero stand zunächst „Zwei Gehminuten
von der Hoheluftbrücke". Diese Angabe war nicht belegt, sie steht nirgends auf der
bestehenden Website und wurde beim Schreiben erfunden. Sie ist entfernt. Auf der
Seite steht jetzt nur, was überprüfbar ist.

**Bilder:** Alle 15 Bilder stammen im Original von der bestehenden Seite. Sie wurden
nicht ersetzt und nicht beschnitten. Zusätzlich liegt jedes als WebP in drei Breiten
vor, die über `srcset` passend zum Gerät ausgeliefert werden. Das JPEG bleibt als
Rückfallebene erhalten.

---

## 6. Gemessene Ergebnisse

Gemessen in Chromium, erster Aufruf ohne Cache, lokaler Server.

| | Bestehende Seite | Erste Fassung | Diese Fassung |
| --- | --- | --- | --- |
| HTML-Dokument | 147,7 KB | 49,8 KB | 47,8 KB |
| CSS-Dateien | 12 | 1 | 1 |
| JS-Dateien | 19 | 1 | 1 |
| Anfragen mobil | mindestens 40 | 12 | **9** |
| Übertragen mobil | nicht gemessen | 307 KB | **188 KB** |
| First Contentful Paint | nicht gemessen | 148 ms | **120 ms** |

Die bestehende Seite wurde aus dem ausgelieferten HTML gezählt, nicht im Browser
gemessen: Chromium in dieser Umgebung vertraut dem Proxy-Zertifikat nicht, und die
TLS-Prüfung abzuschalten wäre der falsche Weg für eine Zahl.

**Geprüft und bestanden:**

- axe-core, WCAG 2.0/2.1 Stufe A und AA plus Best Practices: **0 Verstöße** auf allen
  vier Seiten, jeweils bei 390 px und 1440 px.
- Kein horizontales Scrollen bei 320, 360, 390, 414, 600, 768, 1024, 1440 und 1920 px.
- Keine Konsolenfehler, keine fehlgeschlagenen Anfragen, alle Bilder als WebP.
- `web-quality-audit`: 0 Fehler. Die fünf Warnungen sind Fehlalarme: vier betreffen den
  SVG-Namespace `http://www.w3.org/2000/svg`, die fünfte ein Zitat im Datenschutztext,
  das die Umstellung von „http://" auf „https://" erklärt.
- Funktionstest: Menü öffnet und schließt, Escape schließt, Hintergrund wird gesperrt
  und wieder freigegeben. Das Fragen-Akkordeon öffnet und schließt. Formularvalidierung
  meldet leere Pflichtfelder und ungültige E-Mail-Adressen und setzt den Fokus auf das
  erste fehlerhafte Feld. Die Navigationsmarkierung folgt dem sichtbaren Abschnitt und
  verschwindet, sobald man wieder ganz oben steht.

---

## 7. Offen für den Betreiber

1. **Kontaktformular.** Ohne Konfiguration öffnet das Formular eine vorbereitete
   E-Mail im Mailprogramm. Für Serverversand das Ziel eintragen:
   ```html
   <form data-contact-form data-endpoint="https://ihr-endpunkt">
   ```

2. **Anfahrt.** Der Abschnitt nennt Adresse, Karte, Zeiten und Sprachen. Angaben zu
   Haltestellen und Parkmöglichkeiten fehlen bewusst: Sie stehen nicht auf der
   bisherigen Website. Ein Kommentar im HTML markiert die Stelle.

3. **Online-Buchung.** Zwei der vier Vergleichsseiten buchen über Treatwell
   beziehungsweise ein eigenes System. Das lohnt sich nur mit echtem Kalender im
   Hintergrund. Sobald einer besteht, ersetzt sein Link die „Termin"-Schaltflächen.

4. **Vorher und Nachher.** Zwei der vier zeigen Behandlungsergebnisse. Das ist der
   stärkste Vertrauensbeleg in dieser Branche. Es fehlt hier, weil es keine echten
   Aufnahmen gibt und erfundene Bilder ausgeschlossen sind. Sobald Fotos mit
   Einwilligung der Kundinnen vorliegen, passen sie in den Galerieabschnitt.

5. **Datenschutzerklärung.** Text unverändert übernommen, die technische Grundlage hat
   sich aber geändert: kein WordPress, keine externen Schriften, kein eingebettetes
   YouTube, keine eingebettete Karte. Bitte juristisch prüfen lassen.

6. **Instagram-Adresse.** Im Fußbereich steht `https://www.instagram.com/` ohne
   Profilnamen, weil die bestehende Seite den Link über ein Skript aufbaut.

---

## 8. Betrieb

Die Seite ist statisch. Es genügt, den Ordner auf einen Webserver zu legen, es gibt
keinen Build-Schritt und keine Datenbank. Geeignet sind jeder klassische Webspace,
Netlify, Vercel oder GitHub Pages.

Empfohlene Servereinstellungen: Auslieferung über HTTPS, Komprimierung mit gzip oder
brotli für `.html`, `.css`, `.js` und `.svg`, lange Cache-Dauer für `assets/fonts` und
`assets/img`.

Lokal ansehen:

```bash
python3 -m http.server 8000
```
