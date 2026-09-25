# Dorfflohmarkt Dudenhofen

Eine installierbare Web-App für den Dorfflohmarkt am 26. September 2026, 10–16 Uhr.

## Enthalten

- 106 zusammengeführte Standorte aus 109 Stand-Einträgen und 18 Verpflegungsangaben
- Suche, Angebotskategorien, Typfilter, Favoriten und Routenplanung
- das bereitgestellte Smiley-Icon als Kartenmarker
- PWA-Manifest und Service Worker für die Installation im Browser
- Adminformular zum Anlegen von Ständen und Export der aktualisierten Datendatei

## Bereitstellung

Die Dateien in diesem Ordner müssen unter einer HTTPS-Adresse bereitgestellt werden, damit Browser die Installation der PWA anbieten. Zum Anzeigen der Basiskarte wird eine Internetverbindung benötigt. Favoriten und bereits gefundene Koordinaten werden lokal im Browser gespeichert. Für Safari beim direkten Öffnen über `file://` lädt die App die Daten aus `data.js`, da lokale JSON-Dateien dort nicht zuverlässig per `fetch` abrufbar sind.

`data.json` enthält ein Feld `coordinates` pro Standort. Sobald freigegebene Koordinaten darin stehen, erscheinen die Marker direkt beim Laden. Bis dahin zeigt die App die Standorte in der Liste. Das Kartenmaterial stammt von OpenStreetMap; die App blendet den Kartenhinweis ein.

## Stände verwalten

„＋ Stand hinzufügen“ öffnet das Adminformular. Neue Einträge werden zunächst nur im lokalen Browser gespeichert. Mit „Daten exportieren“ werden aktualisierte `data.json` und `data.js` heruntergeladen. `data.json` ersetzt die Serverdatei für alle Besucher; bei direktem Öffnen per `file://` muss außerdem `data.js` ersetzt werden. Der Adminbereich hat in dieser statischen Version kein Login und Änderungen werden nicht automatisch mit anderen Geräten synchronisiert.

## Koordinaten ergänzen

Für die einmalige Geokodierung in einer Umgebung mit Internetzugang: ZIP entpacken, im entpackten Ordner ein Terminal öffnen und `python3 geocode_maps_co.py` starten. Das Skript fragt den API-Schlüssel verdeckt ab, übermittelt nur die 106 Adressen, ergänzt Koordinaten und aktualisiert das ZIP. Es speichert den Schlüssel nicht. Die Trefferangabe `geocodeMatch` bleibt in `data.json`, damit die Zuordnung kontrolliert werden kann.

## Quelldaten

`data.json` enthält zusammengeführte Standorte und getrennte Felder für Flohmarktangebote und Verpflegung. Doppelte Adressen wurden zusammengeführt; ihre Einträge bleiben als einzelne Angebotsangaben erhalten. Ein Eintrag ohne Angebot ist mit `incomplete: true` markiert.
