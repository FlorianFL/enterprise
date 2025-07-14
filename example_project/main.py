import json
import os
from datetime import datetime

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
PROJECT_MANIFEST_PATH = os.path.join(PROJECT_ROOT, 'project_manifest.json')

def read_project_manifest():
    """Liest das project_manifest.json und gibt es als Dictionary zurück."""
    with open(PROJECT_MANIFEST_PATH, 'r') as f:
        return json.load(f)

def write_project_manifest(data):
    """Schreibt das gegebene Dictionary in project_manifest.json."""
    data['last_updated'] = datetime.now().isoformat(timespec='seconds') + 'Z'
    with open(PROJECT_MANIFEST_PATH, 'w') as f:
        json.dump(data, f, indent=2)

def log_action(ai_name, action_type, affected_item, description, output=''):
    """Protokolliert eine Aktion im history-Verzeichnis."""
    timestamp = datetime.now().isoformat(timespec='seconds') + 'Z'
    log_filename = f"{timestamp.replace(':', '-')}_{ai_name}_{affected_item.replace('/', '-')}.log"
    log_filepath = os.path.join(PROJECT_ROOT, 'history', log_filename)

    log_entry = f"{timestamp} - {ai_name} - {action_type} - {affected_item}\n"
    log_entry += f"Beschreibung: {description}\n"
    log_entry += f"Output: {output}\n\n"

    with open(log_filepath, 'a') as f:
        f.write(log_entry)

def read_task_file(task_id):
    """Liest eine Aufgaben-Datei und gibt ihren Inhalt zurück."""
    task_filepath = os.path.join(PROJECT_ROOT, 'tasks', f'{task_id}.md')
    with open(task_filepath, 'r') as f:
        return f.read()

def write_task_file(task_id, content):
    """Schreibt den gegebenen Inhalt in eine Aufgaben-Datei."""
    task_filepath = os.path.join(PROJECT_ROOT, 'tasks', f'{task_id}.md')
    with open(task_filepath, 'w') as f:
        f.write(content)

def update_task_status_in_manifest(manifest, task_id, new_status, ai_name=None):
    """Aktualisiert den Status einer Aufgabe im Projekt-Manifest."""
    for task in manifest['tasks']:
        if task['task_id'] == task_id:
            task['status'] = new_status
            if new_status == 'in_progress' and ai_name:
                task['assigned_ai'] = ai_name
            elif new_status == 'completed':
                task['completed_date'] = datetime.now().strftime('%Y-%m-%d')
            break
    return manifest

