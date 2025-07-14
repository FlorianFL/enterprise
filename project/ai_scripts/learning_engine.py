import json
import os
import re
from datetime import datetime, timedelta
from typing import List, Dict, Any, Tuple
from collections import defaultdict, Counter

class LearningEngine:
    """
    Adaptive Lernmechanismen für KI-Agenten
    Analysiert Lessons Learned und History-Daten für proaktive Verbesserungen
    """
    
    def __init__(self, project_root: str):
        self.project_root = project_root
        self.manifest_path = os.path.join(project_root, 'project_manifest.json')
        self.history_dir = os.path.join(project_root, 'history')
        self.knowledge_base_dir = os.path.join(project_root, 'knowledge_base')
        self.lessons_learned_path = os.path.join(self.knowledge_base_dir, 'lessons_learned.md')
        self.known_issues_path = os.path.join(self.knowledge_base_dir, 'known_issues.md')
        self.ideas_path = os.path.join(self.knowledge_base_dir, 'ideas.md')
        
        # Pattern für häufige Probleme
        self.error_patterns = [
            r'error|fehler|problem|issue',
            r'failed|fehlgeschlagen|gescheitert',
            r'timeout|zeitüberschreitung',
            r'connection|verbindung.*problem',
            r'permission|berechtigung.*denied',
            r'not found|nicht gefunden',
            r'invalid|ungültig',
            r'conflict|konflikt'
        ]
        
        # Pattern für Erfolgs-Indikatoren
        self.success_patterns = [
            r'completed|abgeschlossen|erfolgreich',
            r'success|erfolg',
            r'finished|beendet',
            r'resolved|gelöst',
            r'optimized|optimiert',
            r'improved|verbessert'
        ]
    
    def load_manifest(self) -> Dict[str, Any]:
        """Lädt das project_manifest.json"""
        with open(self.manifest_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def load_knowledge_base_file(self, file_path: str) -> str:
        """Lädt eine Knowledge Base Datei"""
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        return ""
    
    def save_knowledge_base_file(self, file_path: str, content: str) -> None:
        """Speichert eine Knowledge Base Datei"""
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
    
    def analyze_history_logs(self) -> Dict[str, Any]:
        """
        Analysiert alle History-Logs für Muster und Trends
        """
        analysis = {
            'total_logs': 0,
            'error_frequency': defaultdict(int),
            'success_patterns': defaultdict(int),
            'agent_performance': defaultdict(lambda: {'errors': 0, 'successes': 0}),
            'time_patterns': defaultdict(int),
            'task_patterns': defaultdict(int),
            'recent_issues': []
        }
        
        if not os.path.exists(self.history_dir):
            return analysis
        
        # Alle Log-Dateien durchgehen
        for log_file in os.listdir(self.history_dir):
            if log_file.endswith('.log'):
                log_path = os.path.join(self.history_dir, log_file)
                analysis['total_logs'] += 1
                
                # Log-Inhalt analysieren
                with open(log_path, 'r', encoding='utf-8') as f:
                    content = f.read().lower()
                
                # Agent aus Dateiname extrahieren
                agent_match = re.search(r'ai_agent_(\w+)', log_file.lower())
                agent_name = agent_match.group(1) if agent_match else 'unknown'
                
                # Fehler-Pattern suchen
                for pattern in self.error_patterns:
                    matches = re.findall(pattern, content, re.IGNORECASE)
                    if matches:
                        analysis['error_frequency'][pattern] += len(matches)
                        analysis['agent_performance'][agent_name]['errors'] += len(matches)
                
                # Erfolgs-Pattern suchen
                for pattern in self.success_patterns:
                    matches = re.findall(pattern, content, re.IGNORECASE)
                    if matches:
                        analysis['success_patterns'][pattern] += len(matches)
                        analysis['agent_performance'][agent_name]['successes'] += len(matches)
                
                # Zeitbasierte Analyse (aus Dateiname)
                time_match = re.search(r'(\d{4}-\d{2}-\d{2})', log_file)
                if time_match:
                    date_str = time_match.group(1)
                    analysis['time_patterns'][date_str] += 1
                
                # Task-Pattern analysieren
                task_match = re.search(r'task_(\w+)', log_file.lower())
                if task_match:
                    task_type = task_match.group(1)
                    analysis['task_patterns'][task_type] += 1
                
                # Aktuelle Probleme (letzte 7 Tage)
                try:
                    file_date = datetime.strptime(time_match.group(1), '%Y-%m-%d')
                    if datetime.now() - file_date <= timedelta(days=7):
                        for pattern in self.error_patterns:
                            if re.search(pattern, content, re.IGNORECASE):
                                analysis['recent_issues'].append({
                                    'date': date_str,
                                    'agent': agent_name,
                                    'file': log_file,
                                    'pattern': pattern
                                })
                except:
                    pass
        
        return analysis
    
    def extract_lessons_learned(self) -> List[Dict[str, Any]]:
        """
        Extrahiert und strukturiert Lessons Learned
        """
        lessons_content = self.load_knowledge_base_file(self.lessons_learned_path)
        lessons = []
        
        # Einfache Extraktion von Lessons (kann erweitert werden)
        lines = lessons_content.split('\n')
        current_lesson = None
        
        for line in lines:
            line = line.strip()
            if line.startswith('##') or line.startswith('###'):
                if current_lesson:
                    lessons.append(current_lesson)
                current_lesson = {
                    'title': line.replace('#', '').strip(),
                    'content': '',
                    'keywords': [],
                    'category': self._categorize_lesson(line)
                }
            elif current_lesson and line:
                current_lesson['content'] += line + ' '
        
        if current_lesson:
            lessons.append(current_lesson)
        
        # Keywords extrahieren
        for lesson in lessons:
            lesson['keywords'] = self._extract_keywords(lesson['content'])
        
        return lessons
    
    def _categorize_lesson(self, title: str) -> str:
        """Kategorisiert eine Lesson basierend auf dem Titel"""
        title_lower = title.lower()
        
        if any(word in title_lower for word in ['fehler', 'error', 'problem', 'issue']):
            return 'error_handling'
        elif any(word in title_lower for word in ['optimierung', 'optimization', 'performance']):
            return 'optimization'
        elif any(word in title_lower for word in ['kommunikation', 'communication', 'team']):
            return 'communication'
        elif any(word in title_lower for word in ['prozess', 'process', 'workflow']):
            return 'process'
        else:
            return 'general'
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extrahiert wichtige Keywords aus einem Text"""
        # Einfache Keyword-Extraktion (kann mit NLP verbessert werden)
        important_words = []
        words = re.findall(r'\b\w{4,}\b', text.lower())
        
        # Häufige Wörter zählen
        word_counts = Counter(words)
        
        # Top Keywords (ohne Stoppwörter)
        stopwords = {'dass', 'eine', 'einer', 'eines', 'sind', 'wird', 'wurde', 'werden', 
                    'haben', 'hatte', 'können', 'sollte', 'würde', 'durch', 'über', 'unter'}
        
        for word, count in word_counts.most_common(10):
            if word not in stopwords and len(word) > 3:
                important_words.append(word)
        
        return important_words[:5]  # Top 5 Keywords
    
    def identify_recurring_issues(self) -> List[Dict[str, Any]]:
        """
        Identifiziert wiederkehrende Probleme aus History und Known Issues
        """
        history_analysis = self.analyze_history_logs()
        known_issues_content = self.load_knowledge_base_file(self.known_issues_path)
        
        recurring_issues = []
        
        # Aus History-Analyse
        for pattern, frequency in history_analysis['error_frequency'].items():
            if frequency >= 3:  # Mindestens 3 Vorkommen
                recurring_issues.append({
                    'type': 'history_pattern',
                    'pattern': pattern,
                    'frequency': frequency,
                    'severity': 'high' if frequency >= 5 else 'medium',
                    'source': 'history_logs',
                    'recommendation': self._generate_issue_recommendation(pattern, frequency)
                })
        
        # Aus Known Issues
        known_issues_lines = known_issues_content.split('\n')
        for line in known_issues_lines:
            if line.strip() and not line.startswith('#'):
                # Einfache Heuristik: Zeilen mit "häufig", "oft", "wiederholt"
                if any(word in line.lower() for word in ['häufig', 'oft', 'wiederholt', 'regelmäßig']):
                    recurring_issues.append({
                        'type': 'documented_issue',
                        'description': line.strip(),
                        'severity': 'medium',
                        'source': 'known_issues',
                        'recommendation': 'Überprüfung und mögliche Automatisierung der Lösung'
                    })
        
        return recurring_issues
    
    def _generate_issue_recommendation(self, pattern: str, frequency: int) -> str:
        """Generiert Empfehlungen basierend auf Fehlermustern"""
        recommendations = {
            'error|fehler|problem|issue': 'Implementierung robusterer Fehlerbehandlung und Logging',
            'timeout|zeitüberschreitung': 'Erhöhung der Timeout-Werte oder Implementierung von Retry-Mechanismen',
            'connection|verbindung.*problem': 'Verbesserung der Netzwerk-Resilienz und Connection-Pooling',
            'permission|berechtigung.*denied': 'Überprüfung und Anpassung der Zugriffsberechtigungen',
            'not found|nicht gefunden': 'Implementierung besserer Validierung und Existenzprüfungen',
            'conflict|konflikt': 'Verbesserung der Synchronisation und Konfliktlösung'
        }
        
        for pattern_key, recommendation in recommendations.items():
            if re.search(pattern_key, pattern, re.IGNORECASE):
                return f"{recommendation} (Häufigkeit: {frequency}x)"
        
        return f"Detaillierte Analyse des Musters '{pattern}' erforderlich (Häufigkeit: {frequency}x)"
    
    def generate_proactive_warnings(self) -> List[Dict[str, Any]]:
        """
        Generiert proaktive Warnungen basierend auf Lernmustern
        """
        warnings = []
        history_analysis = self.analyze_history_logs()
        lessons = self.extract_lessons_learned()
        recurring_issues = self.identify_recurring_issues()
        
        # Warnung bei häufigen Fehlern
        for issue in recurring_issues:
            if issue['severity'] == 'high':
                warnings.append({
                    'type': 'high_frequency_error',
                    'message': f"Häufiges Problem erkannt: {issue.get('pattern', issue.get('description'))}",
                    'recommendation': issue['recommendation'],
                    'priority': 'high'
                })
        
        # Warnung bei schlechter Agent-Performance
        for agent, performance in history_analysis['agent_performance'].items():
            total_actions = performance['errors'] + performance['successes']
            if total_actions > 5:  # Mindestens 5 Aktionen
                error_rate = performance['errors'] / total_actions
                if error_rate > 0.3:  # Mehr als 30% Fehlerrate
                    warnings.append({
                        'type': 'agent_performance',
                        'message': f"Agent {agent} zeigt hohe Fehlerrate ({error_rate:.1%})",
                        'recommendation': f"Überprüfung der Konfiguration und Fähigkeiten von {agent}",
                        'priority': 'medium'
                    })
        
        # Warnung bei fehlenden Lessons Learned
        if len(lessons) < 3:
            warnings.append({
                'type': 'insufficient_learning',
                'message': "Wenige dokumentierte Lessons Learned gefunden",
                'recommendation': "KI-Agenten sollten mehr Erkenntnisse dokumentieren",
                'priority': 'low'
            })
        
        return warnings
    
    def suggest_improvements(self) -> List[Dict[str, Any]]:
        """
        Schlägt Verbesserungen basierend auf Lernmustern vor
        """
        improvements = []
        history_analysis = self.analyze_history_logs()
        lessons = self.extract_lessons_learned()
        
        # Verbesserungen basierend auf Lessons Learned
        lesson_categories = defaultdict(int)
        for lesson in lessons:
            lesson_categories[lesson['category']] += 1
        
        # Wenn viele Error-Handling Lessons, schlage Verbesserungen vor
        if lesson_categories['error_handling'] >= 2:
            improvements.append({
                'category': 'error_handling',
                'suggestion': 'Implementierung eines zentralen Error-Handling-Systems',
                'rationale': f"{lesson_categories['error_handling']} Lessons zu Fehlerbehandlung gefunden",
                'impact': 'high'
            })
        
        # Wenn viele Optimierungs-Lessons, schlage Automatisierung vor
        if lesson_categories['optimization'] >= 2:
            improvements.append({
                'category': 'automation',
                'suggestion': 'Automatisierung häufig optimierter Prozesse',
                'rationale': f"{lesson_categories['optimization']} Optimierungs-Lessons gefunden",
                'impact': 'medium'
            })
        
        # Verbesserungen basierend auf Agent-Performance
        best_agents = []
        for agent, performance in history_analysis['agent_performance'].items():
            total_actions = performance['errors'] + performance['successes']
            if total_actions > 3:
                success_rate = performance['successes'] / total_actions
                if success_rate > 0.8:
                    best_agents.append((agent, success_rate))
        
        if best_agents:
            best_agent = max(best_agents, key=lambda x: x[1])
            improvements.append({
                'category': 'knowledge_transfer',
                'suggestion': f'Übertragung der Best Practices von {best_agent[0]} auf andere Agenten',
                'rationale': f'{best_agent[0]} zeigt {best_agent[1]:.1%} Erfolgsrate',
                'impact': 'medium'
            })
        
        return improvements
    
    def update_ai_guidelines(self) -> str:
        """
        Generiert Vorschläge für AI_GUIDELINES.md Updates
        """
        warnings = self.generate_proactive_warnings()
        improvements = self.suggest_improvements()
        recurring_issues = self.identify_recurring_issues()
        
        guidelines_update = "# Vorgeschlagene AI_GUIDELINES.md Updates\n\n"
        guidelines_update += f"Generiert am: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        if warnings:
            guidelines_update += "## Neue Warnhinweise\n\n"
            for warning in warnings:
                guidelines_update += f"### {warning['type'].replace('_', ' ').title()}\n"
                guidelines_update += f"- **Warnung:** {warning['message']}\n"
                guidelines_update += f"- **Empfehlung:** {warning['recommendation']}\n"
                guidelines_update += f"- **Priorität:** {warning['priority']}\n\n"
        
        if recurring_issues:
            guidelines_update += "## Bekannte wiederkehrende Probleme\n\n"
            for issue in recurring_issues[:5]:  # Top 5
                guidelines_update += f"- **Problem:** {issue.get('pattern', issue.get('description'))}\n"
                guidelines_update += f"  - **Empfehlung:** {issue['recommendation']}\n\n"
        
        if improvements:
            guidelines_update += "## Verbesserungsvorschläge\n\n"
            for improvement in improvements:
                guidelines_update += f"### {improvement['category'].replace('_', ' ').title()}\n"
                guidelines_update += f"- **Vorschlag:** {improvement['suggestion']}\n"
                guidelines_update += f"- **Begründung:** {improvement['rationale']}\n"
                guidelines_update += f"- **Impact:** {improvement['impact']}\n\n"
        
        return guidelines_update
    
    def generate_learning_report(self) -> str:
        """
        Generiert einen umfassenden Lernbericht
        """
        history_analysis = self.analyze_history_logs()
        lessons = self.extract_lessons_learned()
        warnings = self.generate_proactive_warnings()
        improvements = self.suggest_improvements()
        
        report = "# Adaptive Lern-Engine Bericht\n\n"
        report += f"Generiert am: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        # Zusammenfassung
        report += "## Zusammenfassung\n\n"
        report += f"- **Analysierte Log-Dateien:** {history_analysis['total_logs']}\n"
        report += f"- **Dokumentierte Lessons Learned:** {len(lessons)}\n"
        report += f"- **Identifizierte Warnungen:** {len(warnings)}\n"
        report += f"- **Verbesserungsvorschläge:** {len(improvements)}\n\n"
        
        # Top Fehler-Pattern
        if history_analysis['error_frequency']:
            report += "## Häufigste Fehler-Pattern\n\n"
            sorted_errors = sorted(history_analysis['error_frequency'].items(), 
                                 key=lambda x: x[1], reverse=True)
            for pattern, frequency in sorted_errors[:5]:
                report += f"- **{pattern}:** {frequency} Vorkommen\n"
            report += "\n"
        
        # Agent Performance
        if history_analysis['agent_performance']:
            report += "## Agent Performance\n\n"
            for agent, performance in history_analysis['agent_performance'].items():
                total = performance['errors'] + performance['successes']
                if total > 0:
                    success_rate = performance['successes'] / total
                    report += f"- **{agent}:** {success_rate:.1%} Erfolgsrate ({total} Aktionen)\n"
            report += "\n"
        
        # Lessons Learned Kategorien
        if lessons:
            report += "## Lessons Learned Kategorien\n\n"
            categories = defaultdict(int)
            for lesson in lessons:
                categories[lesson['category']] += 1
            
            for category, count in categories.items():
                report += f"- **{category.replace('_', ' ').title()}:** {count} Lessons\n"
            report += "\n"
        
        return report

if __name__ == '__main__':
    # Test der Learning Engine
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    engine = LearningEngine(project_root)
    
    print("=== Learning Engine Test ===")
    
    # History-Analyse
    analysis = engine.analyze_history_logs()
    print(f"Analysierte Logs: {analysis['total_logs']}")
    
    # Warnungen generieren
    warnings = engine.generate_proactive_warnings()
    print(f"Generierte Warnungen: {len(warnings)}")
    
    # Verbesserungen vorschlagen
    improvements = engine.suggest_improvements()
    print(f"Verbesserungsvorschläge: {len(improvements)}")
    
    # Bericht generieren
    report = engine.generate_learning_report()
    print(f"Bericht generiert: {len(report)} Zeichen")

