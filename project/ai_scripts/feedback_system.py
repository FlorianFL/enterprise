import json
import os
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import uuid

class FeedbackSystem:
    """
    Automatisiertes Feedback- und Review-Loop-System für KI-Agenten
    """
    
    def __init__(self, project_root: str):
        self.project_root = project_root
        self.manifest_path = os.path.join(project_root, 'project_manifest.json')
        self.feedback_dir = os.path.join(project_root, 'feedback')
        self.knowledge_base_dir = os.path.join(project_root, 'knowledge_base')
        self.ideas_path = os.path.join(self.knowledge_base_dir, 'ideas.md')
        self.framework_improvements_path = os.path.join(project_root, '..', 'framework_improvements.md')
        
        # Feedback-Kategorien
        self.feedback_categories = {
            'task_clarity': 'Aufgabenklarheit',
            'process_efficiency': 'Prozesseffizienz',
            'resource_availability': 'Ressourcenverfügbarkeit',
            'communication': 'Kommunikation',
            'tools_and_frameworks': 'Tools und Frameworks',
            'documentation': 'Dokumentation',
            'collaboration': 'Zusammenarbeit'
        }
        
        # Bewertungsskala
        self.rating_scale = {
            1: 'Sehr schlecht',
            2: 'Schlecht', 
            3: 'Durchschnittlich',
            4: 'Gut',
            5: 'Sehr gut'
        }
        
        # Stelle sicher, dass Feedback-Verzeichnis existiert
        os.makedirs(self.feedback_dir, exist_ok=True)
    
    def load_manifest(self) -> Dict[str, Any]:
        """Lädt das project_manifest.json"""
        with open(self.manifest_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def save_manifest(self, manifest: Dict[str, Any]) -> None:
        """Speichert das project_manifest.json"""
        with open(self.manifest_path, 'w', encoding='utf-8') as f:
            json.dump(manifest, f, indent=2, ensure_ascii=False)
    
    def create_task_completion_feedback(self, task_id: str, agent_id: str, 
                                      ratings: Dict[str, int], 
                                      comments: Dict[str, str],
                                      suggestions: List[str] = None) -> str:
        """
        Erstellt Feedback nach Aufgabenabschluss
        """
        feedback_id = str(uuid.uuid4())[:8]
        timestamp = datetime.now().isoformat()
        
        feedback = {
            'feedback_id': feedback_id,
            'type': 'task_completion',
            'timestamp': timestamp,
            'task_id': task_id,
            'agent_id': agent_id,
            'ratings': ratings,
            'comments': comments,
            'suggestions': suggestions or [],
            'status': 'pending_review'
        }
        
        # Feedback speichern
        feedback_file = os.path.join(self.feedback_dir, f'feedback_{feedback_id}_{task_id}.json')
        with open(feedback_file, 'w', encoding='utf-8') as f:
            json.dump(feedback, f, indent=2, ensure_ascii=False)
        
        return feedback_id
    
    def generate_automated_feedback_prompt(self, task_id: str) -> Dict[str, Any]:
        """
        Generiert automatisierte Feedback-Prompts für KI-Agenten
        """
        manifest = self.load_manifest()
        task = None
        
        # Task finden
        for t in manifest.get('tasks', []):
            if t.get('task_id') == task_id:
                task = t
                break
        
        if not task:
            return {'error': f'Task {task_id} nicht gefunden'}
        
        # Feedback-Prompts basierend auf Task-Typ generieren
        prompts = {
            'task_clarity': {
                'question': 'Wie klar und verständlich war die Aufgabenbeschreibung?',
                'scale': '1-5 (1=sehr unklar, 5=sehr klar)',
                'follow_up': 'Was hätte klarer formuliert werden können?'
            },
            'process_efficiency': {
                'question': 'Wie effizient war der Arbeitsprozess für diese Aufgabe?',
                'scale': '1-5 (1=sehr ineffizient, 5=sehr effizient)',
                'follow_up': 'Welche Schritte könnten optimiert werden?'
            },
            'resource_availability': {
                'question': 'Waren alle benötigten Ressourcen verfügbar?',
                'scale': '1-5 (1=gar nicht verfügbar, 5=vollständig verfügbar)',
                'follow_up': 'Welche Ressourcen fehlten oder waren schwer zugänglich?'
            },
            'communication': {
                'question': 'Wie war die Kommunikation mit anderen Agenten/Teams?',
                'scale': '1-5 (1=sehr schlecht, 5=sehr gut)',
                'follow_up': 'Wie könnte die Kommunikation verbessert werden?'
            },
            'tools_and_frameworks': {
                'question': 'Wie gut unterstützten die verfügbaren Tools die Aufgabe?',
                'scale': '1-5 (1=gar nicht, 5=sehr gut)',
                'follow_up': 'Welche Tools fehlten oder könnten verbessert werden?'
            }
        }
        
        return {
            'task_id': task_id,
            'task_title': task.get('title'),
            'prompts': prompts,
            'instructions': 'Bitte bewerten Sie jeden Aspekt und geben Sie konstruktive Kommentare ab.'
        }
    
    def process_feedback_submission(self, feedback_data: Dict[str, Any]) -> str:
        """
        Verarbeitet eingereichte Feedback-Daten
        """
        feedback_id = self.create_task_completion_feedback(
            task_id=feedback_data.get('task_id'),
            agent_id=feedback_data.get('agent_id'),
            ratings=feedback_data.get('ratings', {}),
            comments=feedback_data.get('comments', {}),
            suggestions=feedback_data.get('suggestions', [])
        )
        
        # Automatische Verarbeitung für sofortige Verbesserungen
        self._process_immediate_improvements(feedback_data)
        
        return feedback_id
    
    def _process_immediate_improvements(self, feedback_data: Dict[str, Any]) -> None:
        """
        Verarbeitet Feedback für sofortige Verbesserungen
        """
        ratings = feedback_data.get('ratings', {})
        comments = feedback_data.get('comments', {})
        suggestions = feedback_data.get('suggestions', [])
        
        # Niedrige Bewertungen identifizieren
        low_ratings = {category: rating for category, rating in ratings.items() if rating <= 2}
        
        if low_ratings:
            # Automatisch zu ideas.md hinzufügen
            self._add_to_ideas(feedback_data, low_ratings)
        
        # Hohe Bewertungen für Best Practices
        high_ratings = {category: rating for category, rating in ratings.items() if rating >= 4}
        
        if high_ratings:
            # Zu Lessons Learned hinzufügen
            self._add_to_lessons_learned(feedback_data, high_ratings)
    
    def _add_to_ideas(self, feedback_data: Dict[str, Any], low_ratings: Dict[str, int]) -> None:
        """
        Fügt Verbesserungsvorschläge zu ideas.md hinzu
        """
        ideas_content = ""
        if os.path.exists(self.ideas_path):
            with open(self.ideas_path, 'r', encoding='utf-8') as f:
                ideas_content = f.read()
        
        # Neue Ideen basierend auf niedrigen Bewertungen
        new_ideas = f"\n\n## Automatisch generierte Verbesserungsvorschläge - {datetime.now().strftime('%Y-%m-%d')}\n\n"
        
        for category, rating in low_ratings.items():
            category_name = self.feedback_categories.get(category, category)
            new_ideas += f"### {category_name} (Bewertung: {rating}/5)\n"
            new_ideas += f"- **Task:** {feedback_data.get('task_id')}\n"
            new_ideas += f"- **Agent:** {feedback_data.get('agent_id')}\n"
            
            comment = feedback_data.get('comments', {}).get(category, '')
            if comment:
                new_ideas += f"- **Kommentar:** {comment}\n"
            
            # Automatische Verbesserungsvorschläge
            improvement_suggestions = self._generate_improvement_suggestions(category, rating, comment)
            for suggestion in improvement_suggestions:
                new_ideas += f"- **Vorschlag:** {suggestion}\n"
            
            new_ideas += "\n"
        
        # Manuelle Vorschläge hinzufügen
        suggestions = feedback_data.get('suggestions', [])
        if suggestions:
            new_ideas += "### Manuelle Verbesserungsvorschläge\n"
            for suggestion in suggestions:
                new_ideas += f"- {suggestion}\n"
            new_ideas += "\n"
        
        # Zu ideas.md hinzufügen
        updated_content = ideas_content + new_ideas
        with open(self.ideas_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)
    
    def _add_to_lessons_learned(self, feedback_data: Dict[str, Any], high_ratings: Dict[str, int]) -> None:
        """
        Fügt erfolgreiche Praktiken zu lessons_learned.md hinzu
        """
        lessons_path = os.path.join(self.knowledge_base_dir, 'lessons_learned.md')
        lessons_content = ""
        
        if os.path.exists(lessons_path):
            with open(lessons_path, 'r', encoding='utf-8') as f:
                lessons_content = f.read()
        
        new_lessons = f"\n\n## Erfolgreiche Praktiken - {datetime.now().strftime('%Y-%m-%d')}\n\n"
        
        for category, rating in high_ratings.items():
            category_name = self.feedback_categories.get(category, category)
            new_lessons += f"### {category_name} (Bewertung: {rating}/5)\n"
            new_lessons += f"- **Task:** {feedback_data.get('task_id')}\n"
            new_lessons += f"- **Agent:** {feedback_data.get('agent_id')}\n"
            
            comment = feedback_data.get('comments', {}).get(category, '')
            if comment:
                new_lessons += f"- **Erfolgreiche Praxis:** {comment}\n"
            
            new_lessons += f"- **Empfehlung:** Diese Herangehensweise sollte als Best Practice dokumentiert und von anderen Agenten übernommen werden.\n\n"
        
        # Zu lessons_learned.md hinzufügen
        updated_content = lessons_content + new_lessons
        with open(lessons_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)
    
    def _generate_improvement_suggestions(self, category: str, rating: int, comment: str) -> List[str]:
        """
        Generiert automatische Verbesserungsvorschläge basierend auf Kategorie und Bewertung
        """
        suggestions = []
        
        category_suggestions = {
            'task_clarity': [
                'Aufgabenbeschreibungen sollten spezifischere Akzeptanzkriterien enthalten',
                'Beispiele für erwartete Ergebnisse hinzufügen',
                'Schritt-für-Schritt-Anleitungen für komplexe Aufgaben erstellen'
            ],
            'process_efficiency': [
                'Automatisierung wiederkehrender Schritte prüfen',
                'Parallele Verarbeitung von unabhängigen Teilaufgaben ermöglichen',
                'Workflow-Optimierung durch Eliminierung redundanter Schritte'
            ],
            'resource_availability': [
                'Ressourcen-Checkliste vor Aufgabenstart implementieren',
                'Automatische Ressourcen-Bereitstellung einrichten',
                'Backup-Ressourcen für kritische Aufgaben definieren'
            ],
            'communication': [
                'Standardisierte Kommunikationsprotokolle einführen',
                'Regelmäßige Status-Updates automatisieren',
                'Zentrale Kommunikationsplattform für Teams einrichten'
            ],
            'tools_and_frameworks': [
                'Evaluation neuer Tools für spezifische Aufgabentypen',
                'Integration zusätzlicher APIs oder Services',
                'Verbesserung der Tool-Dokumentation und Tutorials'
            ],
            'documentation': [
                'Automatische Dokumentationsgenerierung implementieren',
                'Template-basierte Dokumentationsstandards einführen',
                'Regelmäßige Dokumentations-Reviews etablieren'
            ]
        }
        
        base_suggestions = category_suggestions.get(category, [])
        
        # Bewertungsbasierte Anpassungen
        if rating == 1:
            suggestions.extend(base_suggestions)
            suggestions.append(f'Dringende Überarbeitung des {self.feedback_categories.get(category, category)}-Prozesses erforderlich')
        elif rating == 2:
            suggestions.extend(base_suggestions[:2])
            suggestions.append(f'Mittelfristige Verbesserung des {self.feedback_categories.get(category, category)}-Bereichs planen')
        
        # Kommentar-basierte Vorschläge
        if comment and len(comment) > 10:
            if 'zeit' in comment.lower() or 'langsam' in comment.lower():
                suggestions.append('Performance-Optimierung und Zeitmanagement verbessern')
            if 'fehler' in comment.lower() or 'problem' in comment.lower():
                suggestions.append('Robustere Fehlerbehandlung und Validierung implementieren')
            if 'unklar' in comment.lower() or 'verwirrend' in comment.lower():
                suggestions.append('Klarere Anweisungen und bessere Benutzerführung entwickeln')
        
        return suggestions[:3]  # Maximal 3 Vorschläge pro Kategorie
    
    def analyze_feedback_trends(self, days: int = 30) -> Dict[str, Any]:
        """
        Analysiert Feedback-Trends über einen bestimmten Zeitraum
        """
        cutoff_date = datetime.now() - timedelta(days=days)
        feedback_files = []
        
        # Alle Feedback-Dateien sammeln
        if os.path.exists(self.feedback_dir):
            for filename in os.listdir(self.feedback_dir):
                if filename.startswith('feedback_') and filename.endswith('.json'):
                    filepath = os.path.join(self.feedback_dir, filename)
                    try:
                        with open(filepath, 'r', encoding='utf-8') as f:
                            feedback = json.load(f)
                        
                        feedback_date = datetime.fromisoformat(feedback.get('timestamp', ''))
                        if feedback_date >= cutoff_date:
                            feedback_files.append(feedback)
                    except:
                        continue
        
        # Trends analysieren
        analysis = {
            'total_feedback': len(feedback_files),
            'average_ratings': {},
            'category_trends': {},
            'agent_performance': {},
            'common_issues': [],
            'improvement_areas': []
        }
        
        if not feedback_files:
            return analysis
        
        # Durchschnittsbewertungen berechnen
        category_ratings = {category: [] for category in self.feedback_categories.keys()}
        agent_ratings = {}
        
        for feedback in feedback_files:
            ratings = feedback.get('ratings', {})
            agent_id = feedback.get('agent_id', 'unknown')
            
            if agent_id not in agent_ratings:
                agent_ratings[agent_id] = []
            
            for category, rating in ratings.items():
                if category in category_ratings:
                    category_ratings[category].append(rating)
                    agent_ratings[agent_id].append(rating)
        
        # Durchschnitte berechnen
        for category, ratings in category_ratings.items():
            if ratings:
                analysis['average_ratings'][category] = sum(ratings) / len(ratings)
        
        for agent, ratings in agent_ratings.items():
            if ratings:
                analysis['agent_performance'][agent] = sum(ratings) / len(ratings)
        
        # Verbesserungsbereiche identifizieren
        for category, avg_rating in analysis['average_ratings'].items():
            if avg_rating < 3.0:
                analysis['improvement_areas'].append({
                    'category': category,
                    'average_rating': avg_rating,
                    'category_name': self.feedback_categories.get(category, category)
                })
        
        return analysis
    
    def generate_feedback_report(self, days: int = 30) -> str:
        """
        Generiert einen umfassenden Feedback-Bericht
        """
        analysis = self.analyze_feedback_trends(days)
        
        report = "# Feedback-System Bericht\n\n"
        report += f"Zeitraum: Letzte {days} Tage\n"
        report += f"Generiert am: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        # Zusammenfassung
        report += "## Zusammenfassung\n\n"
        report += f"- **Gesamtes Feedback:** {analysis['total_feedback']} Einträge\n"
        report += f"- **Verbesserungsbereiche:** {len(analysis['improvement_areas'])}\n\n"
        
        # Durchschnittsbewertungen
        if analysis['average_ratings']:
            report += "## Durchschnittsbewertungen nach Kategorie\n\n"
            for category, rating in analysis['average_ratings'].items():
                category_name = self.feedback_categories.get(category, category)
                rating_text = self.rating_scale.get(round(rating), f"{rating:.1f}")
                report += f"- **{category_name}:** {rating:.1f}/5 ({rating_text})\n"
            report += "\n"
        
        # Agent Performance
        if analysis['agent_performance']:
            report += "## Agent Performance\n\n"
            sorted_agents = sorted(analysis['agent_performance'].items(), 
                                 key=lambda x: x[1], reverse=True)
            for agent, rating in sorted_agents:
                rating_text = self.rating_scale.get(round(rating), f"{rating:.1f}")
                report += f"- **{agent}:** {rating:.1f}/5 ({rating_text})\n"
            report += "\n"
        
        # Verbesserungsbereiche
        if analysis['improvement_areas']:
            report += "## Prioritäre Verbesserungsbereiche\n\n"
            sorted_areas = sorted(analysis['improvement_areas'], 
                                key=lambda x: x['average_rating'])
            for area in sorted_areas:
                report += f"- **{area['category_name']}:** {area['average_rating']:.1f}/5\n"
            report += "\n"
        
        # Empfehlungen
        report += "## Empfehlungen\n\n"
        if analysis['improvement_areas']:
            report += "### Sofortige Maßnahmen\n"
            for area in analysis['improvement_areas'][:3]:
                if area['average_rating'] < 2.5:
                    report += f"- Dringende Verbesserung: {area['category_name']}\n"
            report += "\n"
        
        if analysis['agent_performance']:
            best_agent = max(analysis['agent_performance'].items(), key=lambda x: x[1])
            worst_agent = min(analysis['agent_performance'].items(), key=lambda x: x[1])
            
            if best_agent[1] - worst_agent[1] > 1.0:
                report += "### Wissenstransfer\n"
                report += f"- Best Practices von {best_agent[0]} (Rating: {best_agent[1]:.1f}) auf andere Agenten übertragen\n"
                report += f"- Spezielle Unterstützung für {worst_agent[0]} (Rating: {worst_agent[1]:.1f}) bereitstellen\n\n"
        
        return report
    
    def create_feedback_template(self, task_id: str) -> str:
        """
        Erstellt ein Feedback-Template für KI-Agenten
        """
        prompts = self.generate_automated_feedback_prompt(task_id)
        
        if 'error' in prompts:
            return f"Fehler: {prompts['error']}"
        
        template = f"# Feedback-Template für Task: {prompts['task_title']}\n\n"
        template += f"**Task ID:** {task_id}\n"
        template += f"**Agent ID:** [Ihr Agent-Name]\n"
        template += f"**Datum:** {datetime.now().strftime('%Y-%m-%d')}\n\n"
        
        template += "## Bewertungen\n\n"
        template += "Bitte bewerten Sie jeden Aspekt auf einer Skala von 1-5:\n\n"
        
        for category, prompt_data in prompts['prompts'].items():
            category_name = self.feedback_categories.get(category, category)
            template += f"### {category_name}\n"
            template += f"**Frage:** {prompt_data['question']}\n"
            template += f"**Bewertung (1-5):** [Ihre Bewertung]\n"
            template += f"**Kommentar:** [Ihr Kommentar]\n\n"
        
        template += "## Zusätzliche Verbesserungsvorschläge\n\n"
        template += "- [Vorschlag 1]\n"
        template += "- [Vorschlag 2]\n"
        template += "- [Vorschlag 3]\n\n"
        
        return template

if __name__ == '__main__':
    # Test des Feedback-Systems
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    feedback_system = FeedbackSystem(project_root)
    
    print("=== Feedback-System Test ===")
    
    # Template generieren
    template = feedback_system.create_feedback_template('task_001_setup')
    print(f"Template generiert: {len(template)} Zeichen")
    
    # Trends analysieren
    trends = feedback_system.analyze_feedback_trends(30)
    print(f"Feedback-Trends: {trends['total_feedback']} Einträge")
    
    # Bericht generieren
    report = feedback_system.generate_feedback_report(30)
    print(f"Bericht generiert: {len(report)} Zeichen")

