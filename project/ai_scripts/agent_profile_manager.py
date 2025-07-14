import json
import os
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Set
import uuid
from collections import defaultdict

class AgentProfileManager:
    """
    KI-Agenten-Profile und Spezialisierungs-Management
    Verwaltet Profile, Fähigkeiten, Erfahrungswerte und Performance-Metriken
    """
    
    def __init__(self, project_root: str):
        self.project_root = project_root
        self.profiles_dir = os.path.join(project_root, 'agent_profiles')
        self.manifest_path = os.path.join(project_root, 'project_manifest.json')
        self.history_dir = os.path.join(project_root, 'history')
        
        # Fähigkeits-Kategorien
        self.capability_categories = {
            'data_processing': {
                'name': 'Datenverarbeitung',
                'skills': ['data_collection', 'data_cleaning', 'data_transformation', 'data_analysis']
            },
            'machine_learning': {
                'name': 'Machine Learning',
                'skills': ['model_training', 'model_evaluation', 'feature_engineering', 'hyperparameter_tuning']
            },
            'software_development': {
                'name': 'Softwareentwicklung',
                'skills': ['coding', 'debugging', 'testing', 'code_review', 'architecture_design']
            },
            'project_management': {
                'name': 'Projektmanagement',
                'skills': ['task_planning', 'resource_allocation', 'team_coordination', 'progress_tracking']
            },
            'communication': {
                'name': 'Kommunikation',
                'skills': ['documentation', 'reporting', 'presentation', 'collaboration']
            },
            'quality_assurance': {
                'name': 'Qualitätssicherung',
                'skills': ['testing', 'validation', 'error_detection', 'process_improvement']
            },
            'research': {
                'name': 'Forschung',
                'skills': ['literature_review', 'experimentation', 'analysis', 'innovation']
            }
        }
        
        # Performance-Metriken
        self.performance_metrics = {
            'task_completion_rate': 'Aufgaben-Abschlussrate',
            'average_task_duration': 'Durchschnittliche Aufgabendauer',
            'error_rate': 'Fehlerrate',
            'quality_score': 'Qualitätsbewertung',
            'collaboration_score': 'Kollaborationsbewertung',
            'learning_rate': 'Lernfortschritt',
            'innovation_score': 'Innovationsbewertung'
        }
        
        # Spezialisierungs-Level
        self.specialization_levels = {
            1: 'Anfänger',
            2: 'Fortgeschritten',
            3: 'Kompetent',
            4: 'Experte',
            5: 'Meister'
        }
        
        # Stelle sicher, dass Profile-Verzeichnis existiert
        os.makedirs(self.profiles_dir, exist_ok=True)
    
    def create_agent_profile(self, agent_id: str, agent_config: Dict[str, Any]) -> str:
        """Erstellt ein neues Agenten-Profil"""
        profile_id = f"profile_{agent_id}_{datetime.now().strftime('%Y%m%d')}"
        
        profile = {
            'profile_id': profile_id,
            'agent_id': agent_id,
            'created_date': datetime.now().isoformat(),
            'last_updated': datetime.now().isoformat(),
            'basic_info': {
                'name': agent_config.get('name', agent_id),
                'description': agent_config.get('description', ''),
                'version': agent_config.get('version', '1.0'),
                'type': agent_config.get('type', 'general'),
                'status': 'active'
            },
            'capabilities': self._initialize_capabilities(agent_config),
            'specializations': self._determine_specializations(agent_config),
            'performance_history': {
                'tasks_completed': 0,
                'tasks_failed': 0,
                'total_runtime_hours': 0.0,
                'last_activity': None,
                'metrics': {metric: 0.0 for metric in self.performance_metrics.keys()}
            },
            'experience_points': {
                category: 0 for category in self.capability_categories.keys()
            },
            'strengths': [],
            'weaknesses': [],
            'learning_goals': [],
            'collaboration_history': {
                'worked_with': [],
                'team_assignments': [],
                'feedback_received': []
            },
            'certifications': [],
            'achievements': []
        }
        
        # Profil speichern
        profile_file = os.path.join(self.profiles_dir, f'{profile_id}.json')
        with open(profile_file, 'w', encoding='utf-8') as f:
            json.dump(profile, f, indent=2, ensure_ascii=False)
        
        return profile_id
    
    def _initialize_capabilities(self, agent_config: Dict[str, Any]) -> Dict[str, Any]:
        """Initialisiert die Fähigkeiten eines Agenten"""
        capabilities = {}
        
        # Basis-Fähigkeiten aus Konfiguration
        config_capabilities = agent_config.get('capabilities', [])
        
        for category, category_info in self.capability_categories.items():
            capabilities[category] = {
                'level': 1,  # Startet bei Level 1
                'skills': {},
                'experience_points': 0,
                'last_used': None
            }
            
            # Skills initialisieren
            for skill in category_info['skills']:
                # Prüfe ob Skill in Konfiguration erwähnt wird
                initial_level = 1
                if skill in config_capabilities or any(skill in cap for cap in config_capabilities):
                    initial_level = 2  # Höheres Startlevel wenn explizit erwähnt
                
                capabilities[category]['skills'][skill] = {
                    'level': initial_level,
                    'experience': 0,
                    'last_used': None,
                    'success_rate': 0.0
                }
        
        return capabilities
    
    def _determine_specializations(self, agent_config: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Bestimmt die Spezialisierungen eines Agenten"""
        specializations = []
        
        # Aus Rollen-Zuweisungen
        role = agent_config.get('role', '')
        team = agent_config.get('assigned_team', '')
        
        role_specializations = {
            'data_collector': 'data_processing',
            'data_cleaner': 'data_processing',
            'model_trainer': 'machine_learning',
            'model_evaluator': 'machine_learning',
            'developer': 'software_development',
            'tester': 'quality_assurance',
            'researcher': 'research',
            'manager': 'project_management'
        }
        
        for role_key, category in role_specializations.items():
            if role_key.lower() in role.lower():
                specializations.append({
                    'category': category,
                    'level': 2,
                    'acquired_date': datetime.now().isoformat(),
                    'source': 'role_assignment'
                })
        
        # Aus Team-Zuweisungen
        team_specializations = {
            'data_engineering': 'data_processing',
            'ml_modeling': 'machine_learning',
            'development': 'software_development',
            'qa': 'quality_assurance',
            'research': 'research'
        }
        
        for team_key, category in team_specializations.items():
            if team_key.lower() in team.lower():
                if not any(spec['category'] == category for spec in specializations):
                    specializations.append({
                        'category': category,
                        'level': 1,
                        'acquired_date': datetime.now().isoformat(),
                        'source': 'team_assignment'
                    })
        
        return specializations
    
    def load_agent_profile(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Lädt das Profil eines Agenten"""
        # Suche nach dem neuesten Profil für den Agenten
        profile_files = []
        
        for filename in os.listdir(self.profiles_dir):
            if filename.startswith(f'profile_{agent_id}_') and filename.endswith('.json'):
                profile_files.append(filename)
        
        if not profile_files:
            return None
        
        # Neueste Datei nehmen
        latest_file = sorted(profile_files)[-1]
        profile_path = os.path.join(self.profiles_dir, latest_file)
        
        with open(profile_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def update_agent_profile(self, agent_id: str, updates: Dict[str, Any]) -> bool:
        """Aktualisiert das Profil eines Agenten"""
        profile = self.load_agent_profile(agent_id)
        if not profile:
            return False
        
        # Updates anwenden
        for key, value in updates.items():
            if key in profile:
                if isinstance(profile[key], dict) and isinstance(value, dict):
                    profile[key].update(value)
                else:
                    profile[key] = value
        
        profile['last_updated'] = datetime.now().isoformat()
        
        # Profil speichern
        profile_file = os.path.join(self.profiles_dir, f"{profile['profile_id']}.json")
        with open(profile_file, 'w', encoding='utf-8') as f:
            json.dump(profile, f, indent=2, ensure_ascii=False)
        
        return True
    
    def record_task_completion(self, agent_id: str, task_info: Dict[str, Any]) -> None:
        """Zeichnet eine Aufgaben-Completion auf und aktualisiert das Profil"""
        profile = self.load_agent_profile(agent_id)
        if not profile:
            return
        
        # Performance-History aktualisieren
        performance = profile['performance_history']
        
        if task_info.get('status') == 'completed':
            performance['tasks_completed'] += 1
        else:
            performance['tasks_failed'] += 1
        
        # Laufzeit hinzufügen
        if task_info.get('duration_hours'):
            performance['total_runtime_hours'] += task_info['duration_hours']
        
        performance['last_activity'] = datetime.now().isoformat()
        
        # Fähigkeiten basierend auf Task-Typ aktualisieren
        task_type = task_info.get('type', 'general')
        required_skills = self._map_task_to_skills(task_type, task_info)
        
        for category, skills in required_skills.items():
            if category in profile['capabilities']:
                for skill in skills:
                    if skill in profile['capabilities'][category]['skills']:
                        # Erfahrung hinzufügen
                        skill_data = profile['capabilities'][category]['skills'][skill]
                        skill_data['experience'] += 1
                        skill_data['last_used'] = datetime.now().isoformat()
                        
                        # Success Rate aktualisieren
                        if task_info.get('status') == 'completed':
                            current_rate = skill_data['success_rate']
                            total_uses = skill_data['experience']
                            skill_data['success_rate'] = (current_rate * (total_uses - 1) + 1.0) / total_uses
                        
                        # Level-Up prüfen
                        if skill_data['experience'] >= skill_data['level'] * 5:
                            skill_data['level'] = min(5, skill_data['level'] + 1)
                
                # Kategorie-Erfahrung aktualisieren
                profile['experience_points'][category] += len(skills)
                
                # Kategorie-Level aktualisieren
                total_exp = profile['experience_points'][category]
                new_level = min(5, 1 + total_exp // 10)
                profile['capabilities'][category]['level'] = new_level
        
        # Metriken aktualisieren
        self._update_performance_metrics(profile, task_info)
        
        # Profil speichern
        self.update_agent_profile(agent_id, profile)
    
    def _map_task_to_skills(self, task_type: str, task_info: Dict[str, Any]) -> Dict[str, List[str]]:
        """Mappt einen Task-Typ zu relevanten Skills"""
        task_skill_mapping = {
            'data_collection': {
                'data_processing': ['data_collection'],
                'communication': ['documentation']
            },
            'data_cleaning': {
                'data_processing': ['data_cleaning', 'data_transformation'],
                'quality_assurance': ['validation']
            },
            'model_training': {
                'machine_learning': ['model_training', 'feature_engineering'],
                'data_processing': ['data_analysis']
            },
            'model_evaluation': {
                'machine_learning': ['model_evaluation'],
                'quality_assurance': ['testing', 'validation']
            },
            'development': {
                'software_development': ['coding', 'debugging'],
                'quality_assurance': ['testing']
            },
            'testing': {
                'quality_assurance': ['testing', 'error_detection'],
                'software_development': ['debugging']
            },
            'research': {
                'research': ['literature_review', 'analysis'],
                'communication': ['documentation']
            },
            'management': {
                'project_management': ['task_planning', 'progress_tracking'],
                'communication': ['reporting']
            }
        }
        
        # Versuche Task-Typ zu matchen
        for pattern, skills in task_skill_mapping.items():
            if pattern.lower() in task_type.lower():
                return skills
        
        # Default: allgemeine Skills
        return {
            'communication': ['documentation'],
            'project_management': ['task_planning']
        }
    
    def _update_performance_metrics(self, profile: Dict[str, Any], task_info: Dict[str, Any]) -> None:
        """Aktualisiert Performance-Metriken"""
        metrics = profile['performance_history']['metrics']
        performance = profile['performance_history']
        
        # Task Completion Rate
        total_tasks = performance['tasks_completed'] + performance['tasks_failed']
        if total_tasks > 0:
            metrics['task_completion_rate'] = performance['tasks_completed'] / total_tasks
        
        # Average Task Duration
        if performance['tasks_completed'] > 0:
            metrics['average_task_duration'] = performance['total_runtime_hours'] / performance['tasks_completed']
        
        # Error Rate
        if total_tasks > 0:
            metrics['error_rate'] = performance['tasks_failed'] / total_tasks
        
        # Quality Score (basierend auf Task-Feedback)
        if task_info.get('quality_rating'):
            current_quality = metrics.get('quality_score', 0.0)
            new_rating = task_info['quality_rating']
            # Gewichteter Durchschnitt
            metrics['quality_score'] = (current_quality * 0.8) + (new_rating * 0.2)
        
        # Learning Rate (basierend auf Skill-Verbesserungen)
        total_skill_levels = sum(
            sum(skill['level'] for skill in category['skills'].values())
            for category in profile['capabilities'].values()
        )
        metrics['learning_rate'] = total_skill_levels / max(1, total_tasks)
    
    def find_best_agent_for_task(self, task_requirements: Dict[str, Any]) -> Optional[str]:
        """Findet den besten Agenten für eine Aufgabe"""
        required_skills = task_requirements.get('required_skills', [])
        required_category = task_requirements.get('category', '')
        min_level = task_requirements.get('min_level', 1)
        
        agent_scores = {}
        
        # Alle Profile durchgehen
        for filename in os.listdir(self.profiles_dir):
            if filename.startswith('profile_') and filename.endswith('.json'):
                profile_path = os.path.join(self.profiles_dir, filename)
                
                with open(profile_path, 'r', encoding='utf-8') as f:
                    profile = json.load(f)
                
                agent_id = profile['agent_id']
                
                # Prüfe ob Agent aktiv ist
                if profile['basic_info']['status'] != 'active':
                    continue
                
                score = self._calculate_agent_task_score(profile, task_requirements)
                agent_scores[agent_id] = score
        
        # Besten Agenten zurückgeben
        if agent_scores:
            best_agent = max(agent_scores.items(), key=lambda x: x[1])
            return best_agent[0] if best_agent[1] > 0 else None
        
        return None
    
    def _calculate_agent_task_score(self, profile: Dict[str, Any], requirements: Dict[str, Any]) -> float:
        """Berechnet einen Score für die Eignung eines Agenten für eine Aufgabe"""
        score = 0.0
        
        required_skills = requirements.get('required_skills', [])
        required_category = requirements.get('category', '')
        min_level = requirements.get('min_level', 1)
        
        capabilities = profile['capabilities']
        performance = profile['performance_history']['metrics']
        
        # Skill-Match Score
        skill_score = 0.0
        skill_count = 0
        
        for category, category_data in capabilities.items():
            if required_category and category != required_category:
                continue
            
            for skill, skill_data in category_data['skills'].items():
                if skill in required_skills or not required_skills:
                    skill_level = skill_data['level']
                    success_rate = skill_data['success_rate']
                    
                    if skill_level >= min_level:
                        skill_score += skill_level * (1 + success_rate)
                        skill_count += 1
        
        if skill_count > 0:
            score += skill_score / skill_count * 0.4
        
        # Performance Score
        completion_rate = performance.get('task_completion_rate', 0.0)
        quality_score = performance.get('quality_score', 0.0)
        error_rate = performance.get('error_rate', 1.0)
        
        performance_score = (completion_rate + quality_score + (1 - error_rate)) / 3
        score += performance_score * 0.3
        
        # Spezialisierungs-Score
        specializations = profile.get('specializations', [])
        specialization_score = 0.0
        
        for spec in specializations:
            if spec['category'] == required_category:
                specialization_score += spec['level'] * 0.2
        
        score += min(1.0, specialization_score) * 0.2
        
        # Verfügbarkeits-Score (basierend auf letzter Aktivität)
        last_activity = profile['performance_history'].get('last_activity')
        availability_score = 1.0
        
        if last_activity:
            try:
                last_time = datetime.fromisoformat(last_activity)
                hours_since = (datetime.now() - last_time).total_seconds() / 3600
                
                if hours_since < 1:
                    availability_score = 0.5  # Möglicherweise noch beschäftigt
                elif hours_since > 24:
                    availability_score = 1.0  # Definitiv verfügbar
                else:
                    availability_score = 0.7 + (hours_since / 24) * 0.3
            except:
                pass
        
        score += availability_score * 0.1
        
        return score
    
    def generate_agent_report(self, agent_id: str) -> str:
        """Generiert einen umfassenden Agenten-Bericht"""
        profile = self.load_agent_profile(agent_id)
        if not profile:
            return f"Profil für Agent {agent_id} nicht gefunden."
        
        report = f"# Agent Profile Report: {agent_id}\n\n"
        report += f"Generiert am: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        # Basis-Informationen
        basic_info = profile['basic_info']
        report += "## Basis-Informationen\n\n"
        report += f"- **Name:** {basic_info['name']}\n"
        report += f"- **Typ:** {basic_info['type']}\n"
        report += f"- **Status:** {basic_info['status']}\n"
        report += f"- **Version:** {basic_info['version']}\n"
        report += f"- **Erstellt:** {profile['created_date'][:10]}\n"
        report += f"- **Letzte Aktualisierung:** {profile['last_updated'][:10]}\n\n"
        
        if basic_info['description']:
            report += f"**Beschreibung:** {basic_info['description']}\n\n"
        
        # Performance-Übersicht
        performance = profile['performance_history']
        metrics = performance['metrics']
        
        report += "## Performance-Übersicht\n\n"
        report += f"- **Abgeschlossene Aufgaben:** {performance['tasks_completed']}\n"
        report += f"- **Fehlgeschlagene Aufgaben:** {performance['tasks_failed']}\n"
        report += f"- **Gesamte Laufzeit:** {performance['total_runtime_hours']:.1f} Stunden\n"
        report += f"- **Abschlussrate:** {metrics.get('task_completion_rate', 0):.1%}\n"
        report += f"- **Durchschnittliche Aufgabendauer:** {metrics.get('average_task_duration', 0):.1f} Stunden\n"
        report += f"- **Fehlerrate:** {metrics.get('error_rate', 0):.1%}\n"
        report += f"- **Qualitätsbewertung:** {metrics.get('quality_score', 0):.1f}/5\n\n"
        
        # Spezialisierungen
        specializations = profile.get('specializations', [])
        if specializations:
            report += "## Spezialisierungen\n\n"
            for spec in specializations:
                category_name = self.capability_categories.get(spec['category'], {}).get('name', spec['category'])
                level_name = self.specialization_levels.get(spec['level'], f"Level {spec['level']}")
                report += f"- **{category_name}:** {level_name}\n"
            report += "\n"
        
        # Top Fähigkeiten
        report += "## Top Fähigkeiten\n\n"
        all_skills = []
        
        for category, category_data in profile['capabilities'].items():
            category_name = self.capability_categories.get(category, {}).get('name', category)
            
            for skill, skill_data in category_data['skills'].items():
                all_skills.append({
                    'skill': skill.replace('_', ' ').title(),
                    'category': category_name,
                    'level': skill_data['level'],
                    'experience': skill_data['experience'],
                    'success_rate': skill_data['success_rate']
                })
        
        # Nach Level und Erfahrung sortieren
        top_skills = sorted(all_skills, key=lambda x: (x['level'], x['experience']), reverse=True)[:10]
        
        for skill in top_skills:
            level_name = self.specialization_levels.get(skill['level'], f"Level {skill['level']}")
            report += f"- **{skill['skill']}** ({skill['category']}): {level_name} "
            report += f"(Erfahrung: {skill['experience']}, Erfolgsrate: {skill['success_rate']:.1%})\n"
        
        report += "\n"
        
        # Stärken und Schwächen
        strengths = profile.get('strengths', [])
        weaknesses = profile.get('weaknesses', [])
        
        if strengths:
            report += "## Stärken\n\n"
            for strength in strengths:
                report += f"- {strength}\n"
            report += "\n"
        
        if weaknesses:
            report += "## Verbesserungsbereiche\n\n"
            for weakness in weaknesses:
                report += f"- {weakness}\n"
            report += "\n"
        
        # Lernziele
        learning_goals = profile.get('learning_goals', [])
        if learning_goals:
            report += "## Lernziele\n\n"
            for goal in learning_goals:
                report += f"- {goal}\n"
            report += "\n"
        
        # Kollaborations-History
        collaboration = profile.get('collaboration_history', {})
        worked_with = collaboration.get('worked_with', [])
        
        if worked_with:
            report += "## Kollaborations-Partner\n\n"
            partner_counts = {}
            for partner in worked_with:
                partner_counts[partner] = partner_counts.get(partner, 0) + 1
            
            for partner, count in sorted(partner_counts.items(), key=lambda x: x[1], reverse=True)[:5]:
                report += f"- **{partner}:** {count} gemeinsame Projekte\n"
            report += "\n"
        
        # Empfehlungen
        report += "## Empfehlungen\n\n"
        
        # Basierend auf Performance
        if metrics.get('task_completion_rate', 0) < 0.8:
            report += "- Fokus auf Verbesserung der Aufgaben-Abschlussrate\n"
        
        if metrics.get('error_rate', 0) > 0.2:
            report += "- Zusätzliches Training zur Fehlerreduzierung empfohlen\n"
        
        # Basierend auf Fähigkeiten
        low_level_categories = [
            cat for cat, data in profile['capabilities'].items()
            if data['level'] < 3
        ]
        
        if low_level_categories:
            category_names = [
                self.capability_categories.get(cat, {}).get('name', cat)
                for cat in low_level_categories[:3]
            ]
            report += f"- Weiterbildung in folgenden Bereichen: {', '.join(category_names)}\n"
        
        return report
    
    def get_team_composition_recommendations(self, task_requirements: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Empfiehlt Team-Zusammensetzung für komplexe Projekte"""
        recommendations = {
            'recommended_team': [],
            'coverage_analysis': {},
            'potential_gaps': [],
            'alternative_options': []
        }
        
        # Sammle alle erforderlichen Skills
        all_required_skills = set()
        required_categories = set()
        
        for req in task_requirements:
            all_required_skills.update(req.get('required_skills', []))
            if req.get('category'):
                required_categories.add(req['category'])
        
        # Finde beste Agenten für jede Kategorie
        category_agents = {}
        
        for category in required_categories:
            best_agent = self.find_best_agent_for_task({
                'category': category,
                'required_skills': list(all_required_skills),
                'min_level': 2
            })
            
            if best_agent:
                category_agents[category] = best_agent
                recommendations['recommended_team'].append({
                    'agent_id': best_agent,
                    'primary_role': category,
                    'confidence': 0.8  # Placeholder
                })
        
        # Analyse der Abdeckung
        covered_skills = set()
        for agent_id in category_agents.values():
            profile = self.load_agent_profile(agent_id)
            if profile:
                for category_data in profile['capabilities'].values():
                    for skill, skill_data in category_data['skills'].items():
                        if skill_data['level'] >= 2:
                            covered_skills.add(skill)
        
        recommendations['coverage_analysis'] = {
            'required_skills': list(all_required_skills),
            'covered_skills': list(covered_skills),
            'coverage_percentage': len(covered_skills & all_required_skills) / max(1, len(all_required_skills))
        }
        
        # Identifiziere Lücken
        missing_skills = all_required_skills - covered_skills
        recommendations['potential_gaps'] = list(missing_skills)
        
        return recommendations

if __name__ == '__main__':
    # Test des Agent Profile Managers
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    profile_manager = AgentProfileManager(project_root)
    
    print("=== Agent Profile Manager Test ===")
    
    # Erstelle Test-Profil
    test_config = {
        'name': 'Test Agent',
        'description': 'Ein Test-Agent für Demonstrationszwecke',
        'type': 'data_processor',
        'role': 'data_collector',
        'assigned_team': 'data_engineering',
        'capabilities': ['data_collection', 'data_cleaning']
    }
    
    profile_id = profile_manager.create_agent_profile('test_agent_001', test_config)
    print(f"Profil erstellt: {profile_id}")
    
    # Lade Profil
    profile = profile_manager.load_agent_profile('test_agent_001')
    print(f"Profil geladen: {profile['basic_info']['name'] if profile else 'Nicht gefunden'}")
    
    # Simuliere Task-Completion
    task_info = {
        'status': 'completed',
        'type': 'data_collection',
        'duration_hours': 2.5,
        'quality_rating': 4.2
    }
    
    profile_manager.record_task_completion('test_agent_001', task_info)
    print("Task-Completion aufgezeichnet")
    
    # Generiere Bericht
    report = profile_manager.generate_agent_report('test_agent_001')
    print(f"Bericht generiert: {len(report)} Zeichen")

