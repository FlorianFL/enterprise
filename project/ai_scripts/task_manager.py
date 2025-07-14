import json
import os

class TaskManager:
    def __init__(self, project_root):
        self.project_root = project_root
        self.manifest_path = os.path.join(project_root, 'project_manifest.json')
        self.tasks_dir = os.path.join(project_root, 'tasks')

    def load_manifest(self):
        with open(self.manifest_path, 'r') as f:
            return json.load(f)

    def save_manifest(self, manifest):
        with open(self.manifest_path, 'w') as f:
            json.dump(manifest, f, indent=2)

    def get_available_tasks(self):
        manifest = self.load_manifest()
        available_tasks = []
        for task in manifest.get('tasks', []):
            if task.get('status') == 'open':
                available_tasks.append(task)
        return available_tasks

    def prioritize_tasks(self, tasks):
        # Simple prioritization logic: prioritize tasks with 'high' urgency first
        # This can be extended with more complex logic based on dependencies, complexity, etc.
        prioritized_tasks = sorted(tasks, key=lambda x: x.get('urgency', 'medium'),
                                   reverse=True)  # 'high' > 'medium' > 'low'
        return prioritized_tasks

    def assign_task(self, task_id, ai_agent_id):
        manifest = self.load_manifest()
        for task in manifest.get('tasks', []):
            if task.get('task_id') == task_id:
                task['assigned_ai'] = ai_agent_id
                task['status'] = 'assigned'
                self.save_manifest(manifest)
                return True
        return False

    def distribute_tasks(self):
        manifest = self.load_manifest()
        available_tasks = self.get_available_tasks()
        prioritized_tasks = self.prioritize_tasks(available_tasks)

        # Simple distribution logic: assign to available AI agents based on their roles
        # This needs to be expanded with actual AI agent availability and capabilities
        assigned_agents = manifest.get('assigned_ais', []) # This needs to be populated by the system
        teams = manifest.get('teams', [])

        # For now, just print the prioritized tasks and suggest manual assignment
        print("Prioritized tasks:")
        for task in prioritized_tasks:
            print(f"- {task['title']} (ID: {task['task_id']}, Urgency: {task.get('urgency', 'medium')})")
        print("\nFurther development needed to automatically assign tasks to suitable AI agents based on their profiles and availability.")

if __name__ == '__main__':
    # This is for testing purposes. In a real scenario, this would be called by main.py or an AI agent.
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    task_manager = TaskManager(project_root)
    task_manager.distribute_tasks()


