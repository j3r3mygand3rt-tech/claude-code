# Tough Gym Hamburg, Relaunch

Statische Website für die Kampfsportschule Tough Gym in Hamburg Altona.
Handgeschriebenes HTML, CSS und JavaScript. Keine Build-Kette, kein
Framework, keine Abhängigkeit, kein Nachladen von fremden Servern.

Vorlage für Struktur und Inhalt war die bisherige Seite
[tough-gym.de](https://www.tough-gym.de/), eine Wix-Seite.

## Seiten

| Adresse          | Datei                | Inhalt |
| ---------------- | -------------------- | ------ |
| `/`              | `index.html`         | Einstieg, drei Stile, Meisterblock, Personaltraining, Impressionen |
| `/kurse`         | `kurse.html`         | Boxen, Thaiboxen, BJJ, Kinder, Jugend, Managerboxen, Personaltraining |
| `/trainingsplan` | `trainingsplan.html` | Die Woche von Montag bis Samstag, dazu was mitzubringen ist |
| `/trainer`       | `trainer.html`       | Human mit Titelliste, das übrige Trainerteam |
| `/preise`        | `preise.html`        | Vier Tarife, Kassen- und Personaltraining-Hinweise |
| `/impressionen`  | `impressionen.html`  | 16 Bilder aus Gym und Wettkampf |
| `/kontakt`       | `kontakt.html`       | Adresse, Öffnungszeiten, Anfrageformular |
| `/impressum`     | `impressum.html`     | Anbieterkennzeichnung |
| `/datenschutz`   | `datenschutz.html`   | Datenschutzerklärung, unverändert übernommen |

Die alte Adresse `/datenschutzerklärung` wird per 301 auf `/datenschutz`
umgeleitet, damit Suchtreffer und Lesezeichen nicht ins Leere laufen.

## Der Deutsche Meister

Der Auftrag war, den Meistertitel eines Trainers zu berücksichtigen. Die
Zuordnung war im Quelltext der Bestandsseite nicht eindeutig lesbar, weil
Namen und Titelblöcke dort als frei positionierte Textfelder liegen. Sie
wurde deshalb über die Reihenfolge im Quelltext geprüft, Zeichenposition für
Zeichenposition. Das Ergebnis:

**Human** trägt die Titel:

* 1995 Deutscher Meister Thaiboxing IPTA, bis 70 kg
* 1995 Deutscher Meister Kickboxing, bis 70 kg
* 2001 Deutscher Meister Kickboxing, bis 76 kg
* 2003 Europameister Kickboxing, bis 76 kg
* 2015 Weltmeister Kickboxing, Kimbo Serie, bis 72 kg
* 3. Dan Kyokushin Budo Kai All Round Fighting
* 2008 bis 2011 Representative M1-Global-Team Germany

**Homayoun** trägt 3. Dan Kyokushin Budo Kai All Round Fighting, dieselbe
M1-Global-Rolle und eine Bilanz von 15 Kämpfen (12 Siege, 3 Niederlagen).

Der Titelblock steht auf der Startseite als eigenes Kapitel und auf der
Trainerseite noch einmal ausführlich, jeweils mit Jahr und Gewichtsklasse,
damit die Angaben nachprüfbar bleiben. Das Foto dazu ist das echte: die fünf
Gürtel über dem Ringseil.

## Look

Die Seite ist dunkel. Das ist keine Stilfrage: die Wortmarke ist weiß auf
Transparenz, und die Halle ist ein Kellergeschoss mit roten Matten und rotem
Ring. Ein heller Auftritt hätte das Logo unbrauchbar gemacht und die Fotos
verraten.

Die Farben sind aus den Fotos gemessen, nicht geschätzt. Matten und Ringseile
liegen bei Farbton 348 bis 352 Grad. Daraus zwei Rot-Rollen, weil ein
einzelnes Rot beides nicht kann:

| Wert | Rolle | Kontrast |
| ---- | ----- | -------- |
| `#c8102e` | Fläche, Schaltflächen, Linien | weiße Schrift darauf **5,88:1** |
| `#ff4b57` | Rot als Text auf dunklem Grund | **5,91:1** auf `#0d0d0f`, 5,45 auf `#17171a`, 4,77 auf `#232327` |
| `#ffffff` | Text | **19,4:1** auf `#0d0d0f` |
| `#a5a5ad` | gedämpfter Text | **7,9:1** |

Schrift: **Anton** für die Schlagzeilen, weil eine schmale, schwere Grotesk
die Sprache von Kampfsportplakaten spricht, **Barlow** für alles andere.
Beide selbst ausgeliefert (120 KB woff2), keine Verbindung zu Google Fonts.

## Inhalt: was woher kommt

Alle Angaben stammen von der bisherigen Seite. **Nichts ist hinzuerfunden** –
keine Preise, keine Trainingszeiten, keine Titel, keine Öffnungszeiten.
Die Texte sind sprachlich straffer und direkter gefasst (die Seite duzt, wie
die Vorlage), ohne den inhaltlichen Kern zu verändern.

Von der Instagram-Seite konnte nichts übernommen werden: Instagram beantwortet
Abrufe aus dieser Umgebung mit HTTP 429. Die Bildsprache stammt deshalb aus
den Fotos des Gyms selbst, was auf dasselbe Material hinausläuft.

## Bildmaterial

Ausschließlich die originalen Bilder der bisherigen Website, 36 Motive. Dazu
WebP-Fassungen in den Breiten, die tatsächlich abgerufen werden; die JPEG-
beziehungsweise PNG-Fassung bleibt als Rückfall im `<img>`.

Die Galeriebilder wurden auf 900 px gedeckelt, weil sie nur als Kacheln
erscheinen. Alle Dateinamen sind kleingeschrieben: gemischte Schreibweise
funktioniert auf macOS und bricht auf einem Linux-Server.

Zwei der sechs Kursbilder sind erkennbar zugekaufte Motive (Brazilian
Jiu-Jitsu, Managerboxen), die übrigen sind im Gym entstanden. Die echten
Bilder stehen an den sichtbarsten Stellen.

## Technik

* **Bilder** `<picture>` mit WebP-Quellen und `srcset`/`sizes`, JPEG als
  Rückfall. Das Hero-Bild lädt mit `fetchpriority="high"`, alles darunter
  `loading="lazy"`.
* **Bewegung** nur `transform` und `opacity`, Kurve
  `cubic-bezier(0.23, 1, 0.32, 1)`. Hover-Effekte hängen an
  `@media (hover: hover) and (pointer: fine)`, damit auf dem Touchscreen
  nichts klebt. Bei `prefers-reduced-motion: reduce` bleibt das Einblenden,
  die Bewegung fällt weg.
* **Ohne JavaScript** bleibt die Seite vollständig lesbar und bedienbar.
* **Symbole** ein SVG-Sprite, eine Anfrage für alle Symbole.

## Barrierefreiheit

Geprüft mit axe-core (WCAG 2.0 und 2.1, Stufe A und AA, plus Best Practices)
auf allen neun Seiten, bei 390 px und 1440 px, sowie auf sieben
Geräteprofilen in beiden Ausrichtungen. Dazu horizontales Scrollen über zehn
Breiten von 320 px bis 1920 px, Konsolenfehler, fehlgeschlagene Anfragen und
ob jedes Bild nach vollständigem Durchscrollen wirklich geladen ist.

## Vorschau erzeugen

```
python3 tools/build-vorschau.py             # -> vorschau/   zum Doppelklicken
python3 tools/build-vorschau.py --hosting   # -> kundenvorschau/  zum Hochladen
```

`vorschau/` öffnet sich ohne Webserver: die Schriften sind als Base64 in das
Stylesheet geschrieben, das Symbol-Sprite steht in der Seite, und die
Verweise tragen wieder ihre `.html`-Endung. Über `file://` blockiert der
Browser sonst Schriften und Sprite als Cross-Origin-Anfrage.

`kundenvorschau/` ist für einen Hoster gedacht und dreifach gegen
Suchmaschinen gesichert: `noindex` im `<head>`, `robots.txt` und
`X-Robots-Tag` über `_headers` für Netlify sowie `.htaccess` für Apache
beziehungsweise LiteSpeed.

## Vor dem Livegang

1. **Datenschutzerklärung neu fassen lassen.** Der übernommene Text
   beschreibt eine Wix-Seite mit Online-Shop, Zahlungs-Gateways und
   Kreditkartendaten. Die neue Seite hat nichts davon: kein Wix, kein Shop,
   kein Zahlungsverkehr, kein Tracking, keine fremden Schriften, keine
   eingebettete Karte, keine Social Plugins. Ein Hinweiskasten auf der Seite
   sagt das auch den Besuchern. Nebenbei: der Text nennt
   `kontakt@toughgym.de`, der Rest der Seite `info@toughgym.de` – bitte
   vereinheitlichen.
2. **Formularversand einrichten.** Das Formular auf `/kontakt` prüft die
   Eingaben, verschickt aber nichts. Es braucht ein Skript auf dem Server,
   das die Anfrage an `info@toughgym.de` weiterleitet.
3. **Widerspruch bei den Samstagszeiten klären.** Die Öffnungszeiten der
   Bestandsseite nennen Samstag und Sonntag „geschlossen“, der Kursplan
   führt aber samstags BJJ um 10:30 Uhr sowie Kinder- und Jugendtraining um
   10:00 Uhr. Beides ist unverändert übernommen. Was stimmt, muss das Gym
   entscheiden.
4. **Hygienehinweise prüfen.** Der Block auf der Bestandsseite stammt aus der
   Corona-Zeit, ist dort unvollständig (die Punkte 1 bis 3 fehlen im
   Quelltext) und nennt einen Mund-Nasen-Schutz. Übernommen wurden nur die
   Punkte, die dauerhaft gelten: eigenes Equipment, zwei Handtücher,
   Hallenschuhe, Handtuch unterlegen, Hände waschen. Der Mund-Nasen-Schutz
   steht bewusst nicht mehr da.
5. **Registereintrag ergänzen.** Das Impressum der Bestandsseite führt
   „Registergericht“ und „Registernummer“ als leere Felder. Sie stehen
   deshalb nicht in der neuen Fassung.
6. **Adressen ohne `.html`** setzen einen Server voraus, der sie auflöst. Die
   beiliegende `.htaccess` erledigt das auf Apache und LiteSpeed, Netlify tut
   es von sich aus. Auf GitHub Pages funktioniert es **nicht**.