def process_task_001(ai_name):
    """Simuliert die Bearbeitung von task_001_setup."""
    task_id = 'task_001_setup'
    print(f"KI {ai_name} beginnt mit der Bearbeitung von {task_id}.")

    # 1. Manifest lesen
    manifest = read_project_manifest()
    if manifest.get('kill_switch', False):
        print(f"Kill-Switch ist aktiviert. KI {ai_name} stoppt die Arbeit.")
        log_action(ai_name, 'PROJECT_STOP', 'Kill-Switch', 'Arbeit aufgrund des aktivierten Kill-Switches eingestellt.')
        return
    
    # Simulate checking for kill keyword in a hypothetical input
    kill_keyword = manifest.get('kill_keyword', '')
    hypothetical_input = "This is a normal message. No kill keyword here."
    # Uncomment the line below to test the kill keyword functionality
    # hypothetical_input = f"Urgent: {kill_keyword} - Stop all operations!"

    if kill_keyword and kill_keyword in hypothetical_input:
        print(f"Kill-Keyword '{kill_keyword}' erkannt. KI {ai_name} stoppt die Arbeit.")
        log_action(ai_name, 'PROJECT_STOP', 'Kill-Keyword', f"Arbeit aufgrund des erkannten Kill-Keywords '{kill_keyword}' eingestellt.")
        return

    # 2. Status in Manifest und Task-Datei auf 'in_progress' setzen
    manifest = update_task_status_in_manifest(manifest, task_id, 'in_progress', ai_name)
    write_project_manifest(manifest)
    log_action(ai_name, 'TASK_STATUS_UPDATE', task_id, f"Status von {task_id} auf 'in_progress' gesetzt.")

    task_content = read_task_file(task_id)
    task_content = task_content.replace('**Status:** open', '**Status:** in_progress')
    task_content = task_content.replace('**Zugewiesen an:** unassigned', f'**Zugewiesen an:** {ai_name}')
    write_task_file(task_id, task_content)
    log_action(ai_name, 'FILE_UPDATE', task_id, f"Task-Datei {task_id}.md aktualisiert: Status auf 'in_progress' und zugewiesene KI.")

    # 3. Schritte ausführen (simuliert)
    print("Simuliere die Überprüfung der Verzeichnisse...")
    log_action(ai_name, 'SIMULATED_ACTION', 'Verzeichnisprüfung', 'Überprüfung der erforderlichen Verzeichnisse abgeschlossen.')

    print("Simuliere die Erstellung/Überprüfung von requirements.txt...")
    # Hier könnte eine echte Logik zur Erstellung/Überprüfung stehen
    requirements_path = os.path.join(PROJECT_ROOT, 'ai_scripts', 'requirements.txt')
    if not os.path.exists(requirements_path):
        with open(requirements_path, 'w') as f:
            f.write('numpy\npandas\n') # Beispiel-Abhängigkeiten
        log_action(ai_name, 'FILE_CREATE', 'ai_scripts/requirements.txt', 'requirements.txt erstellt.')
    else:
        log_action(ai_name, 'FILE_CHECK', 'ai_scripts/requirements.txt', 'requirements.txt existiert bereits.')

    print("Simuliere die Installation von Abhängigkeiten...")
    # In einem echten Szenario würde hier pip install -r requirements.txt ausgeführt
    log_action(ai_name, 'SIMULATED_ACTION', 'Abhängigkeitsinstallation', 'Abhängigkeiten simuliert installiert.')

    # 4. Status in Manifest und Task-Datei auf 'completed' setzen
    manifest = read_project_manifest()
    manifest = update_task_status_in_manifest(manifest, task_id, 'completed')
    write_project_manifest(manifest)
    log_action(ai_name, 'TASK_STATUS_UPDATE', task_id, f"Status von {task_id} auf 'completed' gesetzt.")

    task_content = read_task_file(task_id)
    task_content = task_content.replace('**Status:** in_progress', '**Status:** completed')
    task_content = task_content.replace('- [ ] Überprüfen, ob alle erforderlichen Verzeichnisse vorhanden sind.', '- [x] Überprüfen, ob alle erforderlichen Verzeichnisse vorhanden sind.')
    task_content = task_content.replace('- [ ] Eine `requirements.txt` Datei im `ai_scripts/` Verzeichnis erstellen, falls nicht vorhanden.', '- [x] Eine `requirements.txt` Datei im `ai_scripts/` Verzeichnis erstellen, falls nicht vorhanden.')
    task_content = task_content.replace('- [ ] Die Abhängigkeiten aus der `requirements.txt` installieren.', '- [x] Die Abhängigkeiten aus der `requirements.txt` installieren.')
    task_content = task_content.replace('- [ ] Den Status dieser Aufgabe auf `completed` setzen.', '- [x] Den Status dieser Aufgabe auf `completed` setzen.')
    task_content += f"\n### {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {ai_name}\n- Aufgabe erfolgreich abgeschlossen.\n"
    write_task_file(task_id, task_content)
    log_action(ai_name, 'FILE_UPDATE', task_id, f"Task-Datei {task_id}.md aktualisiert: Status auf 'completed' und Schritte markiert.")

    print(f"KI {ai_name} hat {task_id} erfolgreich abgeschlossen.")


if __name__ == '__main__':
    ai_agent_name = 'AI_Agent_Prototype'
    
    # Initiales Setup des project_manifest.json, falls noch keine tasks vorhanden sind
    manifest = read_project_manifest()
    if not manifest['tasks']:
        manifest['tasks'].append({
            "task_id": "task_001_setup",
            "title": "Initiales Setup des Projektumfelds",
            "status": "open",
            "assigned_ai": "unassigned",
            "due_date": None,
            "completed_date": None
        })
        write_project_manifest(manifest)
        print("project_manifest.json mit initialer Aufgabe aktualisiert.")

    # KI-Logik: Nächste offene Aufgabe finden und bearbeiten
    manifest = read_project_manifest()
    if manifest.get('kill_switch', False):
        print(f"Kill-Switch ist aktiviert. KI {ai_agent_name} stoppt die Arbeit.")
        log_action(ai_agent_name, 'PROJECT_STOP', 'Kill-Switch', 'Arbeit aufgrund des aktivierten Kill-Switches eingestellt.')
    else:
        kill_keyword = manifest.get('kill_keyword', '')
        hypothetical_input = "This is a normal message. No kill keyword here."
        # Uncomment the line below to test the kill keyword functionality
        # hypothetical_input = f"Urgent: {kill_keyword} - Stop all operations!"

        if kill_keyword and kill_keyword in hypothetical_input:
            print(f"Kill-Keyword '{kill_keyword}' erkannt. KI {ai_agent_name} stoppt die Arbeit.")
            log_action(ai_agent_name, 'PROJECT_STOP', 'Kill-Keyword', f"Arbeit aufgrund des erkannten Kill-Keywords '{kill_keyword}' eingestellt.")
        else:
            for task in manifest['tasks']:
                if task['status'] == 'open':
                    if task['task_id'] == 'task_001_setup':
                        process_task_001(ai_agent_name)
                    else:
                        print(f"Unbekannte Aufgabe: {task['task_id']}. Überspringe.")
                    break
            else:
                print("Keine offenen Aufgaben gefunden.")


