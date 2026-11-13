# Ansätze, Unterschiede und erhaltene Exploration

Die Reihenfolge folgt dem ursprünglichen Arbeitsweg. Die Varianten werden nicht zu einer einzigen vermeintlich optimalen Darstellung zusammengezogen.

| Ansatz | Sichtbare Information | Was dabei verloren geht oder zu beachten ist |
|---|---|---|
| Erst- und Zweitstimmen pro Partei | Unterschiede zwischen beiden Stimmenarten, ergänzt um die Verteilung der Gemeinden | Getrennte Quartilgrenzen; gleiche Farbe ist nicht derselbe Prozentwert |
| Bivariate Quartilkarte | Kombination zweier relativ hoher oder niedriger Parteianteile | Keine direkte Darstellung des Vorsprungs; andere Parteien nur indirekt enthalten |
| Kontinuierliches log(CDU/Grüne) | Richtung und Stärke des Stimmenverhältnisses | Der gemeinsame Anteil beider Parteien fehlt; Farben sättigen außerhalb der gewählten Quantile |
| Kategorisiertes Verhältnis | Direkt lesbare Verhältnisbereiche | Unterschiede innerhalb der Klassen verschwinden; ursprüngliche asymmetrische Klassen bleiben erkennbar |
| Ternärplot Grüne/CDU/Rest | Geschlossene Zusammensetzung, gemeinsame Stärke und Verhältnis | Rest bündelt unterschiedliche Parteien; jede Gemeinde erhält dasselbe visuelle Gewicht |
| Stärkste Partei je Gemeinde | Räumliche Orientierung | Knappe Ergebnisse und übrige Anteile verschwinden; Kartenfläche ist keine Stimmenzahl |
| Globales Moran I für R und log(R) | Räumliche Ähnlichkeit unter einer definierten Nachbarschaft | Abhängig von Transformation und Gewichten; kein Erklärungsmodell |
| LISA, lokal und BH-korrigiert | Lokale Cluster und Ausreißer als explorative Hinweise | Viele Tests, räumliche Abhängigkeit und eingeschränkte Briefwahlzuordnung |

## Was sich gegenüber dem Original geändert hat

Die beiden BW-Notebooks waren bis auf den Geometriepfad identisch. Es bleibt eine Fassung; die darin enthaltenen Analyseansätze bleiben erhalten. Die zweite identische Wahldatei und Notebook-Checkpoints entfallen. Die CSV zur repräsentativen Wahlstatistik 2021 war in der Analyse unbenutzt und wird nicht als vermeintlich ausgewerteter Datensatz mitgeliefert.

Die Rohdaten des Original-Snapshots bleiben erhalten. Sie werden nicht stillschweigend durch das spätere Endergebnis ersetzt. Ein Quellenmanifest hält die verwendeten Dateien mit Prüfsummen fest.

Die ursprüngliche Großstadtaggregation summierte überlappende Gebietsebenen. Der korrigierte Weg summiert nur passende, nicht überlappende Einträge. Eine Tabelle im Notebook stellt die alten und korrigierten absoluten Zahlen gegenüber. Diese Tabelle dokumentiert einen verworfenen Rechenweg; sie empfiehlt ihn nicht als Alternative.

Die Landeszeile wurde ursprünglich mit `skiprows=[1]` entfernt. Sie wird nun zur Kontrolle verwendet. Gemeindeergebnisse werden nicht auf die Landessumme hochgerechnet: nicht gemeindescharf zuordenbare Briefwahl bleibt als Differenz sichtbar.

AGS werden durchgehend als Text verarbeitet; der Geometrie-Join verlangt eindeutige Schlüssel und vollständige Treffer. Die Geometriegrundlage bleibt im ursprünglichen Stand. Nur der benötigte BW-Ausschnitt wird mitgeliefert.


Das kategorisierte Verhältnis enthält eine korrigierte Legendenbeschriftung. Im Ternärplot werden die komponentenweisen Mediane explizit auf Summe 1 normiert; die Markierung ist weder ein Landesergebnis noch ein multivariater Median.

Die räumliche Statistik zeigt nun beide Eingangsgrößen R und log(R). Dadurch bleibt der ursprüngliche Rechenansatz sichtbar und die fehlerhafte Zuordnung von Rechnung und Titel ist behoben. Zufallsstart, Permutationen und Inselbehandlung sind festgelegt. Die ursprüngliche lokale Signifikanzschwelle steht neben einer BH-Sensitivitätsansicht.

## Gestalterischer Zusammenhang

Die dunklen Hintergründe, Grün-/Ockervergleiche, Parteifarben, Barcodes, Regierungsbezirks-Inserts und die verschiedenen Kartenlayouts sind erhalten. Der Code für die Abbildungen bleibt im Notebook sichtbar. Technische Datenprüfungen sind in ein kleines Hilfsmodul ausgelagert; eine neue allgemeine Kartenbibliothek ist nicht erforderlich.

Kurze Markdown-Abschnitte erklären die Fragen und Grenzen der einzelnen Schritte. Sie schreiben keine nachträgliche lineare Erfolgsgeschichte: Alternativen und Einschränkungen bleiben sichtbar.
