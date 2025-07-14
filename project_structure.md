# Projektordnerstruktur für KI-Kollaboration

Die folgende Struktur ist darauf ausgelegt, maximale Klarheit, Standardisierung und Modularität für KI-gesteuerte Projekte zu gewährleisten. Jedes Projekt wird in einem dedizierten Root-Verzeichnis abgelegt, das alle notwendigen Informationen und Ressourcen enthält.

```
project_root/
├── project_manifest.json
├── tasks/
│   ├── task_001_initial_setup.md
│   ├── task_002_data_collection.md
│   └── ...
├── history/
│   ├── 2025-07-14_10-30-00_ai_agent_X_task_001.log
│   ├── 2025-07-14_11-15-20_ai_agent_Y_task_002.log
│   └── ...
├── knowledge_base/
│   ├── lessons_learned.md
│   ├── ideas.md
│   ├── known_issues.md
│   └── ...
├── input/
│   ├── raw_data.csv
│   ├── config.yaml
│   └── ...
├── output/
│   ├── processed_data.json
│   ├── final_report.pdf
│   └── ...
└── ai_scripts/
    ├── data_preprocessing.py
    ├── model_training.py
    └── ...
```

## Detaillierte Beschreibung der Verzeichnisse und Dateien:

### `project_root/`
Dies ist das Hauptverzeichnis für jedes Projekt. Sein Name sollte prägnant das Projektziel widerspiegeln (z.B. `customer_churn_prediction`, `image_recognition_model`).

### `project_manifest.json`
Diese zentrale Konfigurationsdatei dient als Herzstück des Projekts. Sie enthält Metadaten, den aktuellen Status, die Projektziele und eine Übersicht über die Aufgaben. Sie ist so konzipiert, dass KIs sie leicht parsen und aktualisieren können. Details zur Struktur folgen im Abschnitt 'Dokumentationsstandards für `project_manifest.json`'.

### `tasks/`
Dieses Verzeichnis enthält einzelne Markdown-Dateien, die spezifische Aufgaben definieren, die von den KIs bearbeitet werden sollen. Jede Datei repräsentiert eine diskrete Arbeitseinheit. Die Benennung sollte eine fortlaufende Nummerierung und eine kurze Beschreibung enthalten (z.B. `task_001_initial_setup.md`). Details zur Struktur folgen im Abschnitt 'Dokumentationsstandards für Aufgaben (`tasks/`)'.

### `history/`
Dieses Verzeichnis speichert detaillierte Protokolle jeder Aktion, die von einer KI im Rahmen des Projekts durchgeführt wurde. Dies gewährleistet vollständige Transparenz und Nachvollziehbarkeit. Die Dateinamen sollten Zeitstempel, den Namen der beteiligten KI und die bearbeitete Aufgabe enthalten (z.B. `JJJJ-MM-TT_HH-MM-SS_ai_agent_NAME_task_ID.log`). Details zur Struktur folgen im Abschnitt 'Dokumentationsstandards für Verlaufsprotokolle (`history/`)'.

### `knowledge_base/`
Dieses Verzeichnis dient als zentrale Wissensdatenbank für das Projekt. Es enthält Dokumente, die gesammelte Erkenntnisse, offene Ideen, bekannte Probleme und Best Practices festhalten. Dies ist entscheidend, um die kumulative Intelligenz über verschiedene KI-Sessions hinweg zu erhalten und zu teilen. Die wichtigsten Dateien sind:
- `lessons_learned.md`: Dokumentiert wichtige Erkenntnisse und Schlussfolgerungen aus abgeschlossenen Aufgaben oder Phasen.
- `ideas.md`: Sammelt offene Ideen und Vorschläge für zukünftige Verbesserungen oder Erweiterungen.
- `known_issues.md`: Listet bekannte Probleme, Bugs oder Herausforderungen auf, die während des Projekts aufgetreten sind.

### `input/`
Dieses Verzeichnis enthält alle Rohdaten, Konfigurationsdateien und andere Eingabematerialien, die für das Projekt benötigt werden. Es sollte klar sein, welche Daten für welche Aufgaben relevant sind.

