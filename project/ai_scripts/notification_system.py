import json
import os
import hashlib
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Set
import difflib
import re

class NotificationSystem:
    """
    Transparentes Änderungsbenachrichtigungssystem für KI-Agenten
    Überwacht Änderungen an kritischen Dateien und benachrichtigt alle Agenten
    """
    
    def __init__(self, project_root: str):
        self.project_root = project_root
        self.manifest_path = os.path.join(project_root, 'project_manifest.json')
        self.guidelines_path = os.path.join(project_root, 'AI_GUIDELINES.md')
        self.notifications_dir = os.path.join(project_root, 'notifications')
        self.state_file = os.path.join(self.notifications_dir, 'file_states.json')
        
        # Überwachte Dateien und ihre Prioritäten
        self.monitored_files = {
            'project_manifest.json': {
                'path': self.manifest_path,
                'priority': 'high',
                'description': 'Zentrale Projektkonfiguration',
                'notify_fields': ['ceo_directives', 'teams', 'tasks', 'kill_switch']
            },
            'AI_GUIDELINES.md': {
                'path': self.guidelines_path,
                'priority': 'critical',
                'description': 'KI-Verhaltensregeln und Richtlinien',
                'notify_fields': None  # Alle Änderungen sind wichtig
            }
        }
        
        # Benachrichtigungstypen
        self.notification_types = {
            'rule_change': 'Regeländerung',
            'directive_update': 'CEO-Direktive aktualisiert',
            'team_structure': 'Team-Struktur geändert',
            'task_assignment': 'Aufgabenzuweisung',
            'emergency': 'Notfall-Benachrichtigung',
            'system_update': 'System-Update'
        }
        
        # Stelle sicher, dass Notifications-Verzeichnis existiert
        os.makedirs(self.notifications_dir, exist_ok=True)
        
        # Initialisiere File States wenn nicht vorhanden
        if not os.path.exists(self.state_file):
            self._initialize_file_states()
    
    def _initialize_file_states(self) -> None:
        """Initialisiert die Datei-Zustandsverfolgung"""
        states = {}
        
        for file_key, file_info in self.monitored_files.items():
            if os.path.exists(file_info['path']):
                with open(file_info['path'], 'r', encoding='utf-8') as f:
                    content = f.read()
                
                states[file_key] = {
                    'last_hash': hashlib.md5(content.encode()).hexdigest(),
                    'last_modified': datetime.now().isoformat(),
                    'last_size': len(content)
                }
        
        with open(self.state_file, 'w', encoding='utf-8') as f:
            json.dump(states, f, indent=2)
    
    def _load_file_states(self) -> Dict[str, Any]:
        """Lädt die gespeicherten Datei-Zustände"""
        if os.path.exists(self.state_file):
            with open(self.state_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def _save_file_states(self, states: Dict[str, Any]) -> None:
        """Speichert die Datei-Zustände"""
        with open(self.state_file, 'w', encoding='utf-8') as f:
            json.dump(states, f, indent=2)
    
    def _get_file_hash(self, file_path: str) -> Optional[str]:
        """Berechnet den Hash einer Datei"""
        if not os.path.exists(file_path):
            return None
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return hashlib.md5(content.encode()).hexdigest()
    
    def _detect_changes(self) -> List[Dict[str, Any]]:
        """Erkennt Änderungen an überwachten Dateien"""
        current_states = self._load_file_states()
        changes = []
        
        for file_key, file_info in self.monitored_files.items():
            file_path = file_info['path']
            
            if not os.path.exists(file_path):
                continue
            
            current_hash = self._get_file_hash(file_path)
            stored_state = current_states.get(file_key, {})
            last_hash = stored_state.get('last_hash')
            
            if current_hash != last_hash:
                # Änderung erkannt
                change_info = {
                    'file_key': file_key,
                    'file_path': file_path,
                    'priority': file_info['priority'],
                    'description': file_info['description'],
                    'timestamp': datetime.now().isoformat(),
                    'change_type': self._determine_change_type(file_key, file_path, stored_state),
                    'details': self._analyze_change_details(file_key, file_path, stored_state)
                }
                
                changes.append(change_info)
                
                # Zustand aktualisieren
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                current_states[file_key] = {
                    'last_hash': current_hash,
                    'last_modified': datetime.now().isoformat(),
                    'last_size': len(content)
                }
        
        # Aktualisierte Zustände speichern
        self._save_file_states(current_states)
        
        return changes
    
    def _determine_change_type(self, file_key: str, file_path: str, stored_state: Dict[str, Any]) -> str:
        """Bestimmt den Typ der Änderung"""
        if file_key == 'project_manifest.json':
            return self._analyze_manifest_changes(file_path)
        elif file_key == 'AI_GUIDELINES.md':
            return 'rule_change'
        else:
            return 'system_update'
    
    def _analyze_manifest_changes(self, manifest_path: str) -> str:
        """Analysiert spezifische Änderungen im project_manifest.json"""
        try:
            with open(manifest_path, 'r', encoding='utf-8') as f:
                manifest = json.load(f)
            
            # Prüfe verschiedene Bereiche
            if manifest.get('kill_switch', False):
                return 'emergency'
            
            ceo_directives = manifest.get('ceo_directives', {})
            if any(ceo_directives.values()):
                return 'directive_update'
            
            teams = manifest.get('teams', [])
            if teams:
                return 'team_structure'
            
            tasks = manifest.get('tasks', [])
            recent_tasks = [t for t in tasks if t.get('status') == 'assigned']
            if recent_tasks:
                return 'task_assignment'
            
            return 'system_update'
            
        except:
            return 'system_update'
    
    def _analyze_change_details(self, file_key: str, file_path: str, stored_state: Dict[str, Any]) -> Dict[str, Any]:
        """Analysiert Details der Änderung"""
        details = {
            'summary': '',
            'affected_sections': [],
            'impact_level': 'medium',
            'action_required': False
        }
        
        if file_key == 'project_manifest.json':
            details.update(self._analyze_manifest_details(file_path))
        elif file_key == 'AI_GUIDELINES.md':
            details.update(self._analyze_guidelines_details(file_path, stored_state))
        
        return details
    
    def _analyze_manifest_details(self, manifest_path: str) -> Dict[str, Any]:
        """Analysiert Details von Manifest-Änderungen"""
        try:
            with open(manifest_path, 'r', encoding='utf-8') as f:
                manifest = json.load(f)
            
            details = {
                'summary': 'Projekt-Manifest wurde aktualisiert',
                'affected_sections': [],
                'impact_level': 'medium',
                'action_required': False
            }
            
            # Kill Switch Check
            if manifest.get('kill_switch', False):
                details.update({
                    'summary': 'NOTFALL: Kill-Switch aktiviert - Alle KI-Aktivitäten stoppen',
                    'impact_level': 'critical',
                    'action_required': True,
                    'affected_sections': ['kill_switch']
                })
                return details
            
            # CEO Directives
            ceo_directives = manifest.get('ceo_directives', {})
            if ceo_directives.get('priority_focus'):
                details['affected_sections'].append('priority_focus')
                details['summary'] += f" - Neuer Prioritätsfokus: {ceo_directives['priority_focus']}"
            
            if ceo_directives.get('budget_allocation'):
                details['affected_sections'].append('budget_allocation')
                details['summary'] += " - Budget-Allokation geändert"
            
            if ceo_directives.get('new_hires_needed'):
                details['affected_sections'].append('new_hires_needed')
                details['summary'] += " - Neue KI-Agenten benötigt"
            
            # Teams
            teams = manifest.get('teams', [])
            if teams:
                details['affected_sections'].append('teams')
                details['summary'] += f" - {len(teams)} Teams konfiguriert"
            
            # Tasks
            tasks = manifest.get('tasks', [])
            open_tasks = [t for t in tasks if t.get('status') == 'open']
            assigned_tasks = [t for t in tasks if t.get('status') == 'assigned']
            
            if open_tasks or assigned_tasks:
                details['affected_sections'].append('tasks')
                details['summary'] += f" - {len(open_tasks)} offene, {len(assigned_tasks)} zugewiesene Aufgaben"
            
            # Impact Level bestimmen
            if len(details['affected_sections']) >= 3:
                details['impact_level'] = 'high'
            elif 'priority_focus' in details['affected_sections'] or 'budget_allocation' in details['affected_sections']:
                details['impact_level'] = 'high'
                details['action_required'] = True
            
            return details
            
        except Exception as e:
            return {
                'summary': f'Fehler beim Analysieren der Manifest-Änderungen: {str(e)}',
                'affected_sections': ['unknown'],
                'impact_level': 'medium',
                'action_required': False
            }
    
    def _analyze_guidelines_details(self, guidelines_path: str, stored_state: Dict[str, Any]) -> Dict[str, Any]:
        """Analysiert Details von Guidelines-Änderungen"""
        details = {
            'summary': 'AI Guidelines wurden aktualisiert',
            'affected_sections': [],
            'impact_level': 'high',  # Guidelines-Änderungen sind immer wichtig
            'action_required': True
        }
        
        try:
            with open(guidelines_path, 'r', encoding='utf-8') as f:
                current_content = f.read()
            
            # Versuche, geänderte Abschnitte zu identifizieren
            sections = re.findall(r'^#+\s+(.+)$', current_content, re.MULTILINE)
            details['affected_sections'] = sections[:5]  # Erste 5 Abschnitte
            
            # Größe der Änderung
            current_size = len(current_content)
            last_size = stored_state.get('last_size', 0)
            
            if abs(current_size - last_size) > 1000:  # Große Änderung
                details['impact_level'] = 'critical'
                details['summary'] += ' - Umfangreiche Änderungen erkannt'
            elif current_size > last_size:
                details['summary'] += ' - Neue Regeln hinzugefügt'
            else:
                details['summary'] += ' - Bestehende Regeln modifiziert'
            
        except Exception as e:
            details['summary'] = f'Guidelines geändert (Analyse-Fehler: {str(e)})'
        
        return details
    
    def create_notification(self, change_info: Dict[str, Any]) -> str:
        """Erstellt eine Benachrichtigung für eine Änderung"""
        notification_id = f"notify_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{change_info['file_key']}"
        
        notification = {
            'notification_id': notification_id,
            'timestamp': change_info['timestamp'],
            'type': change_info['change_type'],
            'priority': change_info['priority'],
            'file_changed': change_info['file_key'],
            'summary': change_info['details']['summary'],
            'affected_sections': change_info['details']['affected_sections'],
            'impact_level': change_info['details']['impact_level'],
            'action_required': change_info['details']['action_required'],
            'status': 'active',
            'acknowledged_by': []
        }
        
        # Benachrichtigung speichern
        notification_file = os.path.join(self.notifications_dir, f'{notification_id}.json')
        with open(notification_file, 'w', encoding='utf-8') as f:
            json.dump(notification, f, indent=2, ensure_ascii=False)
        
        return notification_id
    
    def check_for_changes(self) -> List[str]:
        """Prüft auf Änderungen und erstellt Benachrichtigungen"""
        changes = self._detect_changes()
        notification_ids = []
        
        for change in changes:
            notification_id = self.create_notification(change)
            notification_ids.append(notification_id)
        
        return notification_ids
    
    def get_active_notifications(self, agent_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Holt aktive Benachrichtigungen für einen Agenten"""
        notifications = []
        
        if not os.path.exists(self.notifications_dir):
            return notifications
        
        for filename in os.listdir(self.notifications_dir):
            if filename.startswith('notify_') and filename.endswith('.json'):
                filepath = os.path.join(self.notifications_dir, filename)
                
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        notification = json.load(f)
                    
                    # Nur aktive Benachrichtigungen
                    if notification.get('status') == 'active':
                        # Prüfe ob Agent bereits bestätigt hat
                        if agent_id and agent_id not in notification.get('acknowledged_by', []):
                            notifications.append(notification)
                        elif not agent_id:
                            notifications.append(notification)
                            
                except:
                    continue
        
        # Nach Priorität und Zeitstempel sortieren
        priority_order = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3}
        notifications.sort(key=lambda x: (
            priority_order.get(x.get('priority', 'medium'), 2),
            x.get('timestamp', '')
        ), reverse=True)
        
        return notifications
    
    def acknowledge_notification(self, notification_id: str, agent_id: str) -> bool:
        """Bestätigt eine Benachrichtigung für einen Agenten"""
        notification_file = os.path.join(self.notifications_dir, f'{notification_id}.json')
        
        if not os.path.exists(notification_file):
            return False
        
        try:
            with open(notification_file, 'r', encoding='utf-8') as f:
                notification = json.load(f)
            
            acknowledged_by = notification.get('acknowledged_by', [])
            if agent_id not in acknowledged_by:
                acknowledged_by.append(agent_id)
                notification['acknowledged_by'] = acknowledged_by
                notification['last_acknowledged'] = datetime.now().isoformat()
            
            with open(notification_file, 'w', encoding='utf-8') as f:
                json.dump(notification, f, indent=2, ensure_ascii=False)
            
            return True
            
        except:
            return False
    
    def generate_notification_summary(self, agent_id: str) -> str:
        """Generiert eine Zusammenfassung der Benachrichtigungen für einen Agenten"""
        notifications = self.get_active_notifications(agent_id)
        
        if not notifications:
            return "Keine neuen Benachrichtigungen."
        
        summary = f"# Benachrichtigungen für {agent_id}\n\n"
        summary += f"**{len(notifications)} neue Benachrichtigung(en)**\n\n"
        
        # Nach Priorität gruppieren
        by_priority = {}
        for notification in notifications:
            priority = notification.get('priority', 'medium')
            if priority not in by_priority:
                by_priority[priority] = []
            by_priority[priority].append(notification)
        
        # Kritische zuerst
        for priority in ['critical', 'high', 'medium', 'low']:
            if priority in by_priority:
                priority_name = {
                    'critical': '🚨 KRITISCH',
                    'high': '⚠️ HOCH', 
                    'medium': '📋 MITTEL',
                    'low': '💡 NIEDRIG'
                }.get(priority, priority.upper())
                
                summary += f"## {priority_name}\n\n"
                
                for notification in by_priority[priority]:
                    summary += f"### {notification.get('type', 'Unbekannt').replace('_', ' ').title()}\n"
                    summary += f"- **Datei:** {notification.get('file_changed')}\n"
                    summary += f"- **Zusammenfassung:** {notification.get('summary')}\n"
                    summary += f"- **Zeit:** {notification.get('timestamp')}\n"
                    
                    if notification.get('action_required'):
                        summary += f"- **⚡ AKTION ERFORDERLICH**\n"
                    
                    affected_sections = notification.get('affected_sections', [])
                    if affected_sections:
                        summary += f"- **Betroffene Bereiche:** {', '.join(affected_sections)}\n"
                    
                    summary += f"- **Benachrichtigungs-ID:** {notification.get('notification_id')}\n\n"
        
        summary += "---\n\n"
        summary += "**Hinweis:** Verwenden Sie `acknowledge_notification(notification_id, agent_id)` um Benachrichtigungen zu bestätigen.\n"
        
        return summary
    
    def cleanup_old_notifications(self, days: int = 7) -> int:
        """Bereinigt alte Benachrichtigungen"""
        cutoff_date = datetime.now() - timedelta(days=days)
        cleaned_count = 0
        
        if not os.path.exists(self.notifications_dir):
            return 0
        
        for filename in os.listdir(self.notifications_dir):
            if filename.startswith('notify_') and filename.endswith('.json'):
                filepath = os.path.join(self.notifications_dir, filename)
                
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        notification = json.load(f)
                    
                    notification_date = datetime.fromisoformat(notification.get('timestamp', ''))
                    
                    if notification_date < cutoff_date:
                        os.remove(filepath)
                        cleaned_count += 1
                        
                except:
                    continue
        
        return cleaned_count
    
    def create_emergency_notification(self, message: str, affected_agents: List[str] = None) -> str:
        """Erstellt eine Notfall-Benachrichtigung"""
        notification_id = f"emergency_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        notification = {
            'notification_id': notification_id,
            'timestamp': datetime.now().isoformat(),
            'type': 'emergency',
            'priority': 'critical',
            'file_changed': 'manual',
            'summary': message,
            'affected_sections': ['all'],
            'impact_level': 'critical',
            'action_required': True,
            'status': 'active',
            'acknowledged_by': [],
            'target_agents': affected_agents or ['all']
        }
        
        # Benachrichtigung speichern
        notification_file = os.path.join(self.notifications_dir, f'{notification_id}.json')
        with open(notification_file, 'w', encoding='utf-8') as f:
            json.dump(notification, f, indent=2, ensure_ascii=False)
        
        return notification_id

if __name__ == '__main__':
    # Test des Notification Systems
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    notification_system = NotificationSystem(project_root)
    
    print("=== Notification System Test ===")
    
    # Prüfe auf Änderungen
    changes = notification_system.check_for_changes()
    print(f"Erkannte Änderungen: {len(changes)}")
    
    # Hole aktive Benachrichtigungen
    notifications = notification_system.get_active_notifications()
    print(f"Aktive Benachrichtigungen: {len(notifications)}")
    
    # Generiere Zusammenfassung
    summary = notification_system.generate_notification_summary('test_agent')
    print(f"Zusammenfassung generiert: {len(summary)} Zeichen")

