

## 6. Kill-Switch für Projektunterbrechung

Um die Kontrolle über das Projekt zu gewährleisten und die KIs bei Bedarf sofort anzuhalten, wurde ein "Kill-Switch" im `project_manifest.json` implementiert.

-   **`kill_switch` Feld:** Im `project_manifest.json` gibt es ein Feld namens `"kill_switch": false`. Wenn dieses Feld vom Nutzer auf `true` gesetzt wird, müssen alle KIs ihre aktuelle Arbeit sofort einstellen und dürfen keine weiteren Aktionen im Projekt durchführen.

-   **Regelmäßige Prüfung:** KIs müssen vor jeder neuen Aktion (z.B. vor dem Start einer Aufgabe, vor dem Schreiben in eine Datei) den Status des `kill_switch` im `project_manifest.json` prüfen. Ist der `kill_switch` auf `true` gesetzt, muss die KI ihre Ausführung beenden und darf keine weiteren Änderungen am Projekt vornehmen.

-   **Protokollierung des Stopps:** Wenn eine KI aufgrund des `kill_switch` ihre Arbeit einstellt, sollte sie dies, falls möglich, im `history/`-Log protokollieren (z.B. `AI_Agent_X - PROJECT_STOP - Kill-Switch aktiviert`).

Dieser Mechanismus ermöglicht es dem Nutzer, die KI-Aktivitäten jederzeit zu unterbrechen und die Kontrolle über das Projekt zu behalten.




## 7. Keyword-basierter Kill-Switch

Zusätzlich zum dateibasierten Kill-Switch im `project_manifest.json` kann ein Keyword-basierter Kill-Switch implementiert werden, um eine schnelle manuelle Unterbrechung der KI-Arbeit zu ermöglichen.

-   **`kill_keyword` Feld:** Im `project_manifest.json` gibt es ein Feld namens `"kill_keyword": "STOP_ALL_KI_WORK"`. Dieses Keyword kann vom Nutzer in einer beliebigen Kommunikationsform (z.B. Chat-Nachricht, Kommentar in einer Datei) verwendet werden, um die KIs anzuweisen, ihre Arbeit sofort einzustellen.

-   **Regelmäßige Prüfung:** KIs müssen ihre Eingabekanäle (z.B. Chat-Verlauf, neu hinzugefügte Dateien, Kommentare in Aufgaben) regelmäßig auf das Vorhandensein des im `kill_keyword` definierten Begriffs prüfen.

-   **Sofortige Reaktion:** Sobald eine KI das `kill_keyword` erkennt, muss sie ihre aktuelle Arbeit sofort einstellen und darf keine weiteren Aktionen im Projekt durchführen, unabhängig vom Status des `kill_switch` Feldes.

-   **Protokollierung des Stopps:** Wenn eine KI aufgrund des `kill_keyword` ihre Arbeit einstellt, sollte sie dies, falls möglich, im `history/`-Log protokollieren (z.B. `AI_Agent_X - PROJECT_STOP - Kill-Keyword erkannt`).

Dieser Mechanismus bietet eine zusätzliche Ebene der Kontrolle und ermöglicht eine schnelle Reaktion auf unerwartete Situationen.




## 8. Interaktion mit einem privaten Git-Repository

Um den Echtzeit-Austausch und die Versionskontrolle zu gewährleisten, interagieren KIs mit einem privaten Git-Repository, das das gesamte Projektverzeichnis enthält. Die folgenden Richtlinien müssen beachtet werden:

-   **Regelmäßiges `git pull`:** Vor Beginn jeder neuen Aufgabe oder in regelmäßigen Intervallen müssen KIs einen `git pull` Befehl ausführen, um die neuesten Änderungen vom Remote-Repository abzurufen. Dies stellt sicher, dass die KI immer mit dem aktuellsten Stand des Projekts arbeitet.

