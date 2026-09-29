---
name: geraete-vorschau
description: Zeigt eine fertige Website im Handy-, Android-, Kleinhandy- und iPad-Rahmen (mit Drehen und Neu laden) als Artifact. Immer verwenden, nachdem eine Website gebaut oder geändert wurde, und wenn der Nutzer einen Handytest, eine Handy-Ansicht oder eine Tablet-Vorschau möchte.
---

# Geräte-Vorschau

Der Nutzer möchte nach jedem Website-Bau die Seite im Handyrahmen sehen und durchklicken können.

## Ablauf

1. Website fertig bauen und wie gewohnt prüfen.
2. Vorschau erzeugen (bettet lokale CSS-, JS-, Bild- und Schriftdateien ein):

   ```bash
   python3 .claude/skills/geraete-vorschau/geraete_vorschau.py <pfad/zur/index.html> <scratchpad>/geraete/<name>-handy-vorschau.html --titel "<Name> Handy-Vorschau"
   ```

3. Die erzeugte Datei mit dem Artifact-Tool veröffentlichen (`icon: "phone"`). Bei späteren Änderungen dieselbe Datei neu erzeugen und unter demselben Pfad erneut veröffentlichen, damit der Link gleich bleibt.
4. Dem Nutzer den Link geben und kurz sagen, wie man Gerät wechselt, dreht und neu lädt.

## Hinweise

- Die Website läuft im Rahmen in echter Gerätebreite (iframe `srcdoc`), dadurch greifen ihre Handy-Layouts.
- Geräte: iPhone 14 (390 × 844), Pixel 7 (412 × 915), kleines Handy (320 × 640), iPad Mini (768 × 1024), jeweils auch quer.
- Server-Funktionen (PHP-Formulare, Datenbank) laufen in der Vorschau nicht. Das dem Nutzer sagen.
- Die Artifact-Seite ist privat; zum Zeigen muss der Nutzer sie über das Teilen-Menü freigeben.
