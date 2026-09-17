---
name: website-redesign
description: Redesign an existing website from its live URL. Use when asked to rebuild, relaunch or modernise a site that already exists, especially a small business site. Covers the order of work that avoids rewriting the design twice, the extraction pass that catches every asset, one verification run instead of many, and a preview the client can open.
---

# Website-Redesign

Ein bestehende Seite neu bauen. Die Reihenfolge unten ist nicht Geschmack,
sie stammt aus einem Projekt, das neun Commits gebraucht hat, wo vier
gereicht hätten. Jede Regel benennt den Fehler, den sie verhindert.

## Die drei Fragen, vor der ersten Zeile Code

Sie kosten eine Minute und sparen einen kompletten Neubau. Stelle sie
zusammen, nicht nacheinander, und warte die Antwort ab.

1. **Gestaltungsrichtung.** Zwei bis drei benannte Richtungen zur Auswahl
   stellen, keine offene Frage. Etwa: redaktionell und typografisch,
   ruhig und bildgeführt, oder nah am Bestand modernisiert. Wer rät,
   schreibt das Stylesheet zweimal.
2. **Wo wird sie gehostet und wo angesehen?** Danach richtet sich, ob
   saubere Adressen möglich sind, ob eine `.htaccess` gebraucht wird und
   welche Vorschaufassung am Ende steht. Apache und LiteSpeed, Netlify,
   GitHub Pages und ein reiner Dateiaufruf verhalten sich verschieden.
3. **Preserve oder Overhaul?** Bleibt die Marke erkennbar, oder darf
   alles neu? Das entscheidet über Farbe, Schrift und Bildsprache.

Wenn der Auftraggeber das nicht beantworten kann, entscheide selbst und
sage die Entscheidung in einem Satz an. Aber frage zuerst.

## Phase 1: Auslesen, einmal und vollständig

Alles in einem Durchgang, bevor gestaltet wird. Aus dem ausgelieferten
HTML, nicht aus dem Gedächtnis.

- **Struktur:** alle internen Links, daraus die Seitenliste.
- **Inhalte je Seite:** Überschriften, Fließtext, Preise mit Dauer,
  Kontaktdaten, Öffnungszeiten, Team, Rechtstexte.
- **Bilder:** auch die, die per Skript oder als Hintergrund geladen
  werden. `data-src`, `data-lazyload`, `background-image` mitnehmen.
- **Markenfarben:** die Hexwerte im HTML zählen. Die häufigste ist fast
  immer die Markenfarbe.

**Führe eine Liste, welches Bild zu welchem Abschnitt gehört.** Der
teuerste Einzelfehler im Referenzprojekt war, vier Behandlungsfotos zu
laden und dann nicht zu verwenden, weil die Zuordnung nirgends stand. Das
kostete einen ganzen Nachbau.

Am Ende der Phase: **Welche Bilder sind noch unbenutzt?** Diese Frage
gehört in jeden Durchgang, nicht nur in den letzten.

## Phase 2: Richtung festlegen und ansagen

Ein Satz, bevor Code entsteht:

> Ich lese das als: *Seitenart* für *Zielgruppe*, in *Tonfall*, mit
> *Schrift* und *Farbherkunft*.

**Farbe rechnerisch prüfen, nicht schätzen.** Markenfarben aus
Kleinbetrieben erfüllen oft keinen Kontrast. Im Referenzprojekt erreichte
die Markenfarbe 2,66:1 und war als Textfarbe unbrauchbar. Lösung: sie
bleibt Fläche und Linie, für Text wird eine abgedunkelte Variante
abgeleitet. Kontraste vor dem Bauen durchrechnen, für jede Kombination
aus Textfarbe und Hintergrund.

## Phase 3: Bauen

Für eine kleine Unternehmensseite: handgeschriebenes HTML, ein
Stylesheet, ein Skript ohne Abhängigkeiten. Kein Build-Schritt bedeutet
keine Kette, die brechen kann, und ein Ergebnis, das auf jedem Webspace
liegt.

Was eine Seite nach Baukasten aussehen lässt, und was stattdessen geht:

| Vermeiden | Stattdessen |
| --- | --- |
| Kartenraster mit Icon-Kreisen | Verzeichnis mit Haarlinien und Führungspunkten |
| Runde Ecken, weiche Schatten | Rechteckige Kanten, Ordnung über Weißraum |
| Pillen-Buttons | Rechteckige Fläche, daneben ein unterstrichenes Wort |
| Hakensymbole in Listen | Zeilen mit Haarlinie |
| Farbiges Akzentwort | Kursivsatz |
| Bild im gerahmten Kasten | Bild bricht aus dem Satzspiegel heraus |

**Eine Ausnahme, die zählt:** Bei Branchen, die über Bilder verkaufen
(Kosmetik, Gastronomie, Handwerk, Immobilien) ist ein rein typografisches
Layout zu karg. Dort braucht es großformatige Bildstrecken mit echtem
Beschreibungstext. Im Referenzprojekt war genau das der Nachbau, den die
Kundin zu Recht eingefordert hat.