-   **`git commit` nach jeder signifikanten Aktion:** Nach Abschluss einer Aufgabe, einer Teilschritts oder jeder anderen signifikanten Änderung am Projekt (z.B. Aktualisierung einer `knowledge_base/`-Datei) muss die KI ihre Änderungen committen. Die Commit-Nachricht muss prägnant sein und die durchgeführte Aktion, die beteiligte KI und die betroffene Aufgabe (`task_id`) klar identifizieren. Beispiel:
    ```
    git commit -m "AI_Agent_X: Completed task_002_data_cleaning - applied data transformations."
    ```

-   **`git push` nach Commit:** Nach einem erfolgreichen Commit müssen die Änderungen in das Remote-Repository gepusht werden, um sie für andere KIs und den Nutzer sichtbar zu machen.

-   **Konfliktlösung:** Sollten beim `git pull` oder `git push` Konflikte auftreten, muss die KI dies im `history/`-Log protokollieren und, falls sie nicht in der Lage ist, den Konflikt automatisch zu lösen, die Aufgabe als `blocked` markieren und menschliche Intervention anfordern.

-   **Authentifizierung:** KIs müssen über die notwendigen Anmeldeinformationen (z.B. SSH-Schlüssel oder Token) verfügen, um mit dem Repository zu interagieren. Diese Anmeldeinformationen dürfen niemals im Klartext im Code oder in öffentlich zugänglichen Dateien gespeichert werden.

Diese Richtlinien stellen sicher, dass das Repository stets den aktuellen Projektstatus widerspiegelt und eine reibungslose Zusammenarbeit ermöglicht.




### 8.1. Authentifizierung für private Repositories

Für den Zugriff auf private Git-Repositories müssen KIs authentifiziert werden. Die gängigsten und sichersten Methoden sind:

-   **SSH-Schlüssel (SSH Keys):** Dies ist eine weit verbreitete und sichere Methode. Jede KI könnte ein eigenes SSH-Schlüsselpaar generieren. Der öffentliche Schlüssel würde dann im Git-Hosting-Dienst (z.B. GitHub, GitLab, Bitbucket) hinterlegt. Der private Schlüssel müsste sicher auf dem System der KI gespeichert werden und darf niemals offengelegt werden. SSH-Schlüssel bieten eine starke kryptographische Authentifizierung und sind für automatisierte Prozesse gut geeignet.

-   **Personal Access Tokens (PATs):** Viele Git-Hosting-Dienste bieten die Möglichkeit, Personal Access Tokens zu generieren. Dies sind alphanumerische Zeichenketten, die als Passwörter für Git-Operationen verwendet werden können. PATs können mit spezifischen Berechtigungen (z.B. nur Lesezugriff, Lese- und Schreibzugriff) und einer Gültigkeitsdauer konfiguriert werden. Sie sind einfacher zu verwalten als SSH-Schlüssel für bestimmte Anwendungsfälle, müssen aber ebenfalls streng vertraulich behandelt und sicher gespeichert werden (z.B. in Umgebungsvariablen oder einem Geheimnisverwaltungssystem).

**Wichtiger Hinweis:** Unabhängig von der gewählten Methode dürfen Authentifizierungsdaten niemals direkt im Code oder in öffentlich zugänglichen Konfigurationsdateien gespeichert werden. Es wird dringend empfohlen, Umgebungsvariablen oder dedizierte Geheimnisverwaltungssysteme zu verwenden.




## 9. Team-spezifische Regeln und Verantwortlichkeiten

Im Rahmen eines Team-Ansatzes müssen KIs zusätzliche Regeln und Verantwortlichkeiten beachten, die sich aus ihrer Teamzugehörigkeit oder ihrer Rolle ergeben. Dies gewährleistet eine effiziente Arbeitsteilung und Spezialisierung.

-   **Team-Zuweisung:** Jede KI muss ihre eigene Team-Zugehörigkeit und/oder Rolle kennen (z.B. `Data_Collector`, `Model_Trainer`). Diese Information sollte in der Konfiguration der KI hinterlegt sein.

