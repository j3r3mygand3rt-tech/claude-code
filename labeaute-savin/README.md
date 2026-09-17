# La Beauté de Savin, Website-Relaunch

Neubau der Website des Kosmetikinstituts La Beauté de Savin, Brahmsallee 24, Hamburg.
Ersetzt die bestehende WordPress-Installation durch eine statische Seite ohne Build-Kette,
ohne Framework und ohne externe Abhängigkeiten.

---

## 1. Designentscheidung

**Einordnung:** Redesign im Modus *Preserve*. Die Marke bleibt erkennbar, die Umsetzung ist neu.
Zielgruppe sind anspruchsvolle Privatkundinnen und Privatkunden in Harvestehude und Eppendorf.
Bildsprache: ruhig, hochwertig, redaktionell. Das Ziel der Seite ist die Terminanfrage.

**Farbe.** Die Markenfarben stammen unverändert aus der bestehenden Seite: Altrosa `#c39391`
(dort 81 Mal verwendet) und Taupe `#ac9f94`. Altrosa erreicht auf hellem Grund nur ein
Kontrastverhältnis von 2,66:1 und ist damit als Textfarbe nicht barrierefrei. Es dient deshalb
ausschließlich als Fläche. Für Text, Links und Buttons wurde daraus `--rose-deep #8f5a57`
abgeleitet, das 5,57:1 erreicht und WCAG AA erfüllt. Alle Kombinationen wurden rechnerisch
geprüft, nicht geschätzt.

**Schrift.** Marcellus für Überschriften, Jost für Fließtext. Marcellus ist eine klassische
Antiqua und trägt die französische Anmutung des Namens. Jost geht auf die Futura zurück, wirkt
sachlich und bleibt in den Preistabellen auch bei kleinen Graden lesbar. Beide Schriften werden
selbst ausgeliefert, es geht keine Anfrage an Google.

**Bewegung.** Zurückhaltend. Inhalte fahren beim Erscheinen einmalig ein, Zustandswechsel dauern
160 bis 280 ms. `prefers-reduced-motion` schaltet jede Animation ab. Ohne JavaScript ist alles
sofort sichtbar, nichts bleibt versteckt.

---

## 2. Aufbau

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

Das Icon-Sprite ist zusätzlich direkt in jede HTML-Datei eingebettet. Das spart einen
Ladevorgang und sorgt dafür, dass die Symbole auch beim Öffnen per Doppelklick erscheinen,
also ohne Webserver.

---

## 3. Weg zur Terminanfrage

Der Kontaktweg ist auf jeder Bildschirmgröße und in jeder Scrollposition erreichbar:

| Bereich | Mobil | Desktop |
| --- | --- | --- |
| Kontaktleiste oben | ausgeblendet | Adresse, Öffnungszeiten, E-Mail, Telefon |
| Kopfzeile, mitlaufend | Telefonsymbol plus Button „Termin" | Telefonnummer plus Button „Termin anfragen" |
| Aktionsleiste unten | ab 420 px Scrolltiefe eingeblendet | nicht nötig |
| Im Inhalt | Buttons in Hero, Studio, Gutscheine | ebenso |
| Fußzeile | Telefon, Mobil, E-Mail | ebenso |

Auf sehr schmalen Geräten (unter 400 px) wird das Button-Label auf „Termin" verkürzt, damit
der Handlungsaufruf sichtbar bleibt statt zu verschwinden.

---

## 4. Inhalte

Alle Texte, Leistungen, Preise und Kontaktdaten stammen von der bestehenden Website und wurden
dort ausgelesen. Sprachlich überarbeitet, inhaltlich unverändert. Erfunden wurde nichts,
insbesondere keine Preise, keine Bewertungen und keine Kundenstimmen.

Übernommen sind unter anderem: fünf HydraFacial-Varianten mit Preisen von 159 bis 269 Euro,
vier klassische Gesichtsbehandlungen, drei dermatologische Behandlungen, vier Herrenbehandlungen,
Maniküre und Fußpflege mit je einer vollständigen Preisliste, Eyebrows, die Zusatzleistungen mit
ihrer Doppelpreisstruktur (in und außerhalb der Behandlung), die drei Namen des Teams sowie
Anschrift, Telefon, Mobilnummer, E-Mail und Öffnungszeiten.

