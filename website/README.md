# Gandert. Webdesign – Website

Statische Website (HTML, CSS, ein kleines JavaScript) plus ein PHP-Skript für das Kontaktformular. Läuft ohne Build-Schritt auf Hostinger oder jedem anderen Hosting mit PHP.

## Dateien

| Datei | Zweck |
| --- | --- |
| `index.html` | Startseite: Leistungen, Preise, Betreuung, Ablauf, Über mich, Fragen, Kontakt |
| `impressum.html`, `datenschutz.html` | Pflichtseiten |
| `danke.html` | Bestätigung, falls das Formular ohne JavaScript abgeschickt wird |
| `kontakt.php` | Verschickt Anfragen per E-Mail (mit Spam-Schutz) |
| `assets/style.css`, `assets/main.js` | Gestaltung, Mobilmenü, Formular |
| `assets/fonts/` | DM Serif Display und Manrope, **lokal** eingebunden |
| `llms.txt` | Kurzfassung für KI-Assistenten wie ChatGPT |
| `robots.txt`, `sitemap.xml` | Für Suchmaschinen |
| `.htaccess` | Leitet auf HTTPS um, setzt Sicherheits-Header und Cache-Zeiten |

## Vor dem Livegang ausfüllen

Alle Platzhalter stehen in eckigen Klammern. Suchen mit `grep -rn "\[" --include=*.html --include=*.php --include=*.txt --include=*.xml .`

- [ ] `[DOMAIN]` in `index.html`, `robots.txt`, `sitemap.xml`, `llms.txt`, `kontakt.php`
- [ ] `[TELEFON]` und `[E-MAIL]` in `index.html`, `impressum.html`, `datenschutz.html`, `llms.txt`, `kontakt.php`
- [ ] `[STRASSE HAUSNUMMER]` und `[PLZ]` in `impressum.html` und `datenschutz.html`. Eine ladungsfähige Anschrift ist Pflicht; ein Postfach genügt nicht.
- [ ] `[ANZAHL]` Tage Speicherdauer der Server-Protokolle in `datenschutz.html` (in der Hostinger-Verwaltung nachsehen)
- [ ] Absender in `kontakt.php` als Postfach der eigenen Domain anlegen, damit Mails nicht im Spam landen

## Rechtliches, worauf geachtet wurde

- **Keine Google Fonts von Google-Servern.** Die Schriften liegen im Ordner `assets/fonts`. Für eingebundene Google Fonts gab es Abmahnungen (LG München, 2022).
- **Keine Cookies, kein Tracking, keine eingebetteten Karten oder Videos.** Deshalb ist kein Cookie-Banner nötig. Wird später z. B. Google Maps oder Analytics ergänzt, braucht es Banner **und** eine angepasste Datenschutzerklärung.
- **Impressum nach § 5 DDG** (hat 2024 das TMG abgelöst). Ohne Link zur EU-Streitschlichtungsplattform, weil diese im Juli 2025 eingestellt wurde.
- **§ 19 UStG:** Impressum und Preis-Fußnote gehen von der Kleinunternehmerregelung aus. Laut Businessplan ist das noch mit der Steuerberatung zu klären. Falls nicht zutreffend: den Hinweis entfernen, die USt-IdNr. ins Impressum eintragen und festlegen, ob die Preise netto oder brutto gelten.
- **Kontaktformular** mit Einwilligungs-Häkchen und Link zur Datenschutzerklärung. Die Datenschutzerklärung ist ein Entwurf passend zu dieser Technik und sollte vor dem Livegang mit einem Generator (eRecht24, IT-Recht Kanzlei) abgeglichen werden.
- **Mit Hostinger** einen Vertrag zur Auftragsverarbeitung (AVV) abschließen; das geht in der Hostinger-Verwaltung.

## Hochladen

Den kompletten Inhalt dieses Ordners (auch die versteckte Datei `.htaccess`) per Dateimanager oder FTP in `public_html` hochladen. Danach prüfen:

1. `https://` ist aktiv und `http://` leitet um.
2. Das Formular einmal selbst ausfüllen, die Mail muss ankommen.
3. Die Seite auf dem eigenen Smartphone durchklicken.
4. In der Google Search Console die `sitemap.xml` einreichen.

## Gestaltung

- Logo: Entwurf 44, „G in Blau, gefülltes Quadrat“, aus dem Canvas „Gandert. Logo-Entwürfe“
- Farben: Grund `#070b14`, Fläche `#0c1320`, Text `#e6edf5`, Akzent `#38BDF8`
- Schriften: DM Serif Display (Überschriften, Wortmarke), Manrope (Fließtext)
- Preise und Abos: aus dem Entwurf „Gandert Design – Preise & Abos“