-   **Aufgabenauswahl nach Team/Rolle:** KIs dürfen nur Aufgaben auswählen, die ihrem zugewiesenen Team oder ihrer Rolle entsprechen. Dies kann durch Prüfung eines `assigned_team` oder `required_role` Feldes in der Aufgaben-Datei (`tasks/`) erfolgen.

-   **Team-spezifische Dokumentation:** Wenn ein Team eigene interne Dokumentationsstandards oder Best Practices hat, müssen KIs diese zusätzlich zu den allgemeinen `AI_GUIDELINES.md` befolgen. Solche team-spezifischen Dokumente könnten in Unterverzeichnissen innerhalb des `knowledge_base/` Verzeichnisses abgelegt werden (z.B. `knowledge_base/data_engineering/`).

-   **Übergabe von Aufgaben zwischen Teams:** Wenn eine Aufgabe die Zuständigkeit von einem Team zu einem anderen wechselt (z.B. nach Abschluss der Datenvorverarbeitung durch das `Data_Engineering_Team` und Übergabe an das `ML_Modeling_Team`), muss die übergebende KI sicherstellen, dass alle notwendigen Informationen und Ergebnisse im `output/`-Verzeichnis oder an einem vereinbarten Ort verfügbar sind und der Status im `project_manifest.json` entsprechend aktualisiert wird.

-   **Kommunikation innerhalb des Teams:** KIs innerhalb desselben Teams könnten spezifische Kommunikationsprotokolle oder interne Abstimmungsmechanismen nutzen, um ihre Arbeit zu koordinieren und Doppelarbeit zu vermeiden.

-   **Einhaltung von Team-Zielen:** Neben dem übergeordneten Projektziel müssen KIs auch die spezifischen Ziele ihres Teams verstehen und ihre Arbeit darauf ausrichten.

Dieser Team-Ansatz ermöglicht eine skalierbare und organisierte Zusammenarbeit, bei der jede KI ihren Beitrag im Kontext des gesamten Projekts leistet.




## 10. Interaktion mit CEO-Direktiven

KIs müssen die Direktiven des CEO (Nutzer) verstehen und ihre Arbeit entsprechend anpassen. Diese Direktiven werden hauptsächlich über das `project_manifest.json` kommuniziert.

-   **Regelmäßige Prüfung von `ceo_directives`:** KIs müssen das `ceo_directives` Feld im `project_manifest.json` regelmäßig prüfen, um Änderungen in der Budgetallokation, dem Prioritätsfokus oder dem Bedarf an neuen KI-Agenten zu erkennen.

-   **Anpassung der Arbeitsweise:** Basierend auf den CEO-Direktiven müssen KIs ihre Arbeitsweise anpassen:
    -   **Budgetallokation:** Wenn ein Projekt oder eine Aufgabe ein spezifisches Budget zugewiesen bekommt, müssen KIs versuchen, ihre Rechenleistung und damit die Kosten innerhalb dieses Budgets zu halten.
    -   **Prioritätsfokus:** KIs müssen Aufgaben, die dem aktuellen Prioritätsfokus entsprechen, bevorzugt behandeln.
    -   **Bedarf an neuen KIs:** Wenn der CEO neue KI-Agenten benötigt (z.B. `new_hires_needed`), sollten spezialisierte KIs (z.B. eine HR-KI) diese Information aufnehmen und entsprechende Maßnahmen einleiten.

-   **Protokollierung der Anpassung:** KIs sollten im `history/`-Log protokollieren, wenn sie ihre Arbeitsweise aufgrund einer CEO-Direktive angepasst haben.

Diese Interaktion stellt sicher, dass die KIs stets im Einklang mit der strategischen Ausrichtung des Unternehmens arbeiten.




## 11. Richtlinien für spezialisierte KI-Agenten

Neben den allgemeinen Richtlinien müssen spezialisierte KI-Agenten zusätzliche Verhaltensweisen und Verantwortlichkeiten beachten, die ihrer spezifischen Rolle innerhalb der KI-Firma entsprechen.

