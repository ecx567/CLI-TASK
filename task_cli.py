

import json
import sys
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any


class TaskTracker:
    """Main class for managing tasks."""
    
    def __init__(self, data_file: str = "tasks.json"):
        """Initialize TaskTracker with data file path."""
        self.data_file = Path(data_file)
        self.tasks = self._load_tasks()
    
    def _load_tasks(self) -> Dict[str, Any]:
        """Load tasks from JSON file, create empty structure if file doesn't exist."""
        if not self.data_file.exists():
            return {"tasks": [], "next_id": 1}
        
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Ensure the structure is correct
                if "tasks" not in data:
                    data["tasks"] = []
                if "next_id" not in data:
                    data["next_id"] = 1
                return data
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error loading tasks file: {e}")
            print("Creating new tasks file...")
            return {"tasks": [], "next_id": 1}
    
    def _save_tasks(self) -> None:
        """Save tasks to JSON file."""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(self.tasks, f, indent=2, ensure_ascii=False)
        except IOError as e:
            print(f"Error saving tasks file: {e}")
            sys.exit(1)
    
    def _get_current_timestamp(self) -> str:
        """Get current timestamp in readable format with microseconds for precision."""
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    
    def _find_task_by_id(self, task_id: int) -> Optional[Dict[str, Any]]:
        """Find task by ID."""
        for task in self.tasks["tasks"]:
            if task["id"] == task_id:
                return task
        return None
    
    def add_task(self, description: str) -> None:
        """Add a new task."""
        if not description.strip():
            print("Error: Task description cannot be empty.")
            return
        
        current_time = self._get_current_timestamp()
        new_task = {
            "id": self.tasks["next_id"],
            "description": description.strip(),
            "status": "todo",
            "createdAt": current_time,
            "updatedAt": current_time
        }
        
        self.tasks["tasks"].append(new_task)
        self.tasks["next_id"] += 1
        self._save_tasks()
        
        print(f"Task added successfully (ID: {new_task['id']})")
    
    def update_task(self, task_id: int, new_description: str) -> None:
        """Update task description."""
        if not new_description.strip():
            print("Error: Task description cannot be empty.")
            return
        
        task = self._find_task_by_id(task_id)
        if not task:
            print(f"Error: Task with ID {task_id} not found.")
            return
        
        task["description"] = new_description.strip()
        task["updatedAt"] = self._get_current_timestamp()
        self._save_tasks()
        
        print(f"Task {task_id} updated successfully.")
    
    def delete_task(self, task_id: int) -> None:
        """Delete a task."""
        task = self._find_task_by_id(task_id)
        if not task:
            print(f"Error: Task with ID {task_id} not found.")
            return
        
        self.tasks["tasks"] = [t for t in self.tasks["tasks"] if t["id"] != task_id]
        self._save_tasks()
        
        print(f"Task {task_id} deleted successfully.")
    
    def mark_in_progress(self, task_id: int) -> None:
        """Mark task as in progress."""
        task = self._find_task_by_id(task_id)
        if not task:
            print(f"Error: Task with ID {task_id} not found.")
            return
        
        if task["status"] == "in-progress":
            print(f"Task {task_id} is already in progress.")
            return
        
        task["status"] = "in-progress"
        task["updatedAt"] = self._get_current_timestamp()
        self._save_tasks()
        
        print(f"Task {task_id} marked as in progress.")
    
    def mark_done(self, task_id: int) -> None:
        """Mark task as done."""
        task = self._find_task_by_id(task_id)
        if not task:
            print(f"Error: Task with ID {task_id} not found.")
            return
        
        if task["status"] == "done":
            print(f"Task {task_id} is already done.")
            return
        
        task["status"] = "done"
        task["updatedAt"] = self._get_current_timestamp()
        self._save_tasks()
        
        print(f"Task {task_id} marked as done.")
    
    def list_tasks(self, status_filter: Optional[str] = None) -> None:
        """List tasks with optional status filter."""
        valid_statuses = ["todo", "in-progress", "done"]
        
        if status_filter and status_filter not in valid_statuses:
            print(f"Error: Invalid status '{status_filter}'. Valid statuses are: {', '.join(valid_statuses)}")
            return
        
        tasks_to_show = self.tasks["tasks"]
        
        if status_filter:
            tasks_to_show = [task for task in tasks_to_show if task["status"] == status_filter]
        
        if not tasks_to_show:
            if status_filter:
                print(f"No tasks found with status '{status_filter}'.")
            else:
                print("No tasks found.")
            return
        
        # Print header
        print(f"\n{'ID':<4} {'Description':<30} {'Status':<12} {'Created':<20} {'Updated':<20}")
        print("-" * 86)
        
        # Print tasks
        for task in tasks_to_show:
            description = task['description']
            if len(description) > 30:
                description = description[:27] + "..."
            
            print(f"{task['id']:<4} {description:<30} {task['status']:<12} "
                  f"{task['createdAt']:<20} {task['updatedAt']:<20}")
        
        print(f"\nTotal: {len(tasks_to_show)} task(s)")