**Deutsche Komposita brechen Layouts.** `hyphens: auto` auf Überschriften
und `overflow-wrap: break-word`, dazu `min-width: 0` auf allen
Rasterkindern. Sonst sprengt ein Wort wie
„Verbraucherstreitbeilegung" bei 320 px die ganze Seite.

**Dateinamen konsequent kleinschreiben.** Gemischte Schreibweise
funktioniert auf macOS und bricht auf dem Linux-Server. Dieser Fehler ist
im Referenzprojekt real aufgetreten.

## Phase 4: Prüfen, ein Durchgang

`scripts/pruefen.py` deckt in einem Lauf ab, was sonst über mehrere
Runden verteilt gefunden wird. Der Pfad ist relativ zum Skill-Ordner, den
Claude Code beim Laden als Basisverzeichnis nennt, nicht zum Projekt:

```bash
# Server im Projektordner starten
python3 -m http.server 8000 &

# Prüfen, Pfad an das Basisverzeichnis der Skill anpassen
python3 <skill-ordner>/scripts/pruefen.py http://localhost:8000 \
        --geraete --quelle .
```

`--geraete` ergänzt sieben Geräteprofile in beiden Lagen, `--quelle`
schaltet die Strichprüfung im Quelltext dazu. Ohne Funde ist der
Rückgabewert 0, sonst 1.

Geprüft werden: axe-core über alle Seiten und Breiten, horizontales
Scrollen von 320 bis 2560 px, Konsolenfehler, fehlgeschlagene Anfragen,
ob jedes Bild lädt, Trefferflächen unter 44 px, und Bindestrichzeichen
im Text.

Zwei Dinge, die dabei regelmäßig auffallen:

- **Trefferflächen.** Telefonnummern im Fließtext liegen bei rund 23 px
  Höhe. Auf dem Handy ist die Telefonnummer der wichtigste Klick der
  Seite und darf nicht das kleinste Ziel sein. Polsterung mit passendem
  negativem Außenabstand vergrößert die Fläche, ohne das Satzbild zu
  ändern. Verweise mitten im Satz bleiben ausgenommen, WCAG 2.5.8 sieht
  das ausdrücklich vor.
- **Lazy-Bilder im Test.** Ein Bild, das im Screenshot fehlt, ist meist
  nicht kaputt, sondern nur noch nicht geladen. Vor dem Urteil mit
  `wait_for_function` auf `complete && naturalWidth > 0` warten.

## Phase 5: Vorschau und Übergabe

**Immer mit einer Vorschau abschließen, die der Auftraggeber öffnen
kann.** Welche, hängt an Frage 2 aus dem Vorlauf:

| Zweck | Fassung |
| --- | --- |
| Schnell selbst ansehen | lokaler Server, `python3 -m http.server` |
| Ohne Terminal zeigen | Schriften als Base64 im Stylesheet, öffnet per Doppelklick |
| Kundin bekommt einen Link | zum Hochladen, mit `noindex` abgesichert |

**Die Vorschau für die Kundin muss gegen Suchmaschinen gesperrt sein.**
Ein Entwurf auf öffentlicher URL hat denselben Inhalt wie die echte Seite
und konkurriert mit ihr um dieselben Suchbegriffe. Dreifach absichern:
`noindex` im Kopf jeder Seite, `robots.txt`, und die Kopfzeile
`X-Robots-Tag` über `_headers` für Netlify beziehungsweise `.htaccess`
für Apache.

**Über `file://` laden Schriften nicht.** Der Browser behandelt sie als
Cross-Origin-Anfrage. Für eine Doppelklick-Fassung die woff2-Dateien als
Base64 einbetten und die `<link rel="preload" as="font" crossorigin>`
entfernen, sonst bleibt der Fehler in der Konsole.

**Zum Link selbst:** Eine Seite mit Namen, Logo und Telefonnummer eines
realen Unternehmens veröffentliche ich nicht unter einer teilbaren
Adresse. Der Auftraggeber tut das, in einem Schritt: die fertige ZIP auf
`app.netlify.com/drop` ziehen, die Datei selbst, ohne Entpacken. Diesen
Satz mitliefern, dann ist die Übergabe vollständig.

## Was nie erfunden wird

Preise, Öffnungszeiten, Entfernungen, Haltestellen, Bewertungen,
Kundenstimmen, Vorher-Nachher-Bilder, Rechtstexte. Alles davon stammt
aus der bestehenden Seite oder es steht nicht auf der neuen.

Im Referenzprojekt stand kurzzeitig „Zwei Gehminuten von der
Hoheluftbrücke" im Hero. Nichts auf der Quellseite belegte das. Bei einer
Kundenseite ist eine solche Angabe kein Schönheitsfehler, sondern eine
falsche Aussage über ein echtes Unternehmen.

Was nur der Betreiber liefern kann, wird als offener Punkt dokumentiert,
nicht geraten: Formular-Endpunkt, ÖPNV und Parken, Social-Media-Profile,
und die Datenschutzerklärung, die nach einem Technikwechsel ohnehin
juristisch geprüft werden muss.

## Ablage

Ein eigener Branch für die Website, getrennt von allem anderen im
Repository. Im Referenzprojekt landete sie zuerst in einem fremden Pull
Request und musste per Cherry-Pick herausgelöst werden.