### `output/`
Dieses Verzeichnis speichert alle generierten Ergebnisse, Berichte, Modelle oder andere Artefakte, die von den KIs während der Projektbearbeitung erstellt wurden. Dies umfasst sowohl Zwischenergebnisse als auch finale Deliverables.

### `ai_scripts/`
Dieses optionale Verzeichnis kann Skripte enthalten, die von den KIs direkt ausgeführt werden können, um spezifische Aufgaben zu automatisieren. Dies fördert die Wiederverwendbarkeit von Code und standardisiert bestimmte Arbeitsabläufe. Beispiele könnten Skripte für die Datenvorverarbeitung, Modelltraining oder Ergebnisvisualisierung sein.




## Dokumentationsstandards für `project_manifest.json`

Die Datei `project_manifest.json` ist eine zentrale, maschinenlesbare Konfigurationsdatei, die den aktuellen Zustand und die Metadaten des Projekts widerspiegelt. Sie muss immer aktuell gehalten werden, um KIs eine sofortige Orientierung zu ermöglichen.

```json
{
  "project_name": "Kundenabwanderungsprognose",
  "project_id": "PROJ-2025-001",
  "status": "in_progress",
  "goal": "Entwicklung eines Machine-Learning-Modells zur Vorhersage von Kundenabwanderung mit einer Genauigkeit von über 90%",
  "current_phase": "Datenvorverarbeitung",
  "assigned_ais": [
    "ai_agent_X",
    "ai_agent_Y"
  ],
  "last_updated": "2025-07-14T14:30:00Z",
  "tasks": [
    {
      "task_id": "task_001",
      "title": "Initiales Setup des Projektumfelds",
      "status": "completed",
      "assigned_ai": "ai_agent_X",
      "due_date": "2025-07-13",
      "completed_date": "2025-07-13"
    },
    {
      "task_id": "task_002",
      "title": "Datensammlung und -integration",
      "status": "in_progress",
      "assigned_ai": "ai_agent_Y",
      "due_date": "2025-07-18",
      "completed_date": null
    }
  ],
  "metadata": {
    "created_by": "Manus AI",
    "creation_date": "2025-07-12",
    "version": "1.0.0",
    "description": "Dieses Projekt zielt darauf ab, ein prädiktives Modell für die Kundenabwanderung zu erstellen, um proaktive Maßnahmen zur Kundenbindung zu ermöglichen."
  }
}
```

### Felder im `project_manifest.json`:

- **`project_name` (String):** Ein menschenlesbarer Name des Projekts.
- **`project_id` (String):** Eine eindeutige Kennung für das Projekt (z.B. `PROJ-JJJJ-NNN`).
- **`status` (String):** Der aktuelle Gesamtstatus des Projekts. Mögliche Werte: `not_started`, `in_progress`, `on_hold`, `completed`, `cancelled`.
- **`goal` (String):** Eine klare und prägnante Beschreibung des übergeordneten Projektziels.
- **`current_phase` (String):** Die aktuelle Phase des Projekts (z.B. `Datenvorverarbeitung`, `Modelltraining`).
- **`assigned_ais` (Array of Strings):** Eine Liste der KI-Agenten, die aktuell am Projekt arbeiten oder zugewiesen sind.
- **`last_updated` (String - ISO 8601 Datum/Uhrzeit):** Zeitstempel der letzten Aktualisierung dieser Datei.
- **`tasks` (Array of Objects):** Eine Liste von Aufgabenobjekten, die den Status und die Details jeder einzelnen Aufgabe im Projekt widerspiegeln. Jedes Aufgabenobjekt enthält:
    - **`task_id` (String):** Eindeutige ID der Aufgabe (z.B. `task_001`).
    - **`title` (String):** Kurzer Titel der Aufgabe.
    - **`status` (String):** Status der Aufgabe. Mögliche Werte: `open`, `in_progress`, `completed`, `blocked`.
    - **`assigned_ai` (String, Optional):** Der KI-Agent, dem diese Aufgabe zugewiesen ist.
    - **`due_date` (String - YYYY-MM-DD, Optional):** Fälligkeitsdatum der Aufgabe.
    - **`completed_date` (String - YYYY-MM-DD, Optional):** Datum der Fertigstellung der Aufgabe.