def print_usage():
    """Print usage information."""
    print("Task Tracker CLI - Manage your tasks from the command line")
    print("\nUsage:")
    print("  python task_cli.py add \"<description>\"")
    print("  python task_cli.py update <id> \"<description>\"")
    print("  python task_cli.py delete <id>")
    print("  python task_cli.py mark-in-progress <id>")
    print("  python task_cli.py mark-done <id>")
    print("  python task_cli.py list [status]")
    print("\nExamples:")
    print("  python task_cli.py add \"Buy groceries\"")
    print("  python task_cli.py update 1 \"Buy groceries and cook dinner\"")
    print("  python task_cli.py delete 1")
    print("  python task_cli.py mark-in-progress 1")
    print("  python task_cli.py mark-done 1")
    print("  python task_cli.py list")
    print("  python task_cli.py list done")
    print("  python task_cli.py list todo")
    print("  python task_cli.py list in-progress")


def main():
    """Main entry point of the application."""
    # If no arguments provided, show help
    if len(sys.argv) < 2:
        print_usage()
        return
    
    command = sys.argv[1].lower()
    
    # Initialize task tracker
    tracker = TaskTracker()
    
    try:
        # Execute commands based on positional arguments
        if command == "add":
            if len(sys.argv) != 3:
                print("Error: 'add' command requires a description.")
                print("Usage: python task_cli.py add \"<description>\"")
                return
            tracker.add_task(sys.argv[2])
        
        elif command == "update":
            if len(sys.argv) != 4:
                print("Error: 'update' command requires an ID and description.")
                print("Usage: python task_cli.py update <id> \"<description>\"")
                return
            try:
                task_id = int(sys.argv[2])
                tracker.update_task(task_id, sys.argv[3])
            except ValueError:
                print("Error: Task ID must be a number.")
        
        elif command == "delete":
            if len(sys.argv) != 3:
                print("Error: 'delete' command requires a task ID.")
                print("Usage: python task_cli.py delete <id>")
                return
            try:
                task_id = int(sys.argv[2])
                tracker.delete_task(task_id)
            except ValueError:
                print("Error: Task ID must be a number.")
        
        elif command == "mark-in-progress":
            if len(sys.argv) != 3:
                print("Error: 'mark-in-progress' command requires a task ID.")
                print("Usage: python task_cli.py mark-in-progress <id>")
                return
            try:
                task_id = int(sys.argv[2])
                tracker.mark_in_progress(task_id)
            except ValueError:
                print("Error: Task ID must be a number.")
        
        elif command == "mark-done":
            if len(sys.argv) != 3:
                print("Error: 'mark-done' command requires a task ID.")
                print("Usage: python task_cli.py mark-done <id>")
                return
            try:
                task_id = int(sys.argv[2])
                tracker.mark_done(task_id)
            except ValueError:
                print("Error: Task ID must be a number.")
        
        elif command == "list":
            status_filter = None
            if len(sys.argv) == 3:
                status_filter = sys.argv[2]
            elif len(sys.argv) > 3:
                print("Error: 'list' command accepts only one optional status argument.")
                print("Usage: python task_cli.py list [status]")
                return
            tracker.list_tasks(status_filter)
        
        else:
            print(f"Error: Unknown command '{command}'")
            print_usage()
    
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
