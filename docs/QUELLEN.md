# Datenquellen und Datenstände

## Wahl Baden-Württemberg

Quelle: Statistisches Landesamt Baden-Württemberg, [Ergebnisportal Landtagswahl 2026](https://wahlen.statistik-bw.de/ltw26/), [Datensatzbeschreibung](https://www.statistik-bw.de/fileadmin/user_upload/Presse/Pressemitteilungen/2026021_LTW26-Hinweise-DSB.pdf).

`data/bw2026_snapshot.csv` ist eine unveränderte Kopie der im ursprünglichen Projekt verwendeten `ltw26-ergebnisse.csv`. Das Originalnotebook nennt den Abruf am 09.03.2026; eine identische Datei trägt den Zusatz 20260315. Ein genauerer Abrufzeitpunkt lässt sich daraus nicht sicher bestimmen. Daher lautet die Kennzeichnung „Original-Snapshot März 2026“.

Dieser Snapshot enthält 5.358.876 gültige Erststimmen und 5.374.834 gültige Zweitstimmen. Das am 11.11.2026 geprüfte Ergebnisportal nennt im endgültigen Ergebnis 5.359.187 bzw. 5.375.109. Die Veröffentlichung analysiert bewusst den mitgelieferten historischen Snapshot.

Die Datensatzbeschreibung erläutert Gebietsebenen, Großstadtausnahmen und gemeinsame Briefwahl. Gemeindezeilen sind deshalb nicht vollständig als Ergebnisse der dort wohnenden Wahlberechtigten interpretierbar. Die Aufbereitung kontrolliert Landes-, Wahlkreis- und Wahlbezirkssummen getrennt; die nicht gemeindescharf enthaltenen Stimmen werden ausgewiesen. Die ursprüngliche Karte bleibt eine Exploration der verfügbaren Gemeindezuordnungen.

Quellenangabe bei Weiterverwendung: Statistisches Landesamt Baden-Württemberg, Landtagswahl 2026, Original-Snapshot März 2026; eigene Aufbereitung und Darstellung: Dr. Peter Keller. Siehe auch die [Nutzungsbedingungen des Landesamtes](https://www.statistik-bw.de/agb/). Die Code-Lizenz ersetzt keine Bedingungen der Datenanbieter.

## Verwaltungsgeometrien

Quelle: Bundesamt für Kartographie und Geodäsie, VG250, Stand 01.01.2024. Dieser Stand ist in `aktualitaet.txt` des lokal verwendeten Original-Downloadpakets dokumentiert. Der Ausschnitt umfasst Baden-Württemberg, GF = 4, auf Gemeinde-, Kreis- und Landesebene. Felder: AGS, ARS, GEN und Geometrie. Es erfolgen keine neue Vereinfachung und keine Transformation der Originalgeometrien.

Namensnennung: © [BKG](https://www.bkg.bund.de) 2026, [Datenlizenz Deutschland – Namensnennung – Version 2.0](https://www.govdata.de/dl-de/by-2-0), [Datenquellen VG/NUTS](https://sgx.geodatenzentrum.de/web_public/gdz/datenquellen/datenquellen_vg_nuts.pdf). Bearbeitung: Auswahl von Land, Ebenen und Attributen durch Dr. Peter Keller. [Produkt und Nutzungsangaben](https://gdz.bkg.bund.de/index.php/default/open-data/wfs-verwaltungsgebiete-1-250-000-stand-01-01-wfs-vg250.html).

## Reproduzierbarer Arbeitsbestand

`data/manifest.json` enthält SHA-256-Prüfsummen der mitgelieferten Eingaben. Es enthält keine absoluten lokalen Pfade. Die kleinen Datenausschnitte erlauben eine Ausführung ohne Zugriff auf die private Ordnerstruktur. Ein späterer Austausch gegen aktuellere Daten sollte als eigener, dokumentierter Analysestand erfolgen.