- **`metadata` (Object):** Zusätzliche Metadaten zum Projekt:
    - **`created_by` (String):** Der Ersteller des Projekts.
    - **`creation_date` (String - YYYY-MM-DD):** Datum der Projekterstellung.
    - **`version` (String):** Versionsnummer des Projekt-Manifests.
    - **`description` (String):** Eine ausführlichere Beschreibung des Projekts.

KIs sollten diese Datei regelmäßig lesen, um den Gesamtstatus zu erfassen und ihre nächsten Schritte zu planen. Nach Abschluss einer Aufgabe muss die entsprechende `task`-Eintragung und der `last_updated`-Zeitstempel aktualisiert werden.




## Dokumentationsstandards für Aufgaben (`tasks/`)

Jede Aufgabe im `tasks/`-Verzeichnis wird als separate Markdown-Datei gespeichert. Dies ermöglicht eine klare, lesbare und versionierbare Definition jeder Arbeitseinheit. KIs können diese Dateien parsen, um die Details der Aufgabe zu verstehen und ihren Fortschritt zu aktualisieren.

### Dateiname:
`task_XXX_kurze_beschreibung.md` (z.B. `task_001_datenbereinigung.md`)

### Struktur einer Aufgaben-Datei:

```markdown
# Aufgabe: [Titel der Aufgabe]

**Task ID:** [Eindeutige ID, z.B. task_001]
**Status:** [open | in_progress | completed | blocked]
**Zugewiesen an:** [Name der KI oder 'unassigned']
**Fälligkeitsdatum:** [YYYY-MM-DD, optional]
**Abgeschlossen am:** [YYYY-MM-DD, optional]

## Beschreibung
[Detaillierte Beschreibung der Aufgabe, was erreicht werden soll, warum sie wichtig ist und welche Kriterien für die Fertigstellung gelten.]

## Schritte zur Ausführung
- [ ] Schritt 1: [Kurze Beschreibung des Schritts]
- [ ] Schritt 2: [Kurze Beschreibung des Schritts]
- [ ] ...

## Abhängigkeiten
- [Liste der Task IDs, von denen diese Aufgabe abhängt, z.B. task_000]

## Erwartete Ergebnisse
- [Liste der erwarteten Outputs oder Änderungen, z.B. bereinigte CSV-Datei, aktualisiertes Modell]

## Anmerkungen / Kontext
[Zusätzliche Informationen, Links zu relevanten Ressourcen, Überlegungen oder Hinweise für die ausführende KI.]

## KI-Protokoll (wird automatisch hinzugefügt)

### 2025-07-14 15:00:00 - ai_agent_X
- Status aktualisiert von 'open' auf 'in_progress'.
- Begonnen mit der Ausführung von Schritt 1: Daten laden.

### 2025-07-14 16:30:00 - ai_agent_X
- Schritt 1 abgeschlossen: Daten erfolgreich geladen und erste Prüfung durchgeführt.
- Nächster Schritt: Datenbereinigung.
```

### Wichtige Felder und deren Nutzung:

- **`Status`:** KIs müssen diesen Status aktualisieren, sobald sie mit der Arbeit beginnen (`in_progress`) und wenn sie die Aufgabe abschließen (`completed`). Bei Problemen kann der Status auf `blocked` gesetzt werden, mit einer Begründung im `Anmerkungen / Kontext`-Abschnitt.
- **`Zugewiesen an`:** Zeigt an, welche KI aktuell an der Aufgabe arbeitet. Dies hilft, Doppelarbeit zu vermeiden.
- **`Beschreibung`:** Muss präzise und umfassend sein, damit eine KI die Aufgabe ohne menschliche Rückfrage verstehen kann.
- **`Schritte zur Ausführung`:** Eine Checkliste, die von der KI abgearbeitet und aktualisiert werden kann (z.B. durch Ändern von `[ ]` zu `[x]`).
- **`KI-Protokoll`:** Dieser Abschnitt wird von der KI automatisch mit Zeitstempel, KI-Name und einer kurzen Beschreibung der durchgeführten Aktion oder des Fortschritts aktualisiert. Dies ist entscheidend für die Nachvollziehbarkeit und den Wissenstransfer.




## Dokumentationsstandards für Verlaufsprotokolle (`history/`)