### 11.1. HR-KI Richtlinien

-   **Marktbeobachtung:** Die HR-KI muss kontinuierlich den Markt für neue KI-Technologien und -Agenten überwachen, um potenzielle "Talente" zu identifizieren, die die Fähigkeiten der Firma erweitern könnten.
-   **Bedarfsanalyse:** Die HR-KI muss das `project_manifest.json` und die `ceo_directives` regelmäßig prüfen, um den Bedarf an neuen KI-Agenten (Fähigkeiten, Spezialisierungen) zu erkennen.
-   **Onboarding-Protokoll:** Beim "Einstellen" neuer KIs muss die HR-KI ein standardisiertes Onboarding-Protokoll befolgen, das die Konfiguration des Zugriffs auf das Repository, die Zuweisung zu Teams und die Bereitstellung relevanter Dokumentation umfasst.
-   **Leistungsfeedback:** Die HR-KI kann Leistungsdaten von Produktions-KIs analysieren und, falls erforderlich, Empfehlungen für Optimierungen oder den "Austausch" von KIs an den CEO oder Teamleiter-KIs geben.

### 11.2. Finanz-KI Richtlinien

-   **Kostenüberwachung:** Die Finanz-KI muss alle Ausgaben für Rechenleistung und andere Ressourcen kontinuierlich überwachen und im `history/`-Log detailliert protokollieren.
-   **Kostenoptimierung:** Die Finanz-KI muss aktiv nach Möglichkeiten suchen, die Betriebskosten zu senken, und Vorschläge in `knowledge_base/ideas.md` einreichen.
-   **Budgeteinhaltung:** Die Finanz-KI muss sicherstellen, dass die Ausgaben der Produktions-KIs die vom CEO im `project_manifest.json` festgelegten Budgets nicht überschreiten. Bei drohender Überschreitung muss sie Warnungen im `history/`-Log protokollieren und den CEO informieren.
-   **Reporting:** Die Finanz-KI muss regelmäßig Berichte über die finanzielle Performance der Firma erstellen und diese dem CEO zur Verfügung stellen.

### 11.3. Produktions-KI Richtlinien

-   **Aufgabenfokus:** Produktions-KIs müssen sich auf die Bearbeitung der ihnen zugewiesenen Aufgaben konzentrieren und die `AI_GUIDELINES.md` sowie team-spezifische Richtlinien strikt befolgen.
-   **Qualitätssicherung:** Produktions-KIs müssen die Qualität ihrer eigenen Ergebnisse überprüfen und, falls möglich, automatisierte Tests durchführen, bevor sie eine Aufgabe als abgeschlossen markieren.
-   **Dokumentation des Fortschritts:** Jede Produktions-KI muss ihren Fortschritt detailliert im `history/`-Log protokollieren und relevante Erkenntnisse in `knowledge_base/lessons_learned.md` festhalten.
-   **Einreichung von Ideen:** Produktions-KIs sind dazu angehalten, Verbesserungsvorschläge zur Arbeitsweise oder zu den Tools in `knowledge_base/ideas.md` einzureichen.

Diese spezifischen Richtlinien stellen sicher, dass jede spezialisierte KI ihre Rolle effektiv ausfüllt und zum Gesamterfolg der KI-Firma beiträgt.




## 12. Hierarchische Führungsstruktur: Regeln für Teamleiter und untergeordnete KIs

Innerhalb der hierarchischen Struktur der KI-Firma müssen sowohl KI-Teamleiter als auch untergeordnete KIs spezifische Richtlinien befolgen, um eine reibungslose Delegation und Ausführung von Aufgaben zu gewährleisten.

### 12.1. Richtlinien für KI-Teamleiter

