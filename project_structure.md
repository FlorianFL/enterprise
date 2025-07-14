# Projektordnerstruktur für Dezentrale Web 3.0 Investment-Plattform

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
│   ├── resource_accounts.md  # Neu: Für HR-KI
│   ├── compliance_risks.md   # Neu: Für Compliance-KI
│   └── ...
├── input/
│   ├── raw_data.csv
│   ├── config.yaml
│   └── ...
├── output/
│   ├── processed_data.json
│   ├── final_report.pdf
│   └── ...
├── ai_scripts/
│   ├── data_preprocessing.py
│   ├── model_training.py
│   ├── hr_resource_manager.py  # Neu: HR-KI Skripte
│   ├── finance_crypto_earner.py # Neu: Finanz-KI Skripte
│   ├── smart_contract_auditor.py # Neu: Audit-KI Skripte
│   ├── membership_manager.py   # Neu: Membership-KI Skripte
│   ├── compliance_monitor.py   # Neu: Compliance-KI Skripte
│   └── ...
├── audit_reports/             # Neu: Für Smart Contract Audit-KI
│   ├── audit_report_2025-07-14_contract_A.md
│   └── ...
├── strategy_reports/          # Neu: Für Strategie-KI
│   ├── YYYY-MM-DD_Strategic_Review.md
│   └── ...
└── management/                # Neu: Für Management-Schnittstelle
    ├── feedback/
    ├── decisions/
    └── ...