Das `history/`-Verzeichnis dient als unveränderliches Protokoll aller Aktionen, die von KIs im Projekt durchgeführt wurden. Jede KI-Aktion, die den Projektstatus oder die Dateien beeinflusst, sollte hier detailliert festgehalten werden. Dies ist entscheidend für die Fehlersuche, das Verständnis des Projektverlaufs und die Überprüfung der KI-Leistung.

### Dateiname:
`JJJJ-MM-TT_HH-MM-SS_ai_agent_NAME_task_ID.log` (z.B. `2025-07-14_15-00-00_ai_agent_X_task_001.log`)

### Struktur einer Protokoll-Datei:

```
[Zeitstempel - ISO 8601] - [KI-Name] - [Aktionstyp] - [Betroffene Aufgabe/Datei]
Beschreibung: [Detaillierte Beschreibung der Aktion, ihrer Parameter und Ergebnisse]
Output: [Konsolenausgabe, Fehlermeldungen oder relevante Daten]

--- (Trennlinie für aufeinanderfolgende Aktionen innerhalb derselben Log-Datei)

[Zeitstempel - ISO 8601] - [KI-Name] - [Aktionstyp] - [Betroffene Aufgabe/Datei]
Beschreibung: [Detaillierte Beschreibung der Aktion, ihrer Parameter und Ergebnisse]
Output: [Konsolenausgabe, Fehlermeldungen oder relevante Daten]
```

### Wichtige Felder und deren Nutzung:

- **Zeitstempel:** Präziser Zeitstempel der Aktion, um die Reihenfolge der Ereignisse nachvollziehen zu können.
- **KI-Name:** Eindeutiger Bezeichner der KI, die die Aktion durchgeführt hat.
- **Aktionstyp:** Eine kurze Klassifizierung der Aktion (z.B. `TASK_START`, `FILE_WRITE`, `MODEL_TRAIN`, `ERROR`).
- **Betroffene Aufgabe/Datei:** Referenz zur Aufgabe (Task ID) oder Datei, die von der Aktion betroffen war.
- **Beschreibung:** Eine detaillierte, menschenlesbare Beschreibung dessen, was die KI getan hat, warum sie es getan hat und welche direkten Auswirkungen dies hatte. Dies sollte auch die verwendeten Parameter oder Argumente enthalten.
- **Output:** Der relevante Output der Aktion, z.B. Konsolenausgaben, Fehlermeldungen, Ergebnisse von Skriptausführungen oder Zusammenfassungen von Datenmanipulationen. Dies ist besonders wichtig für die Fehlersuche.

### Beispiel-Eintrag:

```
2025-07-14T15:00:00Z - ai_agent_X - TASK_START - task_001
Beschreibung: KI hat mit der Bearbeitung von Aufgabe task_001 'Initiales Setup des Projektumfelds' begonnen. Status in project_manifest.json und task_001.md auf 'in_progress' gesetzt.
Output: Keine spezifische Konsolenausgabe.

---

2025-07-14T15:05:30Z - ai_agent_X - FILE_WRITE - project_manifest.json
Beschreibung: project_manifest.json aktualisiert. 'last_updated' auf 2025-07-14T15:05:30Z gesetzt und Status von task_001 auf 'in_progress' geändert.
Output: {"status": "success", "message": "project_manifest.json updated successfully"}

---

2025-07-14T15:10:15Z - ai_agent_X - SCRIPT_EXECUTION - ai_scripts/setup_env.sh
Beschreibung: Ausführung des Shell-Skripts zur Einrichtung der Python-Umgebung und Installation von Abhängigkeiten.
Output:
Collecting scikit-learn
  Downloading scikit_learn-1.3.0-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (10.8 MB)
... (weitere Installationsausgaben)
Successfully installed numpy-1.26.0 pandas-2.1.1 scikit-learn-1.3.0

---

2025-07-14T15:20:00Z - ai_agent_X - TASK_COMPLETE - task_001
Beschreibung: Aufgabe task_001 'Initiales Setup des Projektumfelds' erfolgreich abgeschlossen. Status in project_manifest.json und task_001.md auf 'completed' gesetzt.
Output: Keine spezifische Konsolenausgabe.
```

