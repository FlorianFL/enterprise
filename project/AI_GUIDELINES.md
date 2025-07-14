# KI-Agenten Richtlinien für Projekt Beispielprojekt KI-Kollaboration

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




## 6. Kill-Switch für Projektunterbrechung

Um die Kontrolle über das Projekt zu gewährleisten und die KIs bei Bedarf sofort anzuhalten, wurde ein "Kill-Switch" im `project_manifest.json` implementiert.

-   **`kill_switch` Feld:** Im `project_manifest.json` gibt es ein Feld namens `"kill_switch": false`. Wenn dieses Feld vom Nutzer auf `true` gesetzt wird, müssen alle KIs ihre aktuelle Arbeit sofort einstellen und dürfen keine weiteren Aktionen im Projekt durchführen.

-   **Regelmäßige Prüfung:** KIs müssen vor jeder neuen Aktion (z.B. vor dem Start einer Aufgabe, vor dem Schreiben in eine Datei) den Status des `kill_switch` im `project_manifest.json` prüfen. Ist der `kill_switch` auf `true` gesetzt, muss die KI ihre Ausführung beenden und darf keine weiteren Änderungen am Projekt vornehmen.

-   **Protokollierung des Stopps:** Wenn eine KI aufgrund des `kill_switch` ihre Arbeit einstellt, sollte sie dies, falls möglich, im `history/`-Log protokollieren (z.B. `AI_Agent_X - PROJECT_STOP - Kill-Switch aktiviert`).

Dieser Mechanismus ermöglicht es dem Nutzer, die KI-Aktivitäten jederzeit zu unterbrechen und die Kontrolle über das Projekt zu behalten.