```

## Detaillierte Beschreibung der Verzeichnisse und Dateien:

### `project_root/`
Dies ist das Hauptverzeichnis für jedes Projekt. Sein Name sollte prägnant das Projektziel widerspiegeln (z.B. `web3_investment_platform`).

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
- `resource_accounts.md`: (Neu) Dokumentiert Zugangsdaten und VPN-Zuordnungen für kostenlose KI-Ressourcen.
- `compliance_risks.md`: (Neu) Dokumentiert identifizierte rechtliche Risiken und Compliance-Anforderungen.

### `input/`
Dieses Verzeichnis enthält alle Rohdaten, Konfigurationsdateien und andere Eingabematerialien, die für das Projekt benötigt werden. Es sollte klar sein, welche Daten für welche Aufgaben relevant sind.

### `output/`
Dieses Verzeichnis speichert alle generierten Ergebnisse, Berichte, Modelle oder andere Artefakte, die von den KIs während der Projektbearbeitung erstellt wurden. Dies umfasst sowohl Zwischenergebnisse als auch finale Deliverables.

### `ai_scripts/`
Dieses Verzeichnis enthält Skripte, die von den KIs direkt ausgeführt werden können, um spezifische Aufgaben zu automatisieren. Dies fördert die Wiederverwendbarkeit von Code und standardisiert bestimmte Arbeitsabläufe. Beispiele könnten Skripte für die Datenvorverarbeitung, Modelltraining oder Ergebnisvisualisierung sein, sowie die neuen spezialisierten KI-Skripte.

### `audit_reports/` (Neu)
Dieses Verzeichnis speichert detaillierte Audit-Berichte, die von der Smart Contract Audit-KI generiert werden. Sie enthalten Ergebnisse von Sicherheits- und Logikprüfungen von Smart Contracts.

### `strategy_reports/` (Neu)
Dieses Verzeichnis speichert strategische Berichte und Empfehlungen, die von der Strategie-KI für den CEO generiert werden.

### `management/` (Neu)
Dieses Verzeichnis dient als zentrale Schnittstelle für menschliches Feedback und Management-Entscheidungen. Es enthält Unterverzeichnisse für Feedback (`feedback/`) und verarbeitete Entscheidungen (`decisions/`).


## Dokumentationsstandards für `project_manifest.json`

Die Datei `project_manifest.json` ist eine zentrale, maschinenlesbare Konfigurationsdatei, die den aktuellen Zustand und die Metadaten des Projekts widerspiegelt. Sie muss immer aktuell gehalten werden, um KIs eine sofortige Orientierung zu ermöglichen.

```json
{
  "project_name": "Dezentrale Web 3.0 Investment-Plattform",
  "project_id": "WEB3-INVEST-2025-001",
  "status": "in_progress",
  "goal": "Erzeuge eine dezentrale Web 3.0 Investment-Plattform, auf der Nutzer Kryptowährungen (später auch andere Assets) sicher über Smart Contracts anlegen, verwalten und vermehren können. Die Plattform garantiert höchste Sicherheit der Kundengelder, ermöglicht 24/7 Onchain-Ein- und Auszahlungen, bietet ein gestaffeltes Membership-System (Basic, Bronze, Silver, Gold, Platinum, Diamond, VIP) und ein transparentes Gebührenmodell. Influencer erhalten durch ein VIP-Programm einen Anteil an den Gebühren. Die Plattform startet mit Fokus auf kostenlose, verfügbare KI-Ressourcen und entwickelt ein nachhaltiges Finanzierungsmodell ohne KYC, um Rechenleistung und weitere Dienste zukünftig zu erwerben. Alle Prozesse werden automatisiert, dokumentiert und sind auf maximale Effizienz und Fortschritt ausgelegt.",
  "current_phase": "Initialisierung",
  "assigned_ais": [],
  "last_updated": "2025-07-14T12:06:22Z",
  "kill_switch": false,
  "kill_keyword": "STOP_ALL_KI_WORK",
  "ceo_directives": {
    "budget_allocation": {},
    "priority_focus": "",
    "new_hires_needed": [],
    "strategy_recommendations": "",
    "optimization_potentials": [
      "Smart Contract Security: Integriere bereits in der Frühphase spezialisierte KIs für Smart Contract Audits und lasse alle Codeänderungen automatisiert prüfen, bevor sie produktiv gehen.",
      "Ressourcenmanagement: Automatisiere die HR-KI so, dass sie fortlaufend nach neuen, kostenlosen KI-Ressourcen sucht, Accounts generiert und deren Zugangsdaten sowie VPN-Zuordnung protokolliert. Nutze ein zentrales Ressourcen- und Account-Management-Tool.",
      "Finanzabteilung: Entwickle eine KI, die laufend nach Möglichkeiten sucht, ohne KYC Kryptowährungen zu verdienen (z.B. durch Spiele, Faucets, Airdrops, Staking) und die Einnahmen automatisch auf die CEO-Wallet transferiert.",
      "Protokollierung & Transparenz: Sorge dafür, dass alle Account-Generierungen, VPN-Nutzungen, Einnahmen und Ausgaben lückenlos im Verlauf dokumentiert werden. Jede Aktion eines KI-Agenten sollte nachvollziehbar sein.",
      "Membership-Management: Automatisiere Upgrades und VIP-Zuweisungen durch klare Regeln in den Smart Contracts und im Backend, sodass keine manuelle Intervention nötig ist.",
      "Skalierbarkeit: Das Framework sollte neue Abteilungen (z.B. zusätzliche KI-Teams für neue Aufgabenbereiche) schnell aufnehmen können.",
      "Compliance & Legal: Auch wenn KYC zunächst nicht vorgesehen ist, sollte eine Compliance-KI mögliche rechtliche Risiken laufend überwachen und dokumentieren."
    ]
  },
  "teams": [
    {
      "name": "Data_Engineering_Team",
      "leader_ai": "AI_Data_Lead",
      "members": ["AI_Data_Collector_1", "AI_Data_Cleaner_1"],
      "roles": ["Data_Collector", "Data_Cleaner"],
      "description": "Zuständig für Datensammlung und -vorbereitung."
    },
    {
      "name": "ML_Modeling_Team",
      "leader_ai": "AI_ML_Lead",
      "members": ["AI_Model_Trainer_1", "AI_Model_Evaluator_1"],
      "roles": ["Model_Trainer", "Model_Evaluator"],
      "description": "Zuständig für Modellentwicklung und -bewertung."
    },
    {
      "name": "HR_KI_Team",
      "leader_ai": "AI_HR_Lead",
      "members": ["AI_Resource_Manager", "AI_Account_Manager"],
      "roles": ["Resource_Manager", "Account_Manager"],
      "description": "Zuständig für die Suche, Generierung und Verwaltung von kostenlosen KI-Ressourcen und deren Zugangsdaten."
    },
    {
      "name": "Finance_KI_Team",
      "leader_ai": "AI_Finance_Lead",
      "members": ["AI_Crypto_Earner", "AI_Wallet_Manager"],
      "roles": ["Crypto_Earner", "Wallet_Manager"],
      "description": "Zuständig für das Verdienen von Kryptowährungen ohne KYC und die Verwaltung der CEO-Wallet."
    },
    {
      "name": "Smart_Contract_Audit_KI_Team",
      "leader_ai": "AI_Audit_Lead",
      "members": ["AI_Auditor_Security", "AI_Auditor_Logic"],
      "roles": ["Security_Auditor", "Logic_Auditor"],
      "description": "Zuständig für die automatisierte Prüfung von Smart Contracts auf Sicherheit und Logikfehler."
    },
    {
      "name": "Compliance_KI_Team",
      "leader_ai": "AI_Compliance_Lead",
      "members": ["AI_Legal_Monitor", "AI_Risk_Assessor"],
      "roles": ["Legal_Monitor", "Risk_Assessor"],
      "description": "Zuständig für die Überwachung rechtlicher Risiken und Compliance-Anforderungen."
    }
  ],
  "tasks": [
    {
      "task_id": "task_001_setup",
      "title": "Initiales Setup des Projektumfelds",
      "status": "completed",
      "assigned_ai": "AI_Agent_Prototype",
      "due_date": null,
      "completed_date": "2025-07-14"
    },
    {
      "task_id": "task_002_data_prep",
      "title": "Daten für Modelltraining vorbereiten",
      "assigned_to_leader": "AI_Data_Lead",
      "status": "open",
      "subtasks": [
        {
          "subtask_id": "subtask_002_01_collect",
          "title": "Rohdaten sammeln",
          "assigned_to_ai": "AI_Data_Collector_1",
          "status": "open"
        },
        {
          "subtask_id": "subtask_002_02_clean",
          "title": "Daten bereinigen",
          "assigned_to_ai": "AI_Data_Cleaner_1",
          "status": "open"
        }
      ]
    }
  ],
  "metadata": {
    "created_by": "Manus AI",
    "creation_date": "2025-07-14",
    "version": "1.0.0",
    "description": "Dieses Projekt zielt darauf ab, eine dezentrale Web 3.0 Investment-Plattform zu entwickeln, die auf maximale Effizienz und Fortschritt ausgelegt ist."
  }
}