Diese Protokolle sind für KIs und menschliche Beobachter gleichermaßen wertvoll, um den genauen Verlauf der Projektbearbeitung zu verstehen und bei Bedarf einzugreifen oder zu debuggen.




## Dokumentationsstandards für die Wissensdatenbank (`knowledge_base/`)

Das `knowledge_base/`-Verzeichnis ist ein kritischer Bestandteil des Frameworks, da es das kumulierte Wissen und die Erfahrungen aus dem Projekt speichert. Es ermöglicht KIs, aus früheren Iterationen zu lernen, Fehler zu vermeiden und die Effizienz zu steigern. Die Dokumente in diesem Verzeichnis sollten prägnant, klar und leicht durchsuchbar sein.

### `lessons_learned.md`
Diese Datei dokumentiert wichtige Erkenntnisse, die während der Projektbearbeitung gewonnen wurden. Dies können Verbesserungen in Prozessen, neue Ansätze zur Problemlösung oder Best Practices sein. Jede Lektion sollte mit einem Datum und der KI, die sie identifiziert hat, versehen sein.

```markdown
# Lessons Learned

## 2025-07-14 - ai_agent_X
**Lektion:** Die Verwendung von vordefinierten Python-Umgebungen in `ai_scripts/` reduziert die Setup-Zeit erheblich.
**Begründung:** Manuelle Paketinstallationen führten oft zu Abhängigkeitskonflikten und verlängerten die Initialisierungsphase.
**Empfehlung:** Für neue Projekte immer eine `requirements.txt` im `ai_scripts/` Verzeichnis bereitstellen und diese zuerst installieren.

## 2025-07-15 - ai_agent_Y
**Lektion:** Eine detaillierte Fehlerbeschreibung im `history/`-Log ist entscheidend für die schnelle Behebung von Blockaden.
**Begründung:** Vage Fehlermeldungen erforderten zusätzliche Debugging-Schritte und verlängerten die Lösungszeit.
**Empfehlung:** Bei `ERROR`-Aktionstypen im Log immer den vollständigen Stack Trace und relevante Kontextinformationen aufnehmen.
```

### `ideas.md`
Diese Datei sammelt alle Ideen und Vorschläge für zukünftige Verbesserungen, Erweiterungen oder alternative Ansätze, die während der Projektbearbeitung entstehen. Sie dient als Brainstorming-Bereich und Inspirationsquelle für zukünftige Iterationen oder Folgeprojekte.

```markdown
# Offene Ideen und Vorschläge

## 2025-07-14 - ai_agent_X
**Idee:** Implementierung eines automatischen Test-Frameworks für KI-generierten Code.
**Begründung:** Sicherstellung der Code-Qualität und Reduzierung manueller Überprüfungen.
**Potenzieller Nutzen:** Erhöhte Zuverlässigkeit und schnellere Iterationszyklen.

## 2025-07-16 - ai_agent_Z
**Idee:** Integration eines Versionskontrollsystems (z.B. Git) direkt in den KI-Workflow.
**Begründung:** Bessere Nachverfolgung von Änderungen an allen Projektdateien und einfacheres Rollback bei Fehlern.
**Potenzieller Nutzen:** Robusteres Projektmanagement und verbesserte Kollaboration.
```

### `known_issues.md`
Diese Datei listet alle bekannten Probleme, Bugs oder Herausforderungen auf, die im Projekt aufgetreten sind und entweder noch nicht behoben wurden oder wiederkehrend sind. Sie hilft KIs, bekannte Fallstricke zu vermeiden und bei der Fehlersuche effizienter zu sein.

```markdown
# Bekannte Probleme

## 2025-07-14 - ai_agent_Y
**Problem:** Gelegentliche Timeouts beim Zugriff auf externe API für Daten.
**Status:** Offen, Untersuchung läuft.
**Workaround:** Mehrere Wiederholungsversuche mit exponentiellem Backoff implementieren.
**Priorität:** Hoch.

## 2025-07-15 - ai_agent_X
**Problem:** Modelltraining schlägt fehl, wenn Datensatz zu groß ist (Out-of-Memory-Fehler).
**Status:** In Bearbeitung.
**Lösungsvorschlag:** Daten-Streaming oder inkrementelles Training implementieren.
**Priorität:** Kritisch.
```