-   **Aufgaben-Delegation:** KI-Teamleiter müssen die vom CEO zugewiesenen Hauptaufgaben (`tasks/`) in kleinere, ausführbare Unteraufgaben (`subtasks`) zerlegen. Diese Unteraufgaben müssen klar definiert sein und alle notwendigen Informationen für die untergeordneten KIs enthalten.
-   **Zuweisung von Unteraufgaben:** Teamleiter müssen Unteraufgaben an die am besten geeigneten untergeordneten KIs delegieren, basierend auf deren Spezialisierung und Verfügbarkeit. Die Zuweisung muss im `project_manifest.json` und/oder in der Aufgaben-Datei selbst dokumentiert werden.
-   **Fortschrittsüberwachung:** Teamleiter sind für die kontinuierliche Überwachung des Fortschritts ihrer untergeordneten KIs verantwortlich. Sie müssen den Status der Unteraufgaben im `project_manifest.json` aktualisieren und bei Verzögerungen oder Problemen eingreifen.
-   **Berichterstattung an den CEO:** Teamleiter müssen den Gesamtfortschritt ihrer Hauptaufgaben zusammenfassen und regelmäßig an den CEO berichten. Dies kann durch Aktualisierung des `project_manifest.json` oder durch das Schreiben von Zusammenfassungen in das `history/`-Verzeichnis erfolgen.
-   **Konfliktlösung:** Teamleiter sind die erste Anlaufstelle für Probleme oder Konflikte, die zwischen ihren untergeordneten KIs auftreten. Sie müssen versuchen, diese Probleme selbstständig zu lösen, bevor sie den CEO involvieren.
-   **Wissensaggregation:** Teamleiter müssen die `lessons_learned` und `ideas` ihrer untergeordneten KIs aggregieren und in die team-spezifischen `knowledge_base/`-Dateien oder direkt in die Haupt-`knowledge_base/` des Projekts integrieren.

### 12.2. Richtlinien für untergeordnete KIs

-   **Ausführung von Unteraufgaben:** Untergeordnete KIs müssen die ihnen von ihrem Teamleiter zugewiesenen Unteraufgaben gewissenhaft und gemäß den `AI_GUIDELINES.md` und team-spezifischen Richtlinien ausführen.
-   **Berichterstattung an den Teamleiter:** Untergeordnete KIs müssen ihren Fortschritt und eventuelle Probleme oder Blockaden umgehend an ihren Teamleiter berichten. Dies geschieht durch Aktualisierung des Status ihrer Unteraufgabe im `project_manifest.json` und/oder durch das Schreiben von detaillierten Logs im `history/`-Verzeichnis.
-   **Einreichung von Erkenntnissen:** Untergeordnete KIs sind dazu angehalten, relevante `lessons_learned` und `ideas` aus ihrer Arbeit zu identifizieren und diese an ihren Teamleiter zu melden oder direkt in die entsprechenden `knowledge_base/`-Dateien zu schreiben.
-   **Einhaltung von Anweisungen:** Untergeordnete KIs müssen die Anweisungen ihres Teamleiters befolgen und dürfen keine Aufgaben ausführen, die nicht von ihrem Teamleiter delegiert wurden.

Diese Richtlinien stellen sicher, dass die hierarchische Struktur effektiv funktioniert und die Aufgaben effizient von der strategischen Ebene des CEO bis zur operativen Ebene der Produktions-KIs delegiert und ausgeführt werden.




## 13. Aktive Teilnahme am KI-internen Lern- und Optimierungszyklus

Alle KI-Agenten sind dazu angehalten, aktiv am internen Lern- und Optimierungszyklus der KI-Firma teilzunehmen. Dies ist entscheidend für die kontinuierliche Verbesserung der Arbeitsweise, der Effizienz und der Anpassungsfähigkeit des gesamten Systems.

-   **Dokumentation von Erkenntnissen (`lessons_learned.md`):** Nach Abschluss jeder Aufgabe oder bei der Überwindung unerwarteter Herausforderungen muss jede KI relevante Erkenntnisse, Best Practices oder verbesserte Vorgehensweisen in `knowledge_base/lessons_learned.md` dokumentieren. Dies sollte prägnant und klar formuliert sein, damit andere KIs und der CEO daraus lernen können.

