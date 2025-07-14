import json
import os
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Set, Tuple
import re
from pathlib import Path

class DocumentationChecker:
    """
    Automatisierte Dokumentations-Checks für das Framework
    Prüft ob alle relevanten Dokumente nach Task- oder Regel-Updates aktualisiert wurden
    """
    
    def __init__(self, project_root: str):
        self.project_root = project_root
        self.manifest_path = os.path.join(project_root, 'project_manifest.json')
        self.history_dir = os.path.join(project_root, 'history')
        self.knowledge_base_dir = os.path.join(project_root, 'knowledge_base')
        self.tasks_dir = os.path.join(project_root, 'tasks')
        self.guidelines_path = os.path.join(project_root, 'AI_GUIDELINES.md')
        
        # Dokumentations-Abhängigkeiten
        self.documentation_dependencies = {
            'task_completion': {
                'required_updates': [
                    'history/',
                    'knowledge_base/lessons_learned.md',
                    'project_manifest.json'
                ],
                'optional_updates': [
                    'knowledge_base/ideas.md',
                    'knowledge_base/known_issues.md'
                ],
                'check_interval_hours': 1
            },
            'rule_change': {
                'required_updates': [
                    'history/',
                    'knowledge_base/ideas.md'
                ],
                'optional_updates': [
                    'knowledge_base/lessons_learned.md'
                ],
                'check_interval_hours': 0.5
            },
            'team_structure_change': {
                'required_updates': [
                    'history/',
                    'project_manifest.json'
                ],
                'optional_updates': [
                    'knowledge_base/ideas.md'
                ],
                'check_interval_hours': 1
            },
            'new_task_creation': {
                'required_updates': [
                    'tasks/',
                    'project_manifest.json',
                    'history/'
                ],
                'optional_updates': [],
                'check_interval_hours': 0.25
            }
        }
        
        # Dokumentations-Standards
        self.documentation_standards = {
            'lessons_learned.md': {
                'min_sections': 2,
                'required_patterns': [r'##\s+.+', r'###\s+.+'],
                'max_age_days': 7
            },
            'ideas.md': {
                'min_sections': 1,
                'required_patterns': [r'##\s+.+'],
                'max_age_days': 14
            },
            'known_issues.md': {
                'min_sections': 1,
                'required_patterns': [r'##\s+.+', r'-\s+.+'],
                'max_age_days': 30
            }
        }
        
        # Check-Ergebnisse Cache
        self.check_cache = {}
        self.cache_duration = timedelta(minutes=30)
    
    def load_manifest(self) -> Dict[str, Any]:
        """Lädt das project_manifest.json"""
        with open(self.manifest_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def get_file_modification_time(self, file_path: str) -> Optional[datetime]:
        """Holt die letzte Änderungszeit einer Datei"""
        if os.path.exists(file_path):
            timestamp = os.path.getmtime(file_path)
            return datetime.fromtimestamp(timestamp)
        return None
    
    def get_directory_latest_modification(self, dir_path: str) -> Optional[datetime]:
        """Holt die neueste Änderungszeit in einem Verzeichnis"""
        if not os.path.exists(dir_path):
            return None
        
        latest_time = None
        
        for root, dirs, files in os.walk(dir_path):
            for file in files:
                file_path = os.path.join(root, file)
                file_time = self.get_file_modification_time(file_path)
                
                if file_time and (latest_time is None or file_time > latest_time):
                    latest_time = file_time
        
        return latest_time
    
    def detect_recent_changes(self, hours: int = 24) -> Dict[str, List[Dict[str, Any]]]:
        """Erkennt kürzliche Änderungen an wichtigen Dateien"""
        cutoff_time = datetime.now() - timedelta(hours=hours)
        changes = {
            'task_completion': [],
            'rule_change': [],
            'team_structure_change': [],
            'new_task_creation': []
        }
        
        # Manifest-Änderungen prüfen
        manifest_time = self.get_file_modification_time(self.manifest_path)
        if manifest_time and manifest_time > cutoff_time:
            manifest = self.load_manifest()
            
            # Prüfe auf verschiedene Änderungstypen
            completed_tasks = [t for t in manifest.get('tasks', []) if t.get('status') == 'completed']
            if completed_tasks:
                for task in completed_tasks:
                    if task.get('completed_date'):
                        try:
                            completed_date = datetime.fromisoformat(task['completed_date'])
                            if completed_date > cutoff_time:
                                changes['task_completion'].append({
                                    'type': 'task_completed',
                                    'task_id': task.get('task_id'),
                                    'timestamp': completed_date,
                                    'details': task
                                })
                        except:
                            pass
            
            # Neue Tasks
            new_tasks = [t for t in manifest.get('tasks', []) if t.get('status') == 'open']
            for task in new_tasks:
                changes['new_task_creation'].append({
                    'type': 'new_task',
                    'task_id': task.get('task_id'),
                    'timestamp': manifest_time,
                    'details': task
                })
            
            # Team-Struktur Änderungen
            teams = manifest.get('teams', [])
            if teams:
                changes['team_structure_change'].append({
                    'type': 'team_update',
                    'timestamp': manifest_time,
                    'details': {'team_count': len(teams)}
                })
        
        # Guidelines-Änderungen prüfen
        guidelines_time = self.get_file_modification_time(self.guidelines_path)
        if guidelines_time and guidelines_time > cutoff_time:
            changes['rule_change'].append({
                'type': 'guidelines_updated',
                'timestamp': guidelines_time,
                'details': {'file': 'AI_GUIDELINES.md'}
            })
        
        # History-Änderungen prüfen
        history_time = self.get_directory_latest_modification(self.history_dir)
        if history_time and history_time > cutoff_time:
            # Neue Log-Dateien könnten auf Task-Completion hinweisen
            for filename in os.listdir(self.history_dir):
                if filename.endswith('.log'):
                    file_path = os.path.join(self.history_dir, filename)
                    file_time = self.get_file_modification_time(file_path)
                    
                    if file_time and file_time > cutoff_time:
                        # Versuche Task-ID aus Dateiname zu extrahieren
                        task_match = re.search(r'task_(\w+)', filename)
                        if task_match:
                            task_id = task_match.group(1)
                            changes['task_completion'].append({
                                'type': 'task_activity',
                                'task_id': task_id,
                                'timestamp': file_time,
                                'details': {'log_file': filename}
                            })
        
        return changes
    
    def check_documentation_completeness(self, change_type: str, change_details: Dict[str, Any]) -> Dict[str, Any]:
        """Prüft ob die Dokumentation für eine Änderung vollständig ist"""
        if change_type not in self.documentation_dependencies:
            return {'status': 'unknown', 'message': f'Unbekannter Änderungstyp: {change_type}'}
        
        deps = self.documentation_dependencies[change_type]
        check_time = change_details.get('timestamp', datetime.now())
        
        if isinstance(check_time, str):
            check_time = datetime.fromisoformat(check_time)
        
        results = {
            'status': 'complete',
            'missing_required': [],
            'missing_optional': [],
            'outdated_files': [],
            'recommendations': []
        }
        
        # Prüfe erforderliche Updates
        for required_path in deps['required_updates']:
            full_path = os.path.join(self.project_root, required_path)
            
            if required_path.endswith('/'):
                # Verzeichnis - prüfe neueste Datei
                latest_time = self.get_directory_latest_modification(full_path)
                if not latest_time or latest_time < check_time:
                    results['missing_required'].append(required_path)
                    results['status'] = 'incomplete'
            else:
                # Einzelne Datei
                file_time = self.get_file_modification_time(full_path)
                if not file_time or file_time < check_time:
                    results['missing_required'].append(required_path)
                    results['status'] = 'incomplete'
        
        # Prüfe optionale Updates
        for optional_path in deps['optional_updates']:
            full_path = os.path.join(self.project_root, optional_path)
            
            if optional_path.endswith('/'):
                latest_time = self.get_directory_latest_modification(full_path)
                if not latest_time or latest_time < check_time:
                    results['missing_optional'].append(optional_path)
            else:
                file_time = self.get_file_modification_time(full_path)
                if not file_time or file_time < check_time:
                    results['missing_optional'].append(optional_path)
        
        # Generiere Empfehlungen
        if results['missing_required']:
            results['recommendations'].append(
                f"Erforderliche Dokumentation fehlt: {', '.join(results['missing_required'])}"
            )
        
        if results['missing_optional']:
            results['recommendations'].append(
                f"Optionale Dokumentation könnte aktualisiert werden: {', '.join(results['missing_optional'])}"
            )
        
        return results
    
    def validate_documentation_quality(self, file_path: str) -> Dict[str, Any]:
        """Validiert die Qualität einer Dokumentationsdatei"""
        filename = os.path.basename(file_path)
        
        if filename not in self.documentation_standards:
            return {'status': 'no_standards', 'message': f'Keine Standards für {filename} definiert'}
        
        standards = self.documentation_standards[filename]
        
        if not os.path.exists(file_path):
            return {'status': 'missing', 'message': f'Datei {filename} existiert nicht'}
        
        # Datei-Alter prüfen
        file_time = self.get_file_modification_time(file_path)
        if file_time:
            age_days = (datetime.now() - file_time).days
            if age_days > standards['max_age_days']:
                return {
                    'status': 'outdated',
                    'message': f'Datei ist {age_days} Tage alt (Maximum: {standards["max_age_days"]})'
                }
        
        # Inhalt prüfen
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        results = {
            'status': 'valid',
            'issues': [],
            'suggestions': []
        }
        
        # Pattern prüfen
        for pattern in standards['required_patterns']:
            matches = re.findall(pattern, content, re.MULTILINE)
            if not matches:
                results['issues'].append(f'Erforderliches Pattern fehlt: {pattern}')
                results['status'] = 'invalid'
        
        # Mindest-Abschnitte prüfen
        section_count = len(re.findall(r'^#+\s+.+$', content, re.MULTILINE))
        if section_count < standards['min_sections']:
            results['issues'].append(
                f'Zu wenige Abschnitte: {section_count} (Minimum: {standards["min_sections"]})'
            )
            results['status'] = 'invalid'
        
        # Inhaltslänge prüfen
        if len(content.strip()) < 100:
            results['suggestions'].append('Dokumentation könnte detaillierter sein')
        
        # Aktualität prüfen
        if file_time and (datetime.now() - file_time).days > 7:
            results['suggestions'].append('Dokumentation könnte aktualisiert werden')
        
        return results
    
    def run_comprehensive_check(self, hours: int = 24) -> Dict[str, Any]:
        """Führt eine umfassende Dokumentationsprüfung durch"""
        # Cache prüfen
        cache_key = f'comprehensive_check_{hours}'
        if cache_key in self.check_cache:
            cache_time, cache_result = self.check_cache[cache_key]
            if datetime.now() - cache_time < self.cache_duration:
                return cache_result
        
        results = {
            'timestamp': datetime.now().isoformat(),
            'check_period_hours': hours,
            'changes_detected': {},
            'documentation_status': {},
            'quality_issues': {},
            'recommendations': [],
            'summary': {
                'total_changes': 0,
                'complete_documentation': 0,
                'incomplete_documentation': 0,
                'quality_issues_count': 0
            }
        }
        
        # Erkenne Änderungen
        changes = self.detect_recent_changes(hours)
        results['changes_detected'] = changes
        
        # Prüfe Dokumentation für jede Änderung
        for change_type, change_list in changes.items():
            results['summary']['total_changes'] += len(change_list)
            
            for change in change_list:
                check_result = self.check_documentation_completeness(change_type, change)
                
                change_key = f"{change_type}_{change.get('task_id', 'general')}_{change['timestamp']}"
                results['documentation_status'][change_key] = check_result
                
                if check_result['status'] == 'complete':
                    results['summary']['complete_documentation'] += 1
                else:
                    results['summary']['incomplete_documentation'] += 1
                
                # Empfehlungen sammeln
                results['recommendations'].extend(check_result.get('recommendations', []))
        
        # Prüfe Qualität der Knowledge Base Dateien
        kb_files = ['lessons_learned.md', 'ideas.md', 'known_issues.md']
        for kb_file in kb_files:
            file_path = os.path.join(self.knowledge_base_dir, kb_file)
            quality_result = self.validate_documentation_quality(file_path)
            
            results['quality_issues'][kb_file] = quality_result
            
            if quality_result['status'] in ['invalid', 'outdated', 'missing']:
                results['summary']['quality_issues_count'] += 1
                
                if quality_result.get('issues'):
                    results['recommendations'].extend([
                        f"{kb_file}: {issue}" for issue in quality_result['issues']
                    ])
        
        # Cache Ergebnis
        self.check_cache[cache_key] = (datetime.now(), results)
        
        return results
    
    def generate_documentation_reminder(self, agent_id: str, task_id: str = None) -> str:
        """Generiert eine Erinnerung für fehlende Dokumentation"""
        check_results = self.run_comprehensive_check(hours=6)
        
        reminder = f"# Dokumentations-Erinnerung für {agent_id}\n\n"
        reminder += f"Generiert am: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        incomplete_docs = []
        quality_issues = []
        
        # Sammle unvollständige Dokumentation
        for change_key, status in check_results['documentation_status'].items():
            if status['status'] != 'complete':
                if task_id and task_id not in change_key:
                    continue
                
                incomplete_docs.append({
                    'change': change_key,
                    'missing_required': status.get('missing_required', []),
                    'missing_optional': status.get('missing_optional', []),
                    'recommendations': status.get('recommendations', [])
                })
        
        # Sammle Qualitätsprobleme
        for file, quality in check_results['quality_issues'].items():
            if quality['status'] in ['invalid', 'outdated', 'missing']:
                quality_issues.append({
                    'file': file,
                    'status': quality['status'],
                    'issues': quality.get('issues', []),
                    'suggestions': quality.get('suggestions', [])
                })
        
        if not incomplete_docs and not quality_issues:
            reminder += "✅ Alle Dokumentation ist aktuell und vollständig!\n\n"
            return reminder
        
        # Unvollständige Dokumentation
        if incomplete_docs:
            reminder += "## ⚠️ Fehlende oder unvollständige Dokumentation\n\n"
            
            for doc in incomplete_docs:
                reminder += f"### {doc['change']}\n"
                
                if doc['missing_required']:
                    reminder += "**Erforderliche Updates fehlen:**\n"
                    for missing in doc['missing_required']:
                        reminder += f"- {missing}\n"
                    reminder += "\n"
                
                if doc['missing_optional']:
                    reminder += "**Optionale Updates empfohlen:**\n"
                    for missing in doc['missing_optional']:
                        reminder += f"- {missing}\n"
                    reminder += "\n"
                
                if doc['recommendations']:
                    reminder += "**Empfehlungen:**\n"
                    for rec in doc['recommendations']:
                        reminder += f"- {rec}\n"
                    reminder += "\n"
        
        # Qualitätsprobleme
        if quality_issues:
            reminder += "## 📋 Dokumentationsqualität\n\n"
            
            for issue in quality_issues:
                status_emoji = {
                    'missing': '❌',
                    'outdated': '⏰',
                    'invalid': '⚠️'
                }.get(issue['status'], '❓')
                
                reminder += f"### {status_emoji} {issue['file']}\n"
                reminder += f"**Status:** {issue['status']}\n"
                
                if issue['issues']:
                    reminder += "**Probleme:**\n"
                    for problem in issue['issues']:
                        reminder += f"- {problem}\n"
                
                if issue['suggestions']:
                    reminder += "**Verbesserungsvorschläge:**\n"
                    for suggestion in issue['suggestions']:
                        reminder += f"- {suggestion}\n"
                
                reminder += "\n"
        
        # Zusammenfassung
        reminder += "---\n\n"
        reminder += "## Nächste Schritte\n\n"
        reminder += "1. Aktualisieren Sie die fehlenden erforderlichen Dokumente\n"
        reminder += "2. Beheben Sie identifizierte Qualitätsprobleme\n"
        reminder += "3. Erwägen Sie die optionalen Verbesserungen\n"
        reminder += "4. Führen Sie erneut eine Dokumentationsprüfung durch\n\n"
        
        return reminder
    
    def create_documentation_checklist(self, change_type: str) -> str:
        """Erstellt eine Checkliste für Dokumentations-Updates"""
        if change_type not in self.documentation_dependencies:
            return f"Keine Checkliste für Änderungstyp '{change_type}' verfügbar."
        
        deps = self.documentation_dependencies[change_type]
        
        checklist = f"# Dokumentations-Checkliste: {change_type.replace('_', ' ').title()}\n\n"
        checklist += f"Generiert am: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        checklist += "## Erforderliche Updates\n\n"
        for required in deps['required_updates']:
            checklist += f"- [ ] {required}\n"
        
        if deps['optional_updates']:
            checklist += "\n## Optionale Updates\n\n"
            for optional in deps['optional_updates']:
                checklist += f"- [ ] {optional}\n"
        
        checklist += f"\n## Zeitrahmen\n\n"
        checklist += f"Diese Dokumentation sollte innerhalb von {deps['check_interval_hours']} Stunden nach der Änderung aktualisiert werden.\n\n"
        
        # Spezifische Hinweise je nach Typ
        if change_type == 'task_completion':
            checklist += "## Spezifische Hinweise für Task-Completion\n\n"
            checklist += "- Dokumentieren Sie Lessons Learned aus der Aufgabe\n"
            checklist += "- Aktualisieren Sie den Task-Status im Manifest\n"
            checklist += "- Protokollieren Sie alle wichtigen Erkenntnisse\n"
            checklist += "- Fügen Sie Verbesserungsvorschläge zu ideas.md hinzu\n\n"
        
        elif change_type == 'rule_change':
            checklist += "## Spezifische Hinweise für Regel-Änderungen\n\n"
            checklist += "- Dokumentieren Sie die Gründe für die Änderung\n"
            checklist += "- Benachrichtigen Sie alle betroffenen Agenten\n"
            checklist += "- Aktualisieren Sie relevante Prozessdokumentation\n"
            checklist += "- Überwachen Sie die Auswirkungen der Änderung\n\n"
        
        return checklist

if __name__ == '__main__':
    # Test des Documentation Checkers
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    doc_checker = DocumentationChecker(project_root)
    
    print("=== Documentation Checker Test ===")
    
    # Erkenne Änderungen
    changes = doc_checker.detect_recent_changes(24)
    total_changes = sum(len(change_list) for change_list in changes.values())
    print(f"Erkannte Änderungen (24h): {total_changes}")
    
    # Führe umfassende Prüfung durch
    check_results = doc_checker.run_comprehensive_check(24)
    print(f"Dokumentationsstatus: {check_results['summary']}")
    
    # Generiere Erinnerung
    reminder = doc_checker.generate_documentation_reminder('test_agent')
    print(f"Erinnerung generiert: {len(reminder)} Zeichen")