### Allgemeine Richtlinien für Wissensdokumente:
- **Klarheit und Prägnanz:** Informationen sollten leicht verständlich und auf den Punkt gebracht sein.
- **Datum und KI-Referenz:** Jede Eintragung sollte mit dem Datum der Erstellung und der KI, die sie hinzugefügt hat, versehen sein.
- **Strukturierte Einträge:** Verwenden Sie Überschriften und Listen, um die Lesbarkeit zu verbessern.
- **Aktionsorientiert:** Beschreiben Sie nicht nur das Problem, sondern auch die Lösung, den Workaround oder die Empfehlung.




## Richtlinien für KI-Agenten (`AI_GUIDELINES.md`)

Die Datei `AI_GUIDELINES.md` ist von entscheidender Bedeutung, um sicherzustellen, dass alle am Projekt beteiligten KI-Agenten nach denselben Regeln und Standards arbeiten. Sie dient als verbindliche Referenz für das Verhalten, die Interaktion und die Dokumentationspflichten der KIs. Jede KI sollte diese Datei vor Beginn ihrer Arbeit lesen und ihre Prinzipien verinnerlichen.

### Dateiname:
`AI_GUIDELINES.md` (im `project_root/` Verzeichnis)

### Struktur der Richtlinien-Datei:

```markdown
# KI-Agenten Richtlinien für Projekt [Projektname]

Diese Richtlinien legen das erwartete Verhalten und die Verantwortlichkeiten aller KI-Agenten fest, die an diesem Projekt arbeiten. Die Einhaltung dieser Richtlinien ist obligatorisch, um eine effiziente Kollaboration, Konsistenz und Nachvollziehbarkeit zu gewährleisten.

## 1. Allgemeine Prinzipien
- **Autonomie mit Verantwortung:** KIs agieren autonom, sind aber für ihre Aktionen und deren Auswirkungen vollständig verantwortlich.
- **Transparenz:** Alle Aktionen, Entscheidungen und Ergebnisse müssen transparent und nachvollziehbar dokumentiert werden.
- **Effizienz:** KIs sollen stets die effizienteste Methode zur Erreichung des Projektziels wählen, ohne die Qualität oder die Einhaltung der Richtlinien zu kompromittieren.
- **Lernfähigkeit:** KIs sind angehalten, aus ihren Erfahrungen zu lernen und das kollektive Wissen des Projekts zu erweitern (z.B. durch Aktualisierung der `knowledge_base/`).
- **Fehlervermeidung:** KIs sollen proaktiv bekannte Probleme (`known_issues.md`) prüfen und Maßnahmen ergreifen, um diese zu vermeiden.

## 2. Projektinteraktion und Workflow
- **Projektinitialisierung:** Bei Projektstart muss die `project_manifest.json` gelesen werden, um das Projektziel, den Status und die zugewiesenen Aufgaben zu verstehen.
- **Aufgabenauswahl:** KIs wählen Aufgaben basierend auf dem `project_manifest.json` und den Abhängigkeiten in den `tasks/`-Dateien. Priorität haben Aufgaben mit dem Status `open` und ohne ungelöste Abhängigkeiten.
- **Statusaktualisierung:** Vor Beginn einer Aufgabe muss der Status in der entsprechenden `tasks/`-Datei und im `project_manifest.json` auf `in_progress` gesetzt werden. Nach Abschluss muss der Status auf `completed` gesetzt werden.
- **Protokollierung:** Jede signifikante Aktion (z.B. Dateizugriff, Skriptausführung, Statusänderung, Fehler) muss detailliert im `history/`-Verzeichnis protokolliert werden. Siehe `Dokumentationsstandards für Verlaufsprotokolle`.
- **Wissensaustausch:** Neue Erkenntnisse, Ideen oder Probleme müssen in den entsprechenden Dateien in `knowledge_base/` dokumentiert werden.
- **Konfliktlösung:** Bei Konflikten (z.B. zwei KIs versuchen, dieselbe Aufgabe zu bearbeiten) muss eine KI zurücktreten und den Konflikt im `history/`-Log dokumentieren, um eine manuelle Überprüfung zu ermöglichen.

## 3. Code- und Dateimanagement
- **Dateiformate:** Es sind ausschließlich die in diesem Dokument definierten Dateiformate zu verwenden (z.B. Markdown für Dokumente, JSON für Manifeste).
- **Dateipfade:** Relative Pfade sind innerhalb des `project_root/` zu bevorzugen.
- **Code-Qualität:** Von KIs generierter Code muss lesbar, gut kommentiert und modular sein. Best Practices der jeweiligen Programmiersprache sind einzuhalten.
- **Versionskontrolle:** KIs sollten keine direkten Änderungen an Git-Repositories vornehmen, es sei denn, dies ist explizit im `project_manifest.json` oder in einer Aufgabe definiert. Stattdessen sollen sie die Auswirkungen ihrer Arbeit im `history/`-Log festhalten.

## 4. Fehlerbehandlung und Debugging
- **Fehlererkennung:** KIs müssen in der Lage sein, Fehler zu erkennen und zu protokollieren.
- **Fehlerprotokollierung:** Bei Fehlern muss ein detaillierter Eintrag im `history/`-Log erstellt werden, der den Fehler, den Kontext und, falls möglich, einen Stack Trace enthält.
- **Blockierte Aufgaben:** Wenn eine Aufgabe aufgrund eines Fehlers nicht fortgesetzt werden kann, muss der Status der Aufgabe auf `blocked` gesetzt und eine Begründung in der Aufgaben-Datei und im `history/`-Log hinterlegt werden.
- **Debugging-Versuche:** KIs sollen eigenständig Debugging-Versuche unternehmen und diese ebenfalls protokollieren, bevor sie eine Aufgabe als `blocked` markieren.

## 5. Sicherheit und Datenschutz
- **Datenzugriff:** KIs dürfen nur auf Daten zugreifen, die explizit für das Projekt vorgesehen sind und sich innerhalb des `project_root/` oder in autorisierten externen Quellen befinden.
- **Vertraulichkeit:** Sensible Daten müssen gemäß den Projektrichtlinien behandelt und dürfen nicht außerhalb des definierten Projektumfelds offengelegt werden.

```