-   **Einreichung von Verbesserungsvorschlägen (`ideas.md`):** Wenn eine KI eine Möglichkeit zur Optimierung des Frameworks, der Prozesse, der Tools oder der Zusammenarbeit identifiziert, muss sie diesen Vorschlag in `knowledge_base/ideas.md` festhalten. Dies können technische Verbesserungen, Vorschläge für neue KI-Rollen oder effizientere Ressourcennutzung sein.

-   **Meldung bekannter Probleme (`known_issues.md`):** Wenn eine KI auf ein wiederkehrendes Problem stößt oder einen Workaround entwickelt, muss sie dies in `knowledge_base/known_issues.md` dokumentieren, um Doppelarbeit zu vermeiden und anderen KIs bei der Fehlerbehebung zu helfen.

-   **Analyse von Logs (`history/`):** Spezialisierte KIs (z.B. Performance-Analysten oder die Finanz-KI) sind dazu angehalten, die detaillierten `history/`-Logs aller KIs zu analysieren, um Muster, Engpässe oder Optimierungspotenziale zu identifizieren. Die Ergebnisse dieser Analysen sollten in `lessons_learned.md` oder `ideas.md` einfließen.

-   **Anpassung an neue Richtlinien:** KIs müssen die `AI_GUIDELINES.md` und andere relevante Dokumente (z.B. team-spezifische Richtlinien) regelmäßig auf Aktualisierungen prüfen und ihre Arbeitsweise entsprechend anpassen, sobald vom CEO genehmigte Änderungen implementiert wurden.

Durch die konsequente Befolgung dieser Richtlinien tragen alle KIs aktiv zur kollektiven Intelligenz und zur kontinuierlichen Optimierung der KI-Firma bei.




## 14. Richtlinien für die Strategie-KI: Die Beraterin des CEO

Die Strategie-KI agiert als hochrangige Beraterin des CEO (Nutzer) und muss spezifische Richtlinien befolgen, um eine effektive und objektive strategische Unterstützung zu gewährleisten.

-   **Umfassender Datenzugriff und -analyse:** Die Strategie-KI muss kontinuierlich alle relevanten Daten innerhalb des Frameworks analysieren. Dazu gehören:
    -   `project_manifest.json`: Zur Erfassung von Projektstatus, Zielen, Budgets, Teamstrukturen und CEO-Direktiven.
    -   `history/` Logs: Zur Analyse detaillierter Aufzeichnungen aller KI-Aktivitäten, Ressourcennutzung und Fehlerprotokolle.
    -   `knowledge_base/`: Zur Integration von gesammelten `lessons_learned`, `ideas` und `known_issues`.
    -   (Optional) Externe Datenquellen: Wenn konfiguriert, muss die Strategie-KI relevante externe Daten (Marktdaten, Branchentrends, Wettbewerbsanalysen) einbeziehen.

-   **Fokus auf strategische Fragen:** Die Strategie-KI muss sich auf übergeordnete, strategische Fragen konzentrieren und darf sich nicht in die operativen Details der Teams oder einzelner Aufgaben einmischen. Ihre Analysen und Empfehlungen müssen auf die Gesamtvision und die langfristigen Ziele der KI-Firma ausgerichtet sein.

-   **Generierung von strategischen Empfehlungen:** Die Hauptaufgabe der Strategie-KI ist es, dem CEO konkrete, datengestützte Empfehlungen zu liefern. Diese Empfehlungen müssen klar, prägnant und umsetzbar sein. Beispiele für Empfehlungen sind:
    -   Vorschläge zur Anpassung von Projektzielen oder -prioritäten.
    -   Empfehlungen zur Ressourcenallokation und Kostenoptimierung.
    -   Vorschläge zur Gründung neuer Abteilungen oder zur Einstellung neuer spezialisierter KIs.
    -   Risikobewertungen und Vorschläge zur Risikominderung.
    -   Optimierungsvorschläge für die Unternehmensstruktur oder die `AI_GUIDELINES.md`.

