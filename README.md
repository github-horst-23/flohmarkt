# CarstenFit

Eine kleine, installierbare Trainings-PWA für Carstens persönlichen Gebrauch. Trainingsplan und Verlauf bleiben im Browser auf dem jeweiligen Gerät.

## Starten

Die Dateien über einen lokalen Webserver oder einen statischen Webhost mit HTTPS bereitstellen. Für Installation und Offline-Nutzung braucht der Browser einen sicheren Kontext (localhost zählt dazu). Danach die Seite im Browser öffnen und „Zum Home-Bildschirm“ bzw. „App installieren“ auswählen.

Es gibt keine Build- oder Paketinstallation. Der Service Worker legt die App-Dateien für die Offline-Nutzung im Cache ab.

## Funktionen

- Wochentrainingsplan mit bearbeitbaren Einheiten und Übungen
- Übungskatalog mit den zuletzt verwendeten Satzwerten
- Protokoll pro Arbeitssatz: Gewicht und Wiederholungen, plus Notizen
- Trainingshistorie mit Einheiten, Arbeitssätzen und Volumen
- Auswertung von Kraftverlauf und Trainingshäufigkeit
- Spotify-Player für einen gespeicherten Playlist-, Album- oder Titel-Link
- JSON-Backup exportieren und wieder importieren

Die App speichert weiterhin eine lokale Offline-Kopie. Optional kann sie den Datensatz mit Supabase synchronisieren, damit CarstenFit in mehreren Browsern denselben Trainingsstand lädt. Spotify-Inhalte laufen im offiziellen Spotify-Embed-Player; dessen Wiedergabe braucht eine Internetverbindung.

## Cloud-Synchronisierung mit Supabase einrichten

1. Erstelle ein Supabase-Projekt und öffne dort **SQL Editor**. Führe den Inhalt von [`supabase-setup.sql`](supabase-setup.sql) einmal aus. Damit werden Tabelle, Grants und Row Level Security erstellt. Jede Datenbankzeile ist auf den angemeldeten Benutzer begrenzt.
2. Stelle die App über HTTPS bereit, zum Beispiel über GitHub Pages. In Supabase unter **Authentication → URL Configuration** trägst du die URL deiner App als Site URL ein. Aktiviere E-Mail/Passwort-Anmeldung.
3. Kopiere die **Project URL** und den **Publishable Key** aus dem Supabase-Dialog **Connect**.
4. Öffne CarstenFit und tippe oben auf das Wolken-Symbol. Trage URL und Publishable Key ein und erstelle dein persönliches Konto. Falls E-Mail-Bestätigung aktiv ist, bestätige zuerst die E-Mail und melde dich dann an.
5. Beim ersten Abgleich ohne vorhandenen Cloud-Datensatz lädt CarstenFit deine lokalen Daten hoch. Wenn bereits Cloud-Daten existieren, kannst du auswählen, ob du die Cloud-Version laden oder deine lokalen Daten hochladen möchtest.

Änderungen werden lokal gespeichert und bei aktiver Verbindung automatisch in die Cloud geschrieben. Versionsprüfungen verhindern, dass ein älterer Browserstand unbemerkt neuere Cloud-Daten überschreibt. Bei einem Konflikt fragt CarstenFit nach der zu verwendenden Version. Bei Offline-Änderungen erfolgt der Abgleich nach Wiederherstellung der Verbindung oder über **Jetzt synchronisieren**.

Im Browser eingebaut werden nur Project URL und Publishable Key. Verwende niemals den `service_role`- oder Secret-Key in der PWA. Die RLS-Regeln in der SQL-Datei sind erforderlich, damit Benutzer ausschließlich auf ihre eigene Zeile zugreifen.

## Daten lokal sichern und übertragen

Über **Export** in der Kopfzeile kannst du eine JSON-Sicherung aller CarstenFit-Daten herunterladen und auf diesem oder einem anderen Gerät importieren. Das bleibt auch mit aktivierter Cloud-Synchronisierung als manuelles Backup verfügbar.
