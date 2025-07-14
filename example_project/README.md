# Beispielprojekt für KI-Kollaboration

Dieses Projekt demonstriert ein strukturiertes Framework, das darauf ausgelegt ist, die effiziente Zusammenarbeit mehrerer KI-Agenten an einem gemeinsamen Projekt zu ermöglichen. Es bietet eine klare Ordnerstruktur, standardisierte Dokumentationsformate und Mechanismen zur Fortschrittsverfolgung und zum Wissensaustausch.

## Projektstruktur

Das Projekt folgt der im `project_structure.md` definierten Ordnerstruktur:

```
example_project/
├── project_manifest.json       # Zentrale Projektkonfiguration und Status
├── tasks/                      # Aufgabenbeschreibungen für KIs
│   └── task_001_setup.md
│   └── task_template.md
├── history/                    # Protokolle aller KI-Aktionen
│   └── log_template.log
├── knowledge_base/             # Gesammeltes Wissen, Ideen und bekannte Probleme
│   ├── lessons_learned.md
│   ├── ideas.md
│   └── known_issues.md
├── input/                      # Eingabedaten für das Projekt
├── output/                     # Generierte Ergebnisse und Artefakte
├── ai_scripts/                 # Optionale Skripte für KIs
└── AI_GUIDELINES.md            # Richtlinien für KI-Agenten
```

## Zweck

Der Hauptzweck dieses Beispielprojekts ist es, zu veranschaulichen, wie:

1.  **Klarheit:** Eine KI das Projektziel und den aktuellen Status sofort erfassen kann.
2.  **Automatisierung:** KIs Aufgaben selbstständig identifizieren, bearbeiten und ihren Fortschritt dokumentieren können.
3.  **Wissensaustausch:** Erkenntnisse, Probleme und Ideen über verschiedene KI-Sessions hinweg geteilt und genutzt werden.
4.  **Nachvollziehbarkeit:** Jede Aktion einer KI protokolliert wird, um den Projektverlauf transparent zu machen.

## Wie eine KI mit diesem Projekt interagiert

Eine KI, die mit diesem Projekt arbeitet, sollte die folgenden Schritte befolgen:

1.  **`project_manifest.json` lesen:** Zuerst die zentrale Konfigurationsdatei lesen, um den Gesamtstatus, das Ziel und die Liste der Aufgaben zu verstehen.
2.  **`AI_GUIDELINES.md` prüfen:** Die Richtlinien für KI-Agenten lesen, um das erwartete Verhalten und die Dokumentationsstandards zu verstehen.
3.  **Aufgaben identifizieren:** Im `tasks/`-Verzeichnis nach Aufgaben mit dem Status `open` suchen, die keine ungelösten Abhängigkeiten haben.
4.  **Aufgabe bearbeiten:**
    *   Den Status der ausgewählten Aufgabe in der entsprechenden `tasks/`-Datei und im `project_manifest.json` auf `in_progress` setzen.
    *   Die in der Aufgabenbeschreibung definierten Schritte ausführen.
    *   Jede signifikante Aktion im `history/`-Verzeichnis protokollieren.
    *   Neue Erkenntnisse, Ideen oder Probleme in den entsprechenden `knowledge_base/`-Dateien dokumentieren.
    *   Nach Abschluss der Aufgabe den Status in der `tasks/`-Datei und im `project_manifest.json` auf `completed` setzen.
5.  **Wiederholen:** Den Prozess wiederholen, bis alle Aufgaben abgeschlossen sind oder das Projektziel erreicht ist.

## Starten des Projekts (für eine KI)

Eine KI kann das Projekt starten, indem sie das `project_manifest.json` liest und die erste offene Aufgabe (`task_001_setup.md`) bearbeitet. Es wird empfohlen, zuerst die `AI_GUIDELINES.md` zu lesen.

Dieses Framework ist darauf ausgelegt, eine robuste und effiziente Umgebung für die KI-gesteuerte Projektentwicklung zu schaffen.


