import json
import os
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import uuid

class ManagementInterface:
    """
    Schnittstelle für menschliches Feedback und Management-Interaktion
    Ermöglicht CEO und anderen menschlichen Nutzern direktes Feedback auf KI-Vorschläge
    """
    
    def __init__(self, project_root: str):
        self.project_root = project_root
        self.knowledge_base_dir = os.path.join(project_root, 'knowledge_base')
        self.ideas_path = os.path.join(self.knowledge_base_dir, 'ideas.md')
        self.management_dir = os.path.join(project_root, 'management')
        self.feedback_dir = os.path.join(self.management_dir, 'feedback')
        self.decisions_dir = os.path.join(self.management_dir, 'decisions')
        self.manifest_path = os.path.join(project_root, 'project_manifest.json')
        
        # Management-Response-Status
        self.response_status = {
            'pending': 'Ausstehend',
            'approved': 'Genehmigt',
            'rejected': 'Abgelehnt',
            'needs_revision': 'Überarbeitung erforderlich',
            'under_review': 'In Prüfung',
            'implemented': 'Umgesetzt'
        }
        
        # Prioritätsstufen für Management-Entscheidungen
        self.priority_levels = {
            'low': 'Niedrig',
            'medium': 'Mittel', 
            'high': 'Hoch',
            'critical': 'Kritisch',
            'strategic': 'Strategisch'
        }
        
        # Stelle sicher, dass Management-Verzeichnisse existieren
        os.makedirs(self.management_dir, exist_ok=True)
        os.makedirs(self.feedback_dir, exist_ok=True)
        os.makedirs(self.decisions_dir, exist_ok=True)
    
    def load_manifest(self) -> Dict[str, Any]:
        """Lädt das project_manifest.json"""
        with open(self.manifest_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def save_manifest(self, manifest: Dict[str, Any]) -> None:
        """Speichert das project_manifest.json"""
        with open(self.manifest_path, 'w', encoding='utf-8') as f:
            json.dump(manifest, f, indent=2, ensure_ascii=False)
    
    def extract_ideas_for_review(self) -> List[Dict[str, Any]]:
        """Extrahiert KI-Vorschläge aus ideas.md für Management-Review"""
        if not os.path.exists(self.ideas_path):
            return []
        
        with open(self.ideas_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        ideas = []
        current_idea = None
        
        lines = content.split('\n')
        for line in lines:
            line = line.strip()
            
            # Neue Idee (Überschrift Level 2 oder 3)
            if line.startswith('##') and not line.startswith('###'):
                if current_idea:
                    ideas.append(current_idea)
                
                current_idea = {
                    'id': self._generate_idea_id(line),
                    'title': line.replace('#', '').strip(),
                    'content': '',
                    'category': self._categorize_idea(line),
                    'priority': self._estimate_priority(line),
                    'source': 'ai_generated',
                    'status': 'pending',
                    'extracted_date': datetime.now().isoformat()
                }
            
            elif current_idea and line:
                # Inhalt zur aktuellen Idee hinzufügen
                if not line.startswith('#'):
                    current_idea['content'] += line + ' '
        
        if current_idea:
            ideas.append(current_idea)
        
        # Bereinige Content
        for idea in ideas:
            idea['content'] = idea['content'].strip()
        
        return ideas
    
    def _generate_idea_id(self, title: str) -> str:
        """Generiert eine eindeutige ID für eine Idee"""
        # Vereinfache Titel für ID
        clean_title = ''.join(c.lower() for c in title if c.isalnum() or c.isspace())
        words = clean_title.split()[:3]  # Erste 3 Wörter
        base_id = '_'.join(words)
        
        # Füge Zeitstempel hinzu für Eindeutigkeit
        timestamp = datetime.now().strftime('%m%d')
        return f"idea_{base_id}_{timestamp}"
    
    def _categorize_idea(self, title: str) -> str:
        """Kategorisiert eine Idee basierend auf dem Titel"""
        title_lower = title.lower()
        
        categories = {
            'process_improvement': ['prozess', 'workflow', 'verbesserung', 'optimierung'],
            'technology': ['technologie', 'tool', 'system', 'software', 'api'],
            'team_management': ['team', 'personal', 'management', 'führung'],
            'quality_assurance': ['qualität', 'test', 'validierung', 'kontrolle'],
            'automation': ['automatisierung', 'automatisch', 'script'],
            'communication': ['kommunikation', 'dokumentation', 'bericht'],
            'strategic': ['strategie', 'vision', 'ziel', 'roadmap'],
            'cost_optimization': ['kosten', 'budget', 'effizienz', 'ressource']
        }
        
        for category, keywords in categories.items():
            if any(keyword in title_lower for keyword in keywords):
                return category
        
        return 'general'
    
    def _estimate_priority(self, title: str) -> str:
        """Schätzt die Priorität einer Idee"""
        title_lower = title.lower()
        
        if any(word in title_lower for word in ['kritisch', 'dringend', 'sofort', 'notfall']):
            return 'critical'
        elif any(word in title_lower for word in ['wichtig', 'hoch', 'priorität']):
            return 'high'
        elif any(word in title_lower for word in ['strategie', 'langfristig', 'vision']):
            return 'strategic'
        elif any(word in title_lower for word in ['klein', 'einfach', 'optional']):
            return 'low'
        else:
            return 'medium'
    
    def create_management_review_board(self) -> str:
        """Erstellt ein Management-Review-Board mit allen ausstehenden Ideen"""
        ideas = self.extract_ideas_for_review()
        
        # Filtere nur ausstehende Ideen
        pending_ideas = [idea for idea in ideas if idea['status'] == 'pending']
        
        if not pending_ideas:
            return "Keine ausstehenden KI-Vorschläge für Management-Review."
        
        board = "# Management Review Board\n\n"
        board += f"Generiert am: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        board += f"Ausstehende Vorschläge: {len(pending_ideas)}\n\n"
        
        # Gruppiere nach Priorität
        by_priority = {}
        for idea in pending_ideas:
            priority = idea['priority']
            if priority not in by_priority:
                by_priority[priority] = []
            by_priority[priority].append(idea)
        
        # Sortiere nach Priorität
        priority_order = ['critical', 'strategic', 'high', 'medium', 'low']
        
        for priority in priority_order:
            if priority in by_priority:
                priority_name = self.priority_levels.get(priority, priority.title())
                priority_emoji = {
                    'critical': '🚨',
                    'strategic': '🎯',
                    'high': '⚠️',
                    'medium': '📋',
                    'low': '💡'
                }.get(priority, '📌')
                
                board += f"## {priority_emoji} {priority_name} Priorität\n\n"
                
                for idea in by_priority[priority]:
                    board += f"### {idea['title']}\n\n"
                    board += f"**ID:** `{idea['id']}`\n"
                    board += f"**Kategorie:** {idea['category'].replace('_', ' ').title()}\n"
                    board += f"**Quelle:** {idea['source']}\n"
                    board += f"**Extrahiert am:** {idea['extracted_date'][:10]}\n\n"
                    
                    if idea['content']:
                        content = idea['content'][:300]
                        if len(idea['content']) > 300:
                            content += "..."
                        board += f"**Beschreibung:** {content}\n\n"
                    
                    # Management Response Bereich
                    board += "**Management Response:**\n"
                    board += "```\n"
                    board += "Status: [pending/approved/rejected/needs_revision/under_review]\n"
                    board += "Kommentar: [Ihr Feedback hier]\n"
                    board += "Priorität: [low/medium/high/critical/strategic]\n"
                    board += "Deadline: [YYYY-MM-DD oder 'none']\n"
                    board += "Zugewiesener Agent: [agent_id oder 'auto']\n"
                    board += "Budget: [Betrag oder 'none']\n"
                    board += "```\n\n"
                    board += "---\n\n"
        
        # Anweisungen
        board += "## Anweisungen für Management\n\n"
        board += "1. **Status setzen:** Wählen Sie einen der verfügbaren Status\n"
        board += "2. **Kommentar hinzufügen:** Geben Sie spezifisches Feedback\n"
        board += "3. **Priorität anpassen:** Falls erforderlich\n"
        board += "4. **Deadline setzen:** Für genehmigte Ideen\n"
        board += "5. **Agent zuweisen:** Spezifischer Agent oder 'auto' für automatische Zuweisung\n"
        board += "6. **Budget festlegen:** Falls Ressourcen erforderlich\n\n"
        board += "**Speichern Sie diese Datei nach Ihren Änderungen als `management_decisions_[DATUM].md`**\n"
        
        return board
    
    def process_management_decisions(self, decisions_content: str) -> Dict[str, Any]:
        """Verarbeitet Management-Entscheidungen aus dem Review Board"""
        results = {
            'processed_decisions': 0,
            'approved_ideas': [],
            'rejected_ideas': [],
            'revision_needed': [],
            'errors': []
        }
        
        # Parse Entscheidungen aus dem Content
        decisions = self._parse_management_responses(decisions_content)
        
        for decision in decisions:
            try:
                # Validiere Entscheidung
                if not self._validate_decision(decision):
                    results['errors'].append(f"Ungültige Entscheidung für ID {decision.get('id', 'unknown')}")
                    continue
                
                # Verarbeite basierend auf Status
                status = decision['status']
                
                if status == 'approved':
                    self._process_approved_idea(decision)
                    results['approved_ideas'].append(decision['id'])
                
                elif status == 'rejected':
                    self._process_rejected_idea(decision)
                    results['rejected_ideas'].append(decision['id'])
                
                elif status == 'needs_revision':
                    self._process_revision_request(decision)
                    results['revision_needed'].append(decision['id'])
                
                # Speichere Entscheidung
                self._save_management_decision(decision)
                results['processed_decisions'] += 1
                
            except Exception as e:
                results['errors'].append(f"Fehler bei Verarbeitung von {decision.get('id', 'unknown')}: {str(e)}")
        
        return results
    
    def _parse_management_responses(self, content: str) -> List[Dict[str, Any]]:
        """Parst Management-Responses aus dem Review Board Content"""
        decisions = []
        lines = content.split('\n')
        
        current_idea_id = None
        in_response_block = False
        response_data = {}
        
        for line in lines:
            line = line.strip()
            
            # Suche nach Idea ID
            if line.startswith('**ID:**'):
                current_idea_id = line.replace('**ID:**', '').strip().replace('`', '')
                response_data = {'id': current_idea_id}
            
            # Beginn des Response Blocks
            elif line == '**Management Response:**':
                in_response_block = True
            
            # Ende des Response Blocks
            elif line == '```' and in_response_block:
                if response_data and current_idea_id:
                    decisions.append(response_data.copy())
                in_response_block = False
                response_data = {'id': current_idea_id} if current_idea_id else {}
            
            # Parse Response-Felder
            elif in_response_block and ':' in line:
                key, value = line.split(':', 1)
                key = key.strip().lower().replace(' ', '_')
                value = value.strip()
                
                if value and value != '[pending/approved/rejected/needs_revision/under_review]' and not value.startswith('['):
                    response_data[key] = value
        
        return decisions
    
    def _validate_decision(self, decision: Dict[str, Any]) -> bool:
        """Validiert eine Management-Entscheidung"""
        required_fields = ['id', 'status']
        
        for field in required_fields:
            if field not in decision or not decision[field]:
                return False
        
        # Validiere Status
        valid_statuses = list(self.response_status.keys())
        if decision['status'] not in valid_statuses:
            return False
        
        return True
    
    def _process_approved_idea(self, decision: Dict[str, Any]) -> None:
        """Verarbeitet eine genehmigte Idee"""
        manifest = self.load_manifest()
        
        # Erstelle neue Aufgabe aus genehmigter Idee
        task_id = f"task_{decision['id']}_{datetime.now().strftime('%m%d')}"
        
        new_task = {
            'task_id': task_id,
            'title': f"Umsetzung: {decision.get('title', 'Management-genehmigte Idee')}",
            'description': decision.get('kommentar', 'Vom Management genehmigte Verbesserungsidee'),
            'status': 'open',
            'priority': decision.get('priorität', 'medium'),
            'created_date': datetime.now().isoformat(),
            'source': 'management_approved_idea',
            'original_idea_id': decision['id']
        }
        
        # Deadline setzen
        if decision.get('deadline') and decision['deadline'] != 'none':
            new_task['deadline'] = decision['deadline']
        
        # Agent zuweisen
        if decision.get('zugewiesener_agent') and decision['zugewiesener_agent'] != 'auto':
            new_task['assigned_to'] = decision['zugewiesener_agent']
        
        # Budget hinzufügen
        if decision.get('budget') and decision['budget'] != 'none':
            new_task['budget'] = decision['budget']
        
        # Zu Manifest hinzufügen
        if 'tasks' not in manifest:
            manifest['tasks'] = []
        
        manifest['tasks'].append(new_task)
        self.save_manifest(manifest)
    
    def _process_rejected_idea(self, decision: Dict[str, Any]) -> None:
        """Verarbeitet eine abgelehnte Idee"""
        # Dokumentiere Ablehnung für zukünftige Referenz
        rejection_log = {
            'idea_id': decision['id'],
            'rejected_date': datetime.now().isoformat(),
            'reason': decision.get('kommentar', 'Keine Begründung angegeben'),
            'rejected_by': 'management'
        }
        
        # Speichere in separater Rejection-Log-Datei
        rejection_file = os.path.join(self.decisions_dir, 'rejected_ideas.json')
        
        if os.path.exists(rejection_file):
            with open(rejection_file, 'r', encoding='utf-8') as f:
                rejections = json.load(f)
        else:
            rejections = []
        
        rejections.append(rejection_log)
        
        with open(rejection_file, 'w', encoding='utf-8') as f:
            json.dump(rejections, f, indent=2, ensure_ascii=False)
    
    def _process_revision_request(self, decision: Dict[str, Any]) -> None:
        """Verarbeitet eine Überarbeitungsanfrage"""
        revision_request = {
            'idea_id': decision['id'],
            'requested_date': datetime.now().isoformat(),
            'feedback': decision.get('kommentar', 'Überarbeitung erforderlich'),
            'new_priority': decision.get('priorität', 'medium'),
            'status': 'revision_requested'
        }
        
        # Speichere Überarbeitungsanfrage
        revision_file = os.path.join(self.decisions_dir, 'revision_requests.json')
        
        if os.path.exists(revision_file):
            with open(revision_file, 'r', encoding='utf-8') as f:
                revisions = json.load(f)
        else:
            revisions = []
        
        revisions.append(revision_request)
        
        with open(revision_file, 'w', encoding='utf-8') as f:
            json.dump(revisions, f, indent=2, ensure_ascii=False)
    
    def _save_management_decision(self, decision: Dict[str, Any]) -> None:
        """Speichert eine Management-Entscheidung"""
        decision_record = {
            'decision_id': f"decision_{decision['id']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            'idea_id': decision['id'],
            'timestamp': datetime.now().isoformat(),
            'decision': decision,
            'processed': True
        }
        
        decision_file = os.path.join(self.decisions_dir, f"{decision_record['decision_id']}.json")
        
        with open(decision_file, 'w', encoding='utf-8') as f:
            json.dump(decision_record, f, indent=2, ensure_ascii=False)
    
    def generate_management_dashboard(self) -> str:
        """Generiert ein Management-Dashboard mit Übersicht"""
        dashboard = "# Management Dashboard\n\n"
        dashboard += f"Generiert am: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        # Sammle Statistiken
        ideas = self.extract_ideas_for_review()
        pending_ideas = [idea for idea in ideas if idea['status'] == 'pending']
        
        # Lade Entscheidungshistorie
        decisions_count = 0
        approved_count = 0
        rejected_count = 0
        
        if os.path.exists(self.decisions_dir):
            for filename in os.listdir(self.decisions_dir):
                if filename.startswith('decision_') and filename.endswith('.json'):
                    decisions_count += 1
                    
                    try:
                        with open(os.path.join(self.decisions_dir, filename), 'r', encoding='utf-8') as f:
                            decision = json.load(f)
                        
                        status = decision.get('decision', {}).get('status', '')
                        if status == 'approved':
                            approved_count += 1
                        elif status == 'rejected':
                            rejected_count += 1
                    except:
                        continue
        
        # Übersicht
        dashboard += "## Übersicht\n\n"
        dashboard += f"- **Ausstehende KI-Vorschläge:** {len(pending_ideas)}\n"
        dashboard += f"- **Gesamte Entscheidungen:** {decisions_count}\n"
        dashboard += f"- **Genehmigte Ideen:** {approved_count}\n"
        dashboard += f"- **Abgelehnte Ideen:** {rejected_count}\n\n"
        
        # Ausstehende Ideen nach Priorität
        if pending_ideas:
            dashboard += "## Ausstehende Entscheidungen nach Priorität\n\n"
            
            priority_counts = {}
            for idea in pending_ideas:
                priority = idea['priority']
                priority_counts[priority] = priority_counts.get(priority, 0) + 1
            
            for priority in ['critical', 'strategic', 'high', 'medium', 'low']:
                if priority in priority_counts:
                    count = priority_counts[priority]
                    priority_name = self.priority_levels.get(priority, priority.title())
                    dashboard += f"- **{priority_name}:** {count} Ideen\n"
            
            dashboard += "\n"
        
        # Kategorien-Verteilung
        if pending_ideas:
            dashboard += "## Kategorien-Verteilung\n\n"
            
            category_counts = {}
            for idea in pending_ideas:
                category = idea['category']
                category_counts[category] = category_counts.get(category, 0) + 1
            
            for category, count in sorted(category_counts.items(), key=lambda x: x[1], reverse=True):
                category_name = category.replace('_', ' ').title()
                dashboard += f"- **{category_name}:** {count} Ideen\n"
            
            dashboard += "\n"
        
        # Aktionen
        dashboard += "## Empfohlene Aktionen\n\n"
        
        if len(pending_ideas) > 10:
            dashboard += "- ⚠️ Hohe Anzahl ausstehender Entscheidungen - Review-Session empfohlen\n"
        
        critical_ideas = [idea for idea in pending_ideas if idea['priority'] == 'critical']
        if critical_ideas:
            dashboard += f"- 🚨 {len(critical_ideas)} kritische Ideen benötigen sofortige Aufmerksamkeit\n"
        
        strategic_ideas = [idea for idea in pending_ideas if idea['priority'] == 'strategic']
        if strategic_ideas:
            dashboard += f"- 🎯 {len(strategic_ideas)} strategische Ideen für Langzeitplanung\n"
        
        if not pending_ideas:
            dashboard += "- ✅ Alle KI-Vorschläge wurden bearbeitet\n"
        
        dashboard += "\n"
        
        # Quick Actions
        dashboard += "## Quick Actions\n\n"
        dashboard += "- [Neues Review Board erstellen](management_review_board.md)\n"
        dashboard += "- [Entscheidungen verarbeiten](process_decisions.md)\n"
        dashboard += "- [Rejected Ideas ansehen](rejected_ideas.json)\n"
        dashboard += "- [Revision Requests ansehen](revision_requests.json)\n\n"
        
        return dashboard
    
    def create_decision_template(self, idea_id: str) -> str:
        """Erstellt ein Entscheidungstemplate für eine spezifische Idee"""
        ideas = self.extract_ideas_for_review()
        target_idea = None
        
        for idea in ideas:
            if idea['id'] == idea_id:
                target_idea = idea
                break
        
        if not target_idea:
            return f"Idee mit ID '{idea_id}' nicht gefunden."
        
        template = f"# Management Decision Template\n\n"
        template += f"**Idee ID:** {target_idea['id']}\n"
        template += f"**Titel:** {target_idea['title']}\n"
        template += f"**Kategorie:** {target_idea['category'].replace('_', ' ').title()}\n"
        template += f"**Aktuelle Priorität:** {self.priority_levels.get(target_idea['priority'], target_idea['priority'])}\n\n"
        
        template += "## Ideen-Details\n\n"
        template += f"{target_idea['content']}\n\n"
        
        template += "## Management-Entscheidung\n\n"
        template += "**Status:** [Wählen Sie: approved/rejected/needs_revision/under_review]\n\n"
        template += "**Kommentar/Begründung:**\n"
        template += "[Ihr detailliertes Feedback hier]\n\n"
        template += "**Angepasste Priorität:** [low/medium/high/critical/strategic]\n\n"
        template += "**Deadline:** [YYYY-MM-DD oder 'none']\n\n"
        template += "**Zugewiesener Agent:** [agent_id oder 'auto']\n\n"
        template += "**Budget:** [Betrag oder 'none']\n\n"
        template += "**Zusätzliche Anweisungen:**\n"
        template += "[Spezielle Anweisungen für die Umsetzung]\n\n"
        
        return template

if __name__ == '__main__':
    # Test der Management Interface
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    mgmt_interface = ManagementInterface(project_root)
    
    print("=== Management Interface Test ===")
    
    # Extrahiere Ideen
    ideas = mgmt_interface.extract_ideas_for_review()
    print(f"Extrahierte Ideen: {len(ideas)}")
    
    # Erstelle Review Board
    board = mgmt_interface.create_management_review_board()
    print(f"Review Board erstellt: {len(board)} Zeichen")
    
    # Erstelle Dashboard
    dashboard = mgmt_interface.generate_management_dashboard()
    print(f"Dashboard erstellt: {len(dashboard)} Zeichen")

