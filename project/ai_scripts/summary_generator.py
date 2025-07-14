import json
import os
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import re
from collections import defaultdict, Counter

class SummaryGenerator:
    """
    Automatisierte Zusammenfassungen für Projektfortschritt, Probleme und Verbesserungsvorschläge
    Generiert regelmäßige Reports für das Management
    """
    
    def __init__(self, project_root: str):
        self.project_root = project_root
        self.manifest_path = os.path.join(project_root, 'project_manifest.json')
        self.history_dir = os.path.join(project_root, 'history')
        self.knowledge_base_dir = os.path.join(project_root, 'knowledge_base')
        self.summaries_dir = os.path.join(project_root, 'summaries')
        self.agent_profiles_dir = os.path.join(project_root, 'agent_profiles')
        self.feedback_dir = os.path.join(project_root, 'feedback')
        
        # Summary-Typen
        self.summary_types = {
            'daily': 'Tägliche Zusammenfassung',
            'weekly': 'Wöchentliche Zusammenfassung',
            'monthly': 'Monatliche Zusammenfassung',
            'project_status': 'Projekt-Status-Report',
            'performance': 'Performance-Analyse',
            'issues': 'Problem-Report',
            'improvements': 'Verbesserungs-Report'
        }
        
        # Report-Templates
        self.report_templates = {
            'executive': 'Führungskräfte-Summary',
            'technical': 'Technischer Report',
            'operational': 'Operativer Report',
            'strategic': 'Strategischer Report'
        }
        
        # Stelle sicher, dass Summaries-Verzeichnis existiert
        os.makedirs(self.summaries_dir, exist_ok=True)
    
    def load_manifest(self) -> Dict[str, Any]:
        """Lädt das project_manifest.json"""
        with open(self.manifest_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def collect_project_data(self, days: int = 7) -> Dict[str, Any]:
        """Sammelt alle relevanten Projektdaten für die Zusammenfassung"""
        cutoff_date = datetime.now() - timedelta(days=days)
        
        data = {
            'period': {
                'start_date': cutoff_date.isoformat(),
                'end_date': datetime.now().isoformat(),
                'days': days
            },
            'tasks': {
                'total': 0,
                'completed': 0,
                'in_progress': 0,
                'open': 0,
                'failed': 0,
                'recent_completions': []
            },
            'agents': {
                'active_count': 0,
                'performance_summary': {},
                'top_performers': [],
                'underperformers': []
            },
            'issues': {
                'total_reported': 0,
                'resolved': 0,
                'open': 0,
                'critical': 0,
                'recent_issues': []
            },
            'improvements': {
                'suggestions_count': 0,
                'implemented': 0,
                'pending': 0,
                'recent_suggestions': []
            },
            'metrics': {
                'productivity': 0.0,
                'quality': 0.0,
                'efficiency': 0.0,
                'collaboration': 0.0
            }
        }
        
        # Manifest-Daten sammeln
        manifest = self.load_manifest()
        
        # Task-Statistiken
        tasks = manifest.get('tasks', [])
        data['tasks']['total'] = len(tasks)
        
        for task in tasks:
            status = task.get('status', 'unknown')
            if status == 'completed':
                data['tasks']['completed'] += 1
                
                # Prüfe ob kürzlich abgeschlossen
                completed_date = task.get('completed_date')
                if completed_date:
                    try:
                        comp_date = datetime.fromisoformat(completed_date)
                        if comp_date >= cutoff_date:
                            data['tasks']['recent_completions'].append(task)
                    except:
                        pass
            
            elif status == 'in_progress':
                data['tasks']['in_progress'] += 1
            elif status == 'open':
                data['tasks']['open'] += 1
            elif status == 'failed':
                data['tasks']['failed'] += 1
        
        # Agent-Performance sammeln
        if os.path.exists(self.agent_profiles_dir):
            agent_files = [f for f in os.listdir(self.agent_profiles_dir) if f.endswith('.json')]
            data['agents']['active_count'] = len(agent_files)
            
            agent_performances = []
            
            for agent_file in agent_files:
                try:
                    with open(os.path.join(self.agent_profiles_dir, agent_file), 'r', encoding='utf-8') as f:
                        profile = json.load(f)
                    
                    agent_id = profile.get('agent_id')
                    performance = profile.get('performance_history', {})
                    metrics = performance.get('metrics', {})
                    
                    completion_rate = metrics.get('task_completion_rate', 0.0)
                    quality_score = metrics.get('quality_score', 0.0)
                    
                    agent_performances.append({
                        'agent_id': agent_id,
                        'completion_rate': completion_rate,
                        'quality_score': quality_score,
                        'total_tasks': performance.get('tasks_completed', 0) + performance.get('tasks_failed', 0)
                    })
                    
                except:
                    continue
            
            # Top und Underperformer identifizieren
            if agent_performances:
                sorted_by_completion = sorted(agent_performances, key=lambda x: x['completion_rate'], reverse=True)
                data['agents']['top_performers'] = sorted_by_completion[:3]
                data['agents']['underperformers'] = [a for a in sorted_by_completion if a['completion_rate'] < 0.7]
        
        # History-Daten für Issues sammeln
        if os.path.exists(self.history_dir):
            for log_file in os.listdir(self.history_dir):
                if log_file.endswith('.log'):
                    log_path = os.path.join(self.history_dir, log_file)
                    
                    # Prüfe Datei-Datum
                    file_time = datetime.fromtimestamp(os.path.getmtime(log_path))
                    if file_time < cutoff_date:
                        continue
                    
                    try:
                        with open(log_path, 'r', encoding='utf-8') as f:
                            content = f.read().lower()
                        
                        # Suche nach Error-Pattern
                        error_patterns = ['error', 'fehler', 'failed', 'exception', 'critical']
                        for pattern in error_patterns:
                            if pattern in content:
                                data['issues']['total_reported'] += 1
                                
                                if 'critical' in content:
                                    data['issues']['critical'] += 1
                                
                                data['issues']['recent_issues'].append({
                                    'file': log_file,
                                    'date': file_time.isoformat(),
                                    'type': 'error_detected'
                                })
                                break
                    except:
                        continue
        
        # Knowledge Base für Verbesserungen sammeln
        ideas_path = os.path.join(self.knowledge_base_dir, 'ideas.md')
        if os.path.exists(ideas_path):
            with open(ideas_path, 'r', encoding='utf-8') as f:
                ideas_content = f.read()
            
            # Zähle Abschnitte als Verbesserungsvorschläge
            sections = re.findall(r'^#+\s+(.+)$', ideas_content, re.MULTILINE)
            data['improvements']['suggestions_count'] = len(sections)
            
            # Suche nach kürzlich hinzugefügten Ideen
            recent_pattern = datetime.now().strftime('%Y-%m-%d')
            if recent_pattern in ideas_content:
                data['improvements']['recent_suggestions'] = sections[-3:]  # Letzte 3
        
        # Berechne Metriken
        if data['tasks']['total'] > 0:
            data['metrics']['productivity'] = data['tasks']['completed'] / data['tasks']['total']
        
        if agent_performances:
            avg_quality = sum(a['quality_score'] for a in agent_performances) / len(agent_performances)
            data['metrics']['quality'] = avg_quality
            
            avg_completion = sum(a['completion_rate'] for a in agent_performances) / len(agent_performances)
            data['metrics']['efficiency'] = avg_completion
        
        # Kollaboration basierend auf Team-Aktivität
        teams = manifest.get('teams', [])
        if teams:
            active_teams = len([t for t in teams if t.get('members')])
            data['metrics']['collaboration'] = min(1.0, active_teams / max(1, len(teams)))
        
        return data
    
    def generate_executive_summary(self, data: Dict[str, Any]) -> str:
        """Generiert eine Führungskräfte-Zusammenfassung"""
        summary = "# Executive Summary\n\n"
        summary += f"**Berichtszeitraum:** {data['period']['start_date'][:10]} bis {data['period']['end_date'][:10]} ({data['period']['days']} Tage)\n"
        summary += f"**Generiert am:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        # Key Performance Indicators
        summary += "## Key Performance Indicators\n\n"
        
        tasks = data['tasks']
        if tasks['total'] > 0:
            completion_rate = tasks['completed'] / tasks['total']
            summary += f"- **Aufgaben-Abschlussrate:** {completion_rate:.1%} ({tasks['completed']}/{tasks['total']})\n"
        
        summary += f"- **Aktive KI-Agenten:** {data['agents']['active_count']}\n"
        summary += f"- **Produktivität:** {data['metrics']['productivity']:.1%}\n"
        summary += f"- **Qualitätsbewertung:** {data['metrics']['quality']:.1f}/5.0\n"
        summary += f"- **Effizienz:** {data['metrics']['efficiency']:.1%}\n\n"
        
        # Highlights
        summary += "## Highlights\n\n"
        
        if data['tasks']['recent_completions']:
            summary += f"✅ **{len(data['tasks']['recent_completions'])} Aufgaben erfolgreich abgeschlossen**\n"
            for task in data['tasks']['recent_completions'][:3]:
                summary += f"   - {task.get('title', 'Unbenannte Aufgabe')}\n"
            summary += "\n"
        
        if data['agents']['top_performers']:
            summary += "🏆 **Top-Performance Agenten:**\n"
            for agent in data['agents']['top_performers']:
                summary += f"   - {agent['agent_id']}: {agent['completion_rate']:.1%} Erfolgsrate\n"
            summary += "\n"
        
        if data['improvements']['recent_suggestions']:
            summary += f"💡 **{len(data['improvements']['recent_suggestions'])} neue Verbesserungsvorschläge**\n\n"
        
        # Concerns
        concerns = []
        
        if data['tasks']['failed'] > 0:
            concerns.append(f"{data['tasks']['failed']} fehlgeschlagene Aufgaben")
        
        if data['issues']['critical'] > 0:
            concerns.append(f"{data['issues']['critical']} kritische Probleme")
        
        if data['agents']['underperformers']:
            concerns.append(f"{len(data['agents']['underperformers'])} Agenten mit niedriger Performance")
        
        if concerns:
            summary += "## Handlungsbedarf\n\n"
            for concern in concerns:
                summary += f"⚠️ {concern}\n"
            summary += "\n"
        
        # Strategic Recommendations
        summary += "## Strategische Empfehlungen\n\n"
        
        if data['metrics']['productivity'] < 0.7:
            summary += "- **Produktivitätssteigerung:** Überprüfung der Arbeitsabläufe und Ressourcenallokation\n"
        
        if data['metrics']['quality'] < 3.5:
            summary += "- **Qualitätsverbesserung:** Zusätzliche Schulungen und Qualitätskontrolle\n"
        
        if data['agents']['underperformers']:
            summary += "- **Agent-Optimierung:** Spezielle Unterstützung für underperformende Agenten\n"
        
        if data['improvements']['suggestions_count'] > 10:
            summary += "- **Innovation Management:** Priorisierung und Umsetzung der Verbesserungsvorschläge\n"
        
        summary += "\n"
        
        # Next Steps
        summary += "## Nächste Schritte\n\n"
        summary += "1. Review der kritischen Probleme und Sofortmaßnahmen\n"
        summary += "2. Ressourcenallokation für Top-Priorität Aufgaben\n"
        summary += "3. Performance-Gespräche mit underperformenden Agenten\n"
        summary += "4. Bewertung und Priorisierung der Verbesserungsvorschläge\n\n"
        
        return summary
    
    def generate_technical_report(self, data: Dict[str, Any]) -> str:
        """Generiert einen technischen Detailbericht"""
        report = "# Technical Performance Report\n\n"
        report += f"**Berichtszeitraum:** {data['period']['start_date'][:10]} bis {data['period']['end_date'][:10]}\n"
        report += f"**Generiert am:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        # System Overview
        report += "## System Overview\n\n"
        report += f"- **Gesamte Aufgaben:** {data['tasks']['total']}\n"
        report += f"- **Abgeschlossen:** {data['tasks']['completed']}\n"
        report += f"- **In Bearbeitung:** {data['tasks']['in_progress']}\n"
        report += f"- **Offen:** {data['tasks']['open']}\n"
        report += f"- **Fehlgeschlagen:** {data['tasks']['failed']}\n"
        report += f"- **Aktive Agenten:** {data['agents']['active_count']}\n\n"
        
        # Performance Metrics
        report += "## Performance Metrics\n\n"
        
        metrics = data['metrics']
        report += f"| Metrik | Wert | Status |\n"
        report += f"|--------|------|--------|\n"
        report += f"| Produktivität | {metrics['productivity']:.1%} | {'✅' if metrics['productivity'] >= 0.8 else '⚠️' if metrics['productivity'] >= 0.6 else '❌'} |\n"
        report += f"| Qualität | {metrics['quality']:.1f}/5.0 | {'✅' if metrics['quality'] >= 4.0 else '⚠️' if metrics['quality'] >= 3.0 else '❌'} |\n"
        report += f"| Effizienz | {metrics['efficiency']:.1%} | {'✅' if metrics['efficiency'] >= 0.8 else '⚠️' if metrics['efficiency'] >= 0.6 else '❌'} |\n"
        report += f"| Kollaboration | {metrics['collaboration']:.1%} | {'✅' if metrics['collaboration'] >= 0.8 else '⚠️' if metrics['collaboration'] >= 0.6 else '❌'} |\n\n"
        
        # Agent Performance Details
        if data['agents']['top_performers'] or data['agents']['underperformers']:
            report += "## Agent Performance Analysis\n\n"
            
            if data['agents']['top_performers']:
                report += "### Top Performers\n\n"
                for agent in data['agents']['top_performers']:
                    report += f"- **{agent['agent_id']}**\n"
                    report += f"  - Completion Rate: {agent['completion_rate']:.1%}\n"
                    report += f"  - Quality Score: {agent['quality_score']:.1f}/5.0\n"
                    report += f"  - Total Tasks: {agent['total_tasks']}\n\n"
            
            if data['agents']['underperformers']:
                report += "### Performance Issues\n\n"
                for agent in data['agents']['underperformers']:
                    report += f"- **{agent['agent_id']}** ⚠️\n"
                    report += f"  - Completion Rate: {agent['completion_rate']:.1%} (Below 70%)\n"
                    report += f"  - Quality Score: {agent['quality_score']:.1f}/5.0\n"
                    report += f"  - Total Tasks: {agent['total_tasks']}\n"
                    report += f"  - **Action Required:** Performance review and optimization\n\n"
        
        # Recent Issues
        if data['issues']['recent_issues']:
            report += "## Recent Issues\n\n"
            report += f"Total Issues Detected: {data['issues']['total_reported']}\n"
            report += f"Critical Issues: {data['issues']['critical']}\n\n"
            
            report += "### Issue Details\n\n"
            for issue in data['issues']['recent_issues'][:10]:  # Top 10
                report += f"- **{issue['file']}** ({issue['date'][:10]})\n"
                report += f"  - Type: {issue['type']}\n\n"
        
        # Recent Completions
        if data['tasks']['recent_completions']:
            report += "## Recent Task Completions\n\n"
            for task in data['tasks']['recent_completions']:
                report += f"- **{task.get('title', 'Unbenannte Aufgabe')}**\n"
                report += f"  - ID: {task.get('task_id')}\n"
                report += f"  - Completed: {task.get('completed_date', 'Unknown')[:10]}\n"
                if task.get('assigned_to'):
                    report += f"  - Agent: {task.get('assigned_to')}\n"
                report += "\n"
        
        # Recommendations
        report += "## Technical Recommendations\n\n"
        
        if data['metrics']['efficiency'] < 0.7:
            report += "### Performance Optimization\n"
            report += "- Analyze task allocation algorithms\n"
            report += "- Review agent workload distribution\n"
            report += "- Implement performance monitoring\n\n"
        
        if data['issues']['critical'] > 0:
            report += "### Critical Issue Resolution\n"
            report += "- Immediate investigation of critical issues\n"
            report += "- Implement error prevention measures\n"
            report += "- Enhance monitoring and alerting\n\n"
        
        if data['agents']['underperformers']:
            report += "### Agent Optimization\n"
            report += "- Performance analysis for underperforming agents\n"
            report += "- Configuration review and tuning\n"
            report += "- Additional training or capability enhancement\n\n"
        
        return report
    
    def generate_operational_summary(self, data: Dict[str, Any]) -> str:
        """Generiert eine operative Zusammenfassung"""
        summary = "# Operational Summary\n\n"
        summary += f"**Berichtszeitraum:** {data['period']['start_date'][:10]} bis {data['period']['end_date'][:10]}\n"
        summary += f"**Generiert am:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        # Daily Operations
        summary += "## Tägliche Operationen\n\n"
        
        daily_productivity = data['tasks']['completed'] / max(1, data['period']['days'])
        summary += f"- **Durchschnittliche tägliche Aufgaben-Completion:** {daily_productivity:.1f} Aufgaben/Tag\n"
        summary += f"- **Aktive Agenten:** {data['agents']['active_count']}\n"
        summary += f"- **Offene Aufgaben:** {data['tasks']['open']}\n"
        summary += f"- **Aufgaben in Bearbeitung:** {data['tasks']['in_progress']}\n\n"
        
        # Workflow Status
        summary += "## Workflow-Status\n\n"
        
        if data['tasks']['total'] > 0:
            open_percentage = data['tasks']['open'] / data['tasks']['total']
            in_progress_percentage = data['tasks']['in_progress'] / data['tasks']['total']
            completed_percentage = data['tasks']['completed'] / data['tasks']['total']
            
            summary += f"- **Offene Aufgaben:** {open_percentage:.1%}\n"
            summary += f"- **In Bearbeitung:** {in_progress_percentage:.1%}\n"
            summary += f"- **Abgeschlossen:** {completed_percentage:.1%}\n\n"
        
        # Resource Utilization
        summary += "## Ressourcen-Auslastung\n\n"
        
        if data['agents']['active_count'] > 0:
            tasks_per_agent = data['tasks']['total'] / data['agents']['active_count']
            summary += f"- **Aufgaben pro Agent:** {tasks_per_agent:.1f}\n"
            
            if tasks_per_agent > 10:
                summary += "  - ⚠️ Hohe Auslastung - Zusätzliche Ressourcen erwägen\n"
            elif tasks_per_agent < 3:
                summary += "  - ℹ️ Niedrige Auslastung - Kapazität für zusätzliche Aufgaben\n"
            else:
                summary += "  - ✅ Ausgewogene Auslastung\n"
        
        summary += "\n"
        
        # Quality Control
        summary += "## Qualitätskontrolle\n\n"
        
        if data['tasks']['failed'] > 0:
            failure_rate = data['tasks']['failed'] / data['tasks']['total']
            summary += f"- **Fehlerrate:** {failure_rate:.1%}\n"
            
            if failure_rate > 0.1:
                summary += "  - ❌ Hohe Fehlerrate - Sofortige Maßnahmen erforderlich\n"
            elif failure_rate > 0.05:
                summary += "  - ⚠️ Erhöhte Fehlerrate - Überwachung verstärken\n"
            else:
                summary += "  - ✅ Akzeptable Fehlerrate\n"
        else:
            summary += "- **Fehlerrate:** 0% ✅\n"
        
        summary += f"- **Durchschnittliche Qualitätsbewertung:** {data['metrics']['quality']:.1f}/5.0\n\n"
        
        # Issues and Incidents
        if data['issues']['total_reported'] > 0:
            summary += "## Probleme und Vorfälle\n\n"
            summary += f"- **Gemeldete Probleme:** {data['issues']['total_reported']}\n"
            summary += f"- **Kritische Probleme:** {data['issues']['critical']}\n"
            
            if data['issues']['critical'] > 0:
                summary += "  - 🚨 Sofortige Aufmerksamkeit erforderlich\n"
            
            summary += "\n"
        
        # Improvement Activities
        if data['improvements']['suggestions_count'] > 0:
            summary += "## Verbesserungsaktivitäten\n\n"
            summary += f"- **Verbesserungsvorschläge:** {data['improvements']['suggestions_count']}\n"
            summary += f"- **Kürzlich hinzugefügt:** {len(data['improvements']['recent_suggestions'])}\n\n"
        
        # Action Items
        summary += "## Handlungsempfehlungen\n\n"
        
        action_items = []
        
        if data['tasks']['open'] > data['tasks']['in_progress'] * 2:
            action_items.append("Aufgaben-Priorisierung und -Zuweisung überprüfen")
        
        if data['metrics']['efficiency'] < 0.7:
            action_items.append("Workflow-Optimierung durchführen")
        
        if data['issues']['critical'] > 0:
            action_items.append("Kritische Probleme sofort adressieren")
        
        if data['agents']['underperformers']:
            action_items.append("Performance-Support für schwächere Agenten")
        
        if not action_items:
            action_items.append("Aktueller Betrieb läuft stabil - Routineüberwachung fortsetzen")
        
        for i, item in enumerate(action_items, 1):
            summary += f"{i}. {item}\n"
        
        summary += "\n"
        
        return summary
    
    def generate_automated_summary(self, summary_type: str = 'weekly', template: str = 'executive') -> str:
        """Generiert eine automatisierte Zusammenfassung"""
        # Bestimme Zeitraum basierend auf Typ
        days_mapping = {
            'daily': 1,
            'weekly': 7,
            'monthly': 30,
            'project_status': 30,
            'performance': 14,
            'issues': 7,
            'improvements': 14
        }
        
        days = days_mapping.get(summary_type, 7)
        
        # Sammle Daten
        data = self.collect_project_data(days)
        
        # Generiere basierend auf Template
        if template == 'executive':
            summary = self.generate_executive_summary(data)
        elif template == 'technical':
            summary = self.generate_technical_report(data)
        elif template == 'operational':
            summary = self.generate_operational_summary(data)
        else:
            # Default: Executive Summary
            summary = self.generate_executive_summary(data)
        
        # Speichere Summary
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{summary_type}_{template}_summary_{timestamp}.md"
        filepath = os.path.join(self.summaries_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(summary)
        
        return summary
    
    def schedule_regular_summaries(self) -> Dict[str, str]:
        """Plant regelmäßige Zusammenfassungen"""
        scheduled_summaries = {}
        
        # Tägliche operative Zusammenfassung
        daily_summary = self.generate_automated_summary('daily', 'operational')
        scheduled_summaries['daily_operational'] = 'Generiert'
        
        # Wöchentliche Executive Summary
        weekly_summary = self.generate_automated_summary('weekly', 'executive')
        scheduled_summaries['weekly_executive'] = 'Generiert'
        
        # Wöchentlicher technischer Report
        weekly_technical = self.generate_automated_summary('weekly', 'technical')
        scheduled_summaries['weekly_technical'] = 'Generiert'
        
        return scheduled_summaries
    
    def create_summary_dashboard(self) -> str:
        """Erstellt ein Dashboard mit allen verfügbaren Summaries"""
        dashboard = "# Summary Dashboard\n\n"
        dashboard += f"Generiert am: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        # Verfügbare Summaries auflisten
        if os.path.exists(self.summaries_dir):
            summary_files = [f for f in os.listdir(self.summaries_dir) if f.endswith('.md')]
            
            if summary_files:
                dashboard += "## Verfügbare Zusammenfassungen\n\n"
                
                # Gruppiere nach Typ
                by_type = defaultdict(list)
                for filename in summary_files:
                    parts = filename.split('_')
                    if len(parts) >= 2:
                        summary_type = parts[0]
                        by_type[summary_type].append(filename)
                
                for summary_type, files in by_type.items():
                    type_name = self.summary_types.get(summary_type, summary_type.title())
                    dashboard += f"### {type_name}\n\n"
                    
                    # Sortiere nach Datum (neueste zuerst)
                    sorted_files = sorted(files, reverse=True)
                    
                    for filename in sorted_files[:5]:  # Zeige nur die 5 neuesten
                        # Extrahiere Datum aus Dateiname
                        date_match = re.search(r'(\d{8}_\d{6})', filename)
                        if date_match:
                            timestamp = date_match.group(1)
                            try:
                                date_obj = datetime.strptime(timestamp, '%Y%m%d_%H%M%S')
                                date_str = date_obj.strftime('%Y-%m-%d %H:%M')
                            except:
                                date_str = timestamp
                        else:
                            date_str = 'Unknown'
                        
                        dashboard += f"- [{filename}]({filename}) - {date_str}\n"
                    
                    dashboard += "\n"
            else:
                dashboard += "Keine Zusammenfassungen verfügbar.\n\n"
        
        # Quick Actions
        dashboard += "## Quick Actions\n\n"
        dashboard += "- [Neue Executive Summary generieren](generate_executive_summary)\n"
        dashboard += "- [Technischen Report erstellen](generate_technical_report)\n"
        dashboard += "- [Operative Zusammenfassung](generate_operational_summary)\n"
        dashboard += "- [Alle Summaries aktualisieren](update_all_summaries)\n\n"
        
        # Summary-Statistiken
        data = self.collect_project_data(7)  # Letzte 7 Tage
        
        dashboard += "## Aktuelle Kennzahlen (7 Tage)\n\n"
        dashboard += f"- **Produktivität:** {data['metrics']['productivity']:.1%}\n"
        dashboard += f"- **Qualität:** {data['metrics']['quality']:.1f}/5.0\n"
        dashboard += f"- **Effizienz:** {data['metrics']['efficiency']:.1%}\n"
        dashboard += f"- **Abgeschlossene Aufgaben:** {data['tasks']['completed']}\n"
        dashboard += f"- **Aktive Agenten:** {data['agents']['active_count']}\n\n"
        
        return dashboard

if __name__ == '__main__':
    # Test des Summary Generators
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    summary_gen = SummaryGenerator(project_root)
    
    print("=== Summary Generator Test ===")
    
    # Sammle Projektdaten
    data = summary_gen.collect_project_data(7)
    print(f"Projektdaten gesammelt: {data['tasks']['total']} Aufgaben, {data['agents']['active_count']} Agenten")
    
    # Generiere Executive Summary
    exec_summary = summary_gen.generate_automated_summary('weekly', 'executive')
    print(f"Executive Summary generiert: {len(exec_summary)} Zeichen")
    
    # Erstelle Dashboard
    dashboard = summary_gen.create_summary_dashboard()
    print(f"Dashboard erstellt: {len(dashboard)} Zeichen")

