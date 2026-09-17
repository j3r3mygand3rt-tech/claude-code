# MEDALIFE Groß Borstel, Relaunch

Statische Website für das Gesundheitszentrum MEDALIFE in Hamburg Groß Borstel.
Handgeschriebenes HTML, CSS und JavaScript. Keine Build-Kette, kein
Framework, keine Abhängigkeit, kein Nachladen von fremden Servern.

Vorlage für Struktur und Inhalt war die bisherige Seite
[medalife.de](https://medalife.de/). Die gestalterische Richtung folgt einem
vom Auftraggeber mitgeschickten Entwurf für eine Physiotherapie-Praxis,
übertragen auf die Bestandsfarben von MEDALIFE.

## Seiten

| Adresse             | Datei                    | Inhalt |
| ------------------- | ------------------------ | ------ |
| `/`                 | `index.html`             | Einstieg, vier Bereiche, Über MEDALIFE, Bewertungen, Kursänderungen, MYSPORTS, Standorte |
| `/physiotherapie`   | `physiotherapie.html`    | Alle zehn Behandlungsangebote, Beckenboden-Training, Öffnungszeiten |
| `/training`         | `training.html`          | Trainingsbereich, Kursplan der Woche, neun Kursbeschreibungen, Probetraining |
| `/preise`           | `preise.html`            | Training, Mitgliedschaften, Zusatzleistungen, Massage, Kassenhinweise |
| `/team`             | `team.html`              | 15 Personen mit Foto, 7 weitere namentlich, Stellenangebot |
| `/faq`              | `faq.html`               | 16 Fragen zu Anfahrt, Rezept und Ablauf |
| `/kontakt`          | `kontakt.html`           | Beide Standorte, Anfahrt, Barrierefreiheit, Anfrageformular |
| `/impressum`        | `impressum.html`         | Anbieterkennzeichnung |
| `/datenschutz`      | `datenschutz.html`       | Datenschutzerklärung, unverändert übernommen |
| `/barrierefreiheit` | `barrierefreiheit.html`  | Erklärung zur digitalen Barrierefreiheit |

Die bisherige Seite hatte vierzehn Einzelseiten. Zusammengelegt wurden
Kursplan und Kursbeschreibung in `/training`, `ueber_medalife` in die
Startseite, `konditionen` in `/preise`. Für jede alte Adresse steht in der
`.htaccess` eine dauerhafte Umleitung, damit Suchtreffer und Lesezeichen
nicht auf einer Fehlerseite landen.

## Inhalt: was woher kommt

Alle Angaben sind der bisherigen Seite entnommen. **Nichts ist hinzuerfunden** –
keine Preise, keine Öffnungszeiten, keine Verkehrsanbindung, keine
Qualifikation, keine Bewertung. Die Texte sind sprachlich straffer gefasst,
ohne den inhaltlichen Kern zu verändern.

Zwei Dinge stehen bewusst **nicht** auf der Seite:

* **Online-Terminbuchung für die Physiotherapie.** Dafür braucht es einen
  echten Kalender. Für Kurse und Training verweist die Seite auf das
  vorhandene MYSPORTS-Portal.
* **Eine eingebettete Karte.** Die bisherige Seite lädt Google Maps hinter
  einer Einwilligungsschranke. Stattdessen führt ein Verweis „Route planen“
  direkt zur Routenplanung – das lädt nichts nach und braucht keine
  Einwilligung.

Der Abschnitt **Aktuelle Kursänderungen** auf der Startseite ist wöchentlich
zu pflegen. Er trägt deshalb ein sichtbares Datum („Stand: Woche vom …“).
Übernommen ist der Stand der Quelle.

## Bildmaterial

Es werden ausschließlich die originalen Bilder der bisherigen Website
verwendet, 28 Dateien. Zusätzlich liegt von jedem Bild eine WebP-Fassung in
den Breiten bei, die tatsächlich abgerufen werden. Die JPEG- beziehungsweise
PNG-Fassung bleibt als Rückfall im `<img>`.

Die Fotos aus dem Haus (Trainingsfläche, Therapie am Gerät, Sprossenwand,
Porträts) stehen an den sichtbarsten Stellen; die zugekauften Motive
(Bildrechte Thinkstock, siehe Impressum) tragen die Nebenrollen. Das ist eine
Gestaltungsentscheidung: echte Räume und echte Gesichter wirken glaubwürdiger
als Katalogbilder.

Alle Dateinamen sind kleingeschrieben. Gemischte Schreibweise funktioniert auf
macOS und bricht auf einem Linux-Server.

## Farben

Alle Werte stammen aus dem Bestand:

| Wert      | Herkunft                                   |
| --------- | ------------------------------------------ |
| `#16212b` | Dunkelblau der bisherigen Kopf- und Fußzeile |
| `#ea9701` | Orange, häufigste Akzentfarbe im Quelltext |
| `#d1d7cd` | Salbei, Farbe der Wortmarke im Logo        |

Der Kontrast wurde vor dem Entwurf gerechnet, nicht geschätzt:

* Orange erreicht auf Weiß nur **2.35:1** und ist als Textfarbe unbrauchbar.
  Es dient hier ausschließlich als Fläche, Linie und Schaltfläche – immer mit
  dunkler Schrift darauf (**6.94:1**), nie mit weißer.
* Für Text auf hellem Grund steht `--amber` `#905500`: **6.03:1** auf Weiß,
  **5.59:1** auf `--paper-2`, **5.04:1** auf `--sage-soft`.
* Auf dem Dunkelblau darf Orange selbst Text sein, dort erreicht es 6.94:1.

Die Kopfzeile sitzt auf dem Dunkelblau, weil die Wortmarke im Logo blasser
Salbei ist. Das ist keine Stilentscheidung, sondern eine Folge des Logos.

## Technik

* **Schrift** Archivo in vier Schnitten, selbst ausgeliefert (148 KB woff2).
  Keine Verbindung zu Google Fonts.
* **Bilder** `<picture>` mit WebP-Quellen und `srcset`/`sizes`, JPEG als
  Rückfall. Das Hero-Bild lädt mit `fetchpriority="high"`, alles darunter
  `loading="lazy"`.
* **Bewegung** nur `transform` und `opacity`, Kurve
  `cubic-bezier(0.23, 1, 0.32, 1)`. Hover-Effekte hängen an
  `@media (hover: hover) and (pointer: fine)`, damit auf dem Touchscreen
  nichts klebt. Bei `prefers-reduced-motion: reduce` bleibt das Einblenden,
  die Bewegung fällt weg.
* **Ohne JavaScript** bleibt die Seite vollständig lesbar und bedienbar. Das
  Aufklappen der Leistungen nutzt `<details>`, also den Browser selbst.
* **Symbole** ein SVG-Sprite, eine Anfrage für alle Symbole.

## Barrierefreiheit

Geprüft mit axe-core (WCAG 2.0 und 2.1, Stufe A und AA, plus Best Practices)
auf allen zehn Seiten, bei 390 px und 1440 px, sowie auf sieben Geräteprofilen
in beiden Ausrichtungen. Ergebnis: keine Verstöße, kein horizontales Scrollen
zwischen 320 px und 1920 px, keine Konsolenfehler, keine fehlgeschlagene
Anfrage, alle Bilder geladen.

Trefferflächen sind mindestens 44 px hoch, mit den beiden Ausnahmen, die
WCAG 2.5.8 vorsieht: Verweise mitten im Fließtext und ein Kästchen, das in
seinem Label steckt.

## Vorschau erzeugen

```
python3 tools/build-vorschau.py             # -> vorschau/   zum Doppelklicken
python3 tools/build-vorschau.py --hosting   # -> kundenvorschau/  zum Hochladen
```

`vorschau/` öffnet sich ohne Webserver. Dafür sind die Schriften als Base64 in
das Stylesheet geschrieben (über `file://` blockiert der Browser sie sonst als
Cross-Origin-Anfrage) und die Verweise tragen wieder ihre `.html`-Endung.

`kundenvorschau/` ist für einen Hoster gedacht und dreifach gegen
Suchmaschinen gesichert: `noindex` im `<head>`, `robots.txt`, und
`X-Robots-Tag` über `_headers` für Netlify und `.htaccess` für Apache
beziehungsweise LiteSpeed. Eine unveröffentlichte Vorschau darf nicht
indexiert werden, sonst konkurriert der Entwurf mit der echten Seite um
dieselben Suchbegriffe.

Beide Ordner stehen in der `.gitignore` und werden nicht mitversioniert.

## Vor dem Livegang

1. **Formularversand einrichten.** Das Formular auf `/kontakt` prüft die
   Eingaben, verschickt aber nichts. Es braucht ein Skript auf dem Server, das
   die Anfrage an `info@medalife.de` weiterleitet.
2. **Datenschutzerklärung anpassen lassen.** Der Text ist unverändert
   übernommen. Die Abschnitte 17 bis 19 (Social Plugins, Google Analytics,
   Google Ads Conversion Tracking) und der Hinweis auf Flash-Cookies in
   Abschnitt 5 treffen auf diese Seite nicht mehr zu, weil sie nichts davon
   einsetzt. Ein Hinweiskasten auf der Seite sagt das auch den Besuchern.
3. **Adressen ohne `.html`** setzen einen Server voraus, der sie auflöst. Die
   beiliegende `.htaccess` erledigt das auf Apache und LiteSpeed, Netlify tut
   es von sich aus. Auf GitHub Pages funktioniert es **nicht**. Wer den Block 7
   der `.htaccess` abschaltet, muss auch die `canonical`-Angaben und die
   interne Verlinkung auf `.html` zurückdrehen.
4. **Kursänderungen und Kursplan** aktuell halten.