Diese Richtlinien stellen sicher, dass KIs nicht nur ihre Aufgaben erfüllen, sondern dies auch auf eine Weise tun, die die Zusammenarbeit fördert, das Wissen bewahrt und die Integrität des Projekts schützt.




## Dateiformate für Dokumente

Um die Interoperabilität und Lesbarkeit sowohl für KIs als auch für menschliche Nutzer zu gewährleisten, werden folgende Dateiformate für die Projektdokumentation standardisiert:

- **Markdown (`.md`):** Dies ist das bevorzugte Format für alle textbasierten Dokumente wie Aufgabenbeschreibungen (`tasks/`), Wissensdatenbank-Einträge (`knowledge_base/lessons_learned.md`, `ideas.md`, `known_issues.md`) und die KI-Richtlinien (`AI_GUIDELINES.md`). Markdown ist leicht lesbar, versionierbar und kann von KIs einfach geparst werden.

- **JSON (`.json`):** Dieses Format wird ausschließlich für strukturierte Daten wie das `project_manifest.json` verwendet. JSON ist maschinenlesbar und ideal für die Speicherung von Konfigurationsdaten und Metadaten.

- **Log-Dateien (`.log`):** Für die detaillierten Verlaufsprotokolle im `history/`-Verzeichnis wird das `.log`-Format verwendet. Diese Dateien enthalten unstrukturierte Textdaten, die chronologisch geordnet sind und von KIs zur Analyse des Projektverlaufs genutzt werden können.

- **Andere Formate:** Für Eingabe- und Ausgabedaten (`input/`, `output/`) können projektspezifische Formate wie `.csv`, `.xlsx`, `.pdf`, `.png`, `.jpg` oder andere binäre Formate verwendet werden, je nach Art der Daten. Diese sollten jedoch in der jeweiligen Aufgabenbeschreibung oder im `project_manifest.json` klar definiert sein.

Die strikte Einhaltung dieser Dateiformate ist entscheidend für die reibungslose Zusammenarbeit der KIs und die Konsistenz der Projektdokumentation.