**Bilder:** Alle 15 Bilder stammen im Original von der bestehenden Seite. Sie wurden nicht
ersetzt und nicht beschnitten. Zusätzlich liegt jedes Bild als WebP in drei Breiten vor, die
über `srcset` passend zum Gerät ausgeliefert werden. Das JPEG bleibt als Rückfallebene erhalten.

---

## 5. Gemessene Ergebnisse

Gemessen in Chromium, erster Aufruf ohne Cache, lokaler Server.

| | Bestehende Seite | Neue Seite |
| --- | --- | --- |
| HTML-Dokument | 147,7 KB | 49,8 KB |
| CSS-Dateien | 12 | 1 |
| JS-Dateien | 19 | 1 |
| Anfragen gesamt | mindestens 40 | 12 (mobil) |
| Übertragen mobil | nicht gemessen | 307 KB |
| First Contentful Paint | nicht gemessen | 148 ms |

Die bestehende Seite wurde aus dem ausgelieferten HTML gezählt, nicht im Browser gemessen:
Chromium in dieser Umgebung vertraut dem Proxy-Zertifikat nicht, und die TLS-Prüfung
abzuschalten wäre der falsche Weg für eine Zahl. Die Angaben zur neuen Seite sind
Browser-Messungen.

**Geprüft und bestanden:**

- axe-core, Regelsätze WCAG 2.0/2.1 Stufe A und AA plus Best Practices: **0 Verstöße**
  auf allen vier Seiten, jeweils bei 390 px und 1440 px.
- Kein horizontales Scrollen bei 320, 360, 390, 414, 768, 1024, 1440 und 1920 px.
- Keine Konsolenfehler, keine fehlgeschlagenen Anfragen.
- Alle 13 Bilder laden, alle werden als WebP ausgeliefert.
- Statische Prüfung mit `web-quality-audit`: 0 Fehler. Die fünf Warnungen sind Fehlalarme,
  vier betreffen den SVG-Namespace `http://www.w3.org/2000/svg`, die fünfte ein Zitat im
  Datenschutztext.
- Funktionstest: Menü öffnet und schließt, Escape schließt, Hintergrund wird gesperrt und
  wieder freigegeben. Formularvalidierung meldet leere Pflichtfelder und ungültige
  E-Mail-Adressen, setzt den Fokus auf das erste fehlerhafte Feld und löscht Fehler bei
  Korrektur. Tastaturreihenfolge beginnt mit dem Sprunglink.

---

## 6. Vor dem Livegang zu erledigen

Drei Punkte kann nur der Betreiber entscheiden:

1. **Kontaktformular.** Ohne Konfiguration öffnet das Formular eine vorbereitete E-Mail im
   Mailprogramm. Das funktioniert überall, wirkt aber altmodisch. Für echten Serverversand
   das Ziel eintragen:
   ```html
   <form class="form" data-contact-form data-endpoint="https://ihr-endpunkt">
   ```
   Der Rest der Logik ist vorhanden, inklusive Fehlerbehandlung und deaktiviertem Button
   während des Sendens.

2. **Datenschutzerklärung.** Der Text wurde unverändert übernommen, die technische Grundlage
   hat sich aber geändert: kein WordPress, keine externen Schriften, kein eingebettetes
   YouTube, keine eingebettete Google-Maps-Karte. Die Abschnitte zu diesen Diensten treffen
   nicht mehr zu. Die Seite trägt dazu einen sichtbaren Hinweis. Bitte juristisch prüfen lassen.

3. **Instagram-Adresse.** Im Fußbereich steht derzeit `https://www.instagram.com/` ohne
   Profilnamen, weil die bestehende Seite den Link über ein Skript aufbaut und der Name im
   HTML nicht auftaucht. Bitte eintragen.

---

## 7. Betrieb

Die Seite ist statisch. Es genügt, den Ordner auf einen Webserver zu legen, es gibt keinen
Build-Schritt und keine Datenbank. Geeignet sind jeder klassische Webspace, Netlify, Vercel
oder GitHub Pages.

Empfohlene Servereinstellungen: Auslieferung über HTTPS, Komprimierung mit gzip oder brotli
für `.html`, `.css`, `.js` und `.svg`, sowie eine lange Cache-Dauer für `assets/fonts` und
`assets/img`, die sich nicht mehr ändern.

Lokal ansehen:

```bash
python3 -m http.server 8000
```

Danach `http://localhost:8000` aufrufen.
