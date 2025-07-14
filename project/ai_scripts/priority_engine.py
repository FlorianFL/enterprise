import json
import os
from datetime import datetime, timedelta
from typing import List, Dict, Any
import re

class PriorityEngine:
    """
    Erweiterte Priorisierungs-Engine für automatisierte Aufgabenverteilung
    """
    
    def __init__(self, project_root: str):
        self.project_root = project_root
        self.manifest_path = os.path.join(project_root, 'project_manifest.json')
        self.tasks_dir = os.path.join(project_root, 'tasks')
        self.history_dir = os.path.join(project_root, 'history')
        self.knowledge_base_dir = os.path.join(project_root, 'knowledge_base')
        
        # Priorisierungs-Gewichtungen
        self.weights = {
            'urgency': 0.3,
            'complexity': 0.2,
            'dependencies': 0.25,
            'resource_availability': 0.15,
            'strategic_importance': 0.1
        }
    
    def load_manifest(self) -> Dict[str, Any]:
        """Lädt das project_manifest.json"""
        with open(self.manifest_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def save_manifest(self, manifest: Dict[str, Any]) -> None:
        """Speichert das project_manifest.json"""
        with open(self.manifest_path, 'w', encoding='utf-8') as f:
            json.dump(manifest, f, indent=2, ensure_ascii=False)
    
    def analyze_task_complexity(self, task: Dict[str, Any]) -> float:
        """
        Analysiert die Komplexität einer Aufgabe basierend auf:
        - Anzahl der Subtasks
        - Beschreibungslänge
        - Verwendete Keywords (technisch, komplex, etc.)
        """
        complexity_score = 0.0
        
        # Subtasks-Analyse
        subtasks = task.get('subtasks', [])
        complexity_score += len(subtasks) * 0.1
        
        # Beschreibungsanalyse
        description = task.get('description', '')
        complexity_keywords = ['komplex', 'schwierig', 'herausfordernd', 'umfangreich', 
                              'integration', 'algorithmus', 'optimierung', 'machine learning']
        
        for keyword in complexity_keywords:
            if keyword.lower() in description.lower():
                complexity_score += 0.2
        
        # Normalisierung auf 0-1 Skala
        return min(complexity_score, 1.0)
    
    def analyze_dependencies(self, task: Dict[str, Any], all_tasks: List[Dict[str, Any]]) -> float:
        """
        Analysiert Abhängigkeiten einer Aufgabe
        """
        dependencies = task.get('dependencies', [])
        dependency_score = 0.0
        
        # Direkte Abhängigkeiten
        for dep_id in dependencies:
            for other_task in all_tasks:
                if other_task.get('task_id') == dep_id:
                    if other_task.get('status') != 'completed':
                        dependency_score += 0.3
        
        # Implizite Abhängigkeiten durch Team-Zuweisungen
        assigned_team = task.get('assigned_team', '')
        for other_task in all_tasks:
            if (other_task.get('assigned_team') == assigned_team and 
                other_task.get('status') == 'in_progress'):
                dependency_score += 0.1
        
        return min(dependency_score, 1.0)
    
    def analyze_resource_availability(self, task: Dict[str, Any], manifest: Dict[str, Any]) -> float:
        """
        Analysiert die Verfügbarkeit von Ressourcen für eine Aufgabe
        """
        teams = manifest.get('teams', [])
        assigned_team = task.get('assigned_team', '')
        assigned_leader = task.get('assigned_to_leader', '')
        
        availability_score = 1.0  # Start mit hoher Verfügbarkeit
        
        # Team-Verfügbarkeit prüfen
        for team in teams:
            if team.get('name') == assigned_team:
                members = team.get('members', [])
                if len(members) == 0:
                    availability_score -= 0.5  # Kein Team verfügbar
                elif len(members) < 2:
                    availability_score -= 0.2  # Kleines Team
        
        # Budget-Verfügbarkeit prüfen
        ceo_directives = manifest.get('ceo_directives', {})
        budget_allocation = ceo_directives.get('budget_allocation', {})
        
        if assigned_team in budget_allocation:
            budget_info = budget_allocation[assigned_team]
            if isinstance(budget_info, dict):
                total = budget_info.get('total', 0)
                spent = budget_info.get('spent', 0)
                if total > 0 and (spent / total) > 0.8:
                    availability_score -= 0.3  # Budget fast aufgebraucht
        
        return max(availability_score, 0.0)
    
    def analyze_strategic_importance(self, task: Dict[str, Any], manifest: Dict[str, Any]) -> float:
        """
        Analysiert die strategische Wichtigkeit einer Aufgabe
        """
        ceo_directives = manifest.get('ceo_directives', {})
        priority_focus = ceo_directives.get('priority_focus', '').lower()
        
        strategic_score = 0.5  # Basis-Score
        
        # CEO-Prioritätsfokus
        task_title = task.get('title', '').lower()
        task_description = task.get('description', '').lower()
        
        if priority_focus and (priority_focus in task_title or priority_focus in task_description):
            strategic_score += 0.4
        
        # Projekt-Ziel Alignment
        project_goal = manifest.get('goal', '').lower()
        goal_keywords = project_goal.split()[:5]  # Erste 5 Wörter des Ziels
        
        for keyword in goal_keywords:
            if len(keyword) > 3 and keyword in task_description:
                strategic_score += 0.1
        
        return min(strategic_score, 1.0)
    
    def calculate_priority_score(self, task: Dict[str, Any], all_tasks: List[Dict[str, Any]], 
                                manifest: Dict[str, Any]) -> float:
        """
        Berechnet den Gesamtprioritätsscore einer Aufgabe
        """
        # Urgency (aus Task-Metadaten oder Default)
        urgency_map = {'high': 1.0, 'medium': 0.6, 'low': 0.3}
        urgency = urgency_map.get(task.get('urgency', 'medium'), 0.6)
        
        # Komplexität (invertiert - weniger komplex = höhere Priorität für schnelle Wins)
        complexity = 1.0 - self.analyze_task_complexity(task)
        
        # Abhängigkeiten (invertiert - weniger Abhängigkeiten = höhere Priorität)
        dependencies = 1.0 - self.analyze_dependencies(task, all_tasks)
        
        # Ressourcenverfügbarkeit
        resource_availability = self.analyze_resource_availability(task, manifest)
        
        # Strategische Wichtigkeit
        strategic_importance = self.analyze_strategic_importance(task, manifest)
        
        # Gewichtete Gesamtbewertung
        total_score = (
            urgency * self.weights['urgency'] +
            complexity * self.weights['complexity'] +
            dependencies * self.weights['dependencies'] +
            resource_availability * self.weights['resource_availability'] +
            strategic_importance * self.weights['strategic_importance']
        )
        
        return total_score
    
    def prioritize_tasks(self) -> List[Dict[str, Any]]:
        """
        Priorisiert alle offenen Aufgaben und gibt sie sortiert zurück
        """
        manifest = self.load_manifest()
        all_tasks = manifest.get('tasks', [])
        
        # Nur offene Aufgaben berücksichtigen
        open_tasks = [task for task in all_tasks if task.get('status') == 'open']
        
        # Prioritätsscore für jede Aufgabe berechnen
        for task in open_tasks:
            priority_score = self.calculate_priority_score(task, all_tasks, manifest)
            task['priority_score'] = priority_score
        
        # Nach Prioritätsscore sortieren (höchster zuerst)
        prioritized_tasks = sorted(open_tasks, key=lambda x: x.get('priority_score', 0), reverse=True)
        
        return prioritized_tasks
    
    def find_suitable_agent(self, task: Dict[str, Any], manifest: Dict[str, Any]) -> str:
        """
        Findet den am besten geeigneten KI-Agenten für eine Aufgabe
        """
        teams = manifest.get('teams', [])
        assigned_team = task.get('assigned_team', '')
        assigned_leader = task.get('assigned_to_leader', '')
        required_role = task.get('required_role', '')
        
        # Wenn ein Teamleiter zugewiesen ist, diesen zurückgeben
        if assigned_leader:
            return assigned_leader
        
        # Wenn ein Team zugewiesen ist, verfügbares Mitglied finden
        if assigned_team:
            for team in teams:
                if team.get('name') == assigned_team:
                    members = team.get('members', [])
                    roles = team.get('roles', [])
                    
                    # Wenn eine spezifische Rolle erforderlich ist
                    if required_role and required_role in roles:
                        # Hier könnte eine komplexere Logik implementiert werden
                        # um den besten Agenten basierend auf Verfügbarkeit zu finden
                        if members:
                            return members[0]  # Vereinfacht: ersten verfügbaren nehmen
                    
                    # Andernfalls ersten verfügbaren Agenten des Teams
                    if members:
                        return members[0]
        
        return None
    
    def auto_assign_tasks(self, max_assignments: int = 5) -> List[Dict[str, Any]]:
        """
        Weist automatisch Aufgaben an geeignete KI-Agenten zu
        """
        prioritized_tasks = self.prioritize_tasks()
        manifest = self.load_manifest()
        assignments = []
        
        for i, task in enumerate(prioritized_tasks[:max_assignments]):
            suitable_agent = self.find_suitable_agent(task, manifest)
            
            if suitable_agent:
                # Aufgabe zuweisen
                task_id = task.get('task_id')
                
                # Manifest aktualisieren
                for manifest_task in manifest.get('tasks', []):
                    if manifest_task.get('task_id') == task_id:
                        manifest_task['assigned_ai'] = suitable_agent
                        manifest_task['status'] = 'assigned'
                        manifest_task['assigned_date'] = datetime.now().isoformat()
                        break
                
                assignments.append({
                    'task_id': task_id,
                    'task_title': task.get('title'),
                    'assigned_to': suitable_agent,
                    'priority_score': task.get('priority_score'),
                    'assignment_reason': self._generate_assignment_reason(task, suitable_agent)
                })
        
        # Aktualisiertes Manifest speichern
        self.save_manifest(manifest)
        
        return assignments
    
    def _generate_assignment_reason(self, task: Dict[str, Any], agent: str) -> str:
        """
        Generiert eine Begründung für die Aufgabenzuweisung
        """
        reasons = []
        
        if task.get('assigned_team'):
            reasons.append(f"Team-Zugehörigkeit: {task.get('assigned_team')}")
        
        if task.get('required_role'):
            reasons.append(f"Erforderliche Rolle: {task.get('required_role')}")
        
        priority_score = task.get('priority_score', 0)
        if priority_score > 0.8:
            reasons.append("Hohe Priorität")
        elif priority_score > 0.6:
            reasons.append("Mittlere Priorität")
        else:
            reasons.append("Niedrige Priorität")
        
        return "; ".join(reasons)
    
    def generate_priority_report(self) -> str:
        """
        Generiert einen Bericht über die aktuelle Aufgabenpriorisierung
        """
        prioritized_tasks = self.prioritize_tasks()
        
        report = "# Aufgaben-Priorisierungsbericht\n\n"
        report += f"Generiert am: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        report += f"Anzahl offener Aufgaben: {len(prioritized_tasks)}\n\n"
        
        report += "## Priorisierte Aufgaben\n\n"
        
        for i, task in enumerate(prioritized_tasks, 1):
            priority_score = task.get('priority_score', 0)
            report += f"### {i}. {task.get('title', 'Unbenannte Aufgabe')}\n"
            report += f"- **Task ID:** {task.get('task_id')}\n"
            report += f"- **Prioritätsscore:** {priority_score:.3f}\n"
            report += f"- **Team:** {task.get('assigned_team', 'Nicht zugewiesen')}\n"
            report += f"- **Status:** {task.get('status', 'Unbekannt')}\n"
            
            if task.get('urgency'):
                report += f"- **Dringlichkeit:** {task.get('urgency')}\n"
            
            if task.get('description'):
                description = task.get('description')[:100]
                if len(task.get('description', '')) > 100:
                    description += "..."
                report += f"- **Beschreibung:** {description}\n"
            
            report += "\n"
        
        return report

if __name__ == '__main__':
    # Test der Priorisierungs-Engine
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    engine = PriorityEngine(project_root)
    
    print("=== Aufgaben-Priorisierung ===")
    prioritized = engine.prioritize_tasks()
    for task in prioritized:
        print(f"{task.get('title')}: Score {task.get('priority_score', 0):.3f}")
    
    print("\n=== Automatische Zuweisung ===")
    assignments = engine.auto_assign_tasks(max_assignments=3)
    for assignment in assignments:
        print(f"{assignment['task_title']} -> {assignment['assigned_to']} (Score: {assignment['priority_score']:.3f})")