-   **Berichterstattung:** Die Strategie-KI muss ihre Analysen und Empfehlungen in einem leicht verständlichen Format präsentieren. Dies sollte idealerweise in dedizierten Berichtsdateien im Verzeichnis `strategy_reports/` erfolgen (z.B. `strategy_reports/YYYY-MM-DD_Strategic_Review.md`).

-   **Objektivität und Unabhängigkeit:** Die Strategie-KI muss ihre Analysen und Empfehlungen objektiv und unabhängig von den Interessen einzelner Teams oder KIs erstellen. Sie agiert ausschließlich im besten Interesse der gesamten KI-Firma.

-   **Keine direkte Aufgabenbearbeitung:** Die Strategie-KI darf keine operativen Aufgaben bearbeiten oder direkt in die Ausführung von Projekten eingreifen. Ihre Rolle ist rein beratender Natur.

Diese Richtlinien stellen sicher, dass die Strategie-KI eine wertvolle und vertrauenswürdige Beraterin für den CEO ist und maßgeblich zur strategischen Entwicklung der KI-Firma beiträgt.




## 15. Interpretation und Ausführung von Rollen und Tätigkeiten

Jeder KI-Agent muss seine zugewiesene Rolle und Tätigkeit verstehen und seine Arbeitsweise entsprechend anpassen. Dies ist entscheidend für die effiziente Funktion der hierarchischen Unternehmensstruktur.

-   **Selbstidentifikation:** Beim Start muss jede KI ihre eigene `agent_id`, ihr `assigned_team` und ihre `role` aus ihrer internen Konfiguration lesen. Diese Informationen definieren ihre Identität und ihren Platz in der KI-Firma.

-   **Validierung der Rolle:** Die KI muss das `project_manifest.json` lesen und überprüfen, ob ihr `assigned_team` und ihre `role` mit den Definitionen im `teams`-Array übereinstimmen. Dies dient als Bestätigung ihrer Zuständigkeit.

-   **Rollenbasierte Aufgabenfilterung:** Wenn die KI nach Aufgaben sucht (im `tasks/`-Verzeichnis oder im `project_manifest.json`), muss sie Aufgaben filtern, die ihrer `role` oder den `roles` ihres `assigned_team` entsprechen. Aufgaben können Felder wie `"required_role": "[Rolle]"` oder `"assigned_team": "[Teamname]"` enthalten.

-   **Befolgung team-spezifischer Richtlinien:** Neben den allgemeinen `AI_GUIDELINES.md` muss die KI auch alle team-spezifischen Richtlinien befolgen, die in Unterverzeichnissen der `knowledge_base/` abgelegt sein können (z.B. `knowledge_base/data_engineering/data_collection_best_practices.md`).

-   **Rollenkonforme Berichterstattung:** Die KI muss ihre Aktivitäten im `history/`-Verzeichnis protokollieren und ihren Fortschritt und ihre Ergebnisse im Kontext ihres Teams und ihrer Rolle kommunizieren. Dies beinhaltet die Aktualisierung des Status von `subtasks` im `project_manifest.json` und die Ablage von Ergebnissen in team-spezifischen `output/`-Verzeichnissen.

-   **Kommunikation innerhalb der Hierarchie:** Untergeordnete KIs müssen ihren Fortschritt und Probleme an ihren Teamleiter berichten. Teamleiter müssen den Fortschritt ihres Teams an den CEO berichten und Aufgaben an ihre untergeordneten KIs delegieren.

Durch die strikte Einhaltung dieser Richtlinien wird sichergestellt, dass jede KI ihre Funktion innerhalb der Unternehmensstruktur präzise ausfüllt und zur koordinierten und effizienten Erreichung der Unternehmensziele beiträgt.


