

import json
import sys
import os
import argparse
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any
from config import config
from utils import (
    format_task_table, print_success, print_error, print_warning, print_info,
    get_color_for_status, get_color_for_priority, COLORS_AVAILABLE
)


class TaskTracker:
    """Main class for managing tasks with enhanced functionality."""
    
    def __init__(self, data_file: Optional[str] = None):
        """Initialize TaskTracker with data file path."""
        self.data_file = Path(data_file or config.get("data_file"))
        self.tasks = self._load_tasks()
        self._ensure_backup_dir()
    
    def _ensure_backup_dir(self) -> None:
        """Ensure backup directory exists."""
        if config.get("backup_enabled"):
            backup_dir = Path("backups")
            backup_dir.mkdir(exist_ok=True)
    
    def _load_tasks(self) -> Dict[str, Any]:
        """Load tasks from JSON file, create empty structure if file doesn't exist."""
        if not self.data_file.exists():
            return {
                "tasks": [], 
                "next_id": 1,
                "metadata": {
                    "version": "2.0",
                    "created": self._get_current_timestamp(),
                    "last_modified": self._get_current_timestamp()
                }
            }
        
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Ensure the structure is correct and migrate if needed
                if "tasks" not in data:
                    data["tasks"] = []
                if "next_id" not in data:
                    data["next_id"] = 1
                if "metadata" not in data:
                    data["metadata"] = {
                        "version": "2.0",
                        "created": self._get_current_timestamp(),
                        "last_modified": self._get_current_timestamp()
                    }
                
                # Migrate old tasks to new format if needed
                for task in data["tasks"]:
                    if "category" not in task:
                        task["category"] = "general"
                    if "priority" not in task:
                        task["priority"] = "medium"
                    if "due_date" not in task:
                        task["due_date"] = None
                
                return data
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error loading tasks file: {e}")
            print("Creating new tasks file...")
            return {
                "tasks": [], 
                "next_id": 1,
                "metadata": {
                    "version": "2.0",
                    "created": self._get_current_timestamp(),
                    "last_modified": self._get_current_timestamp()
                }
            }
    
    def _save_tasks(self) -> None:
        """Save tasks to JSON file with backup support."""
        # Create backup if enabled
        if config.get("backup_enabled") and self.data_file.exists():
            self._create_backup()
        
        # Update metadata
        self.tasks["metadata"]["last_modified"] = self._get_current_timestamp()
        
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(self.tasks, f, indent=2, ensure_ascii=False)
        except IOError as e:
            print(f"Error saving tasks file: {e}")
            sys.exit(1)
    
    def _create_backup(self) -> None:
        """Create a backup of the current tasks file."""
        try:
            backup_dir = Path("backups")
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = backup_dir / f"tasks_backup_{timestamp}.json"
            
            # Copy current file to backup
            import shutil
            shutil.copy2(self.data_file, backup_file)
            
            # Clean old backups
            self._cleanup_old_backups(backup_dir)
            
        except Exception as e:
            print(f"Warning: Could not create backup: {e}")
    
    def _cleanup_old_backups(self, backup_dir: Path) -> None:
        """Remove old backup files, keeping only the specified count."""
        try:
            backup_files = sorted(
                [f for f in backup_dir.glob("tasks_backup_*.json")],
                key=lambda x: x.stat().st_mtime,
                reverse=True
            )
            
            max_backups = config.get("backup_count", 5)
            for old_backup in backup_files[max_backups:]:
                old_backup.unlink()
                
        except Exception as e:
            print(f"Warning: Could not cleanup old backups: {e}")
    
    def _get_current_timestamp(self) -> str:
        """Get current timestamp in configurable format."""
        date_format = config.get("date_format")
        return datetime.now().strftime(date_format)
    
    def search_tasks(self, query: str) -> List[Dict[str, Any]]:
        """Search tasks by description content."""
        query_lower = query.lower()
        return [
            task for task in self.tasks["tasks"]
            if query_lower in task["description"].lower()
        ]
    
    def sort_tasks(self, tasks: List[Dict[str, Any]], sort_by: str = "id", 
                  reverse: bool = False) -> List[Dict[str, Any]]:
        """Sort tasks by specified criteria."""
        sort_functions = {
            "id": lambda t: t["id"],
            "description": lambda t: t["description"].lower(),
            "status": lambda t: t["status"],
            "priority": lambda t: config.get("valid_priorities").index(t["priority"]),
            "category": lambda t: t["category"],
            "created": lambda t: t["createdAt"],
            "updated": lambda t: t["updatedAt"],
            "due_date": lambda t: t.get("due_date") or "9999-12-31"
        }
        
        if sort_by not in sort_functions:
            print(f"Warning: Invalid sort option '{sort_by}'. Using 'id' instead.")
            sort_by = "id"
        
        return sorted(tasks, key=sort_functions[sort_by], reverse=reverse)
    
    def _find_task_by_id(self, task_id: int) -> Optional[Dict[str, Any]]:
        """Find task by ID."""
        for task in self.tasks["tasks"]:
            if task["id"] == task_id:
                return task
        return None
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get comprehensive statistics about tasks."""
        tasks = self.tasks["tasks"]
        total_tasks = len(tasks)
        
        if total_tasks == 0:
            return {"total": 0, "message": "No tasks found"}
        
        # Status statistics
        status_counts = {}
        for status in config.get("valid_statuses"):
            status_counts[status] = sum(1 for task in tasks if task["status"] == status)
        
        # Priority statistics
        priority_counts = {}
        for priority in config.get("valid_priorities"):
            priority_counts[priority] = sum(1 for task in tasks if task["priority"] == priority)
        
        # Category statistics
        categories = {}
        for task in tasks:
            category = task.get("category", "general")
            categories[category] = categories.get(category, 0) + 1
        
        # Due date statistics
        today = datetime.now().date()
        overdue = 0
        due_today = 0
        due_this_week = 0
        
        for task in tasks:
            if task.get("due_date"):
                try:
                    due_date = datetime.strptime(task["due_date"], "%Y-%m-%d").date()
                    days_until = (due_date - today).days
                    
                    if days_until < 0:
                        overdue += 1
                    elif days_until == 0:
                        due_today += 1
                    elif days_until <= 7:
                        due_this_week += 1
                except ValueError:
                    pass
        
        # Completion rate
        completed = status_counts.get("done", 0)
        completion_rate = (completed / total_tasks * 100) if total_tasks > 0 else 0
        
        # Time-based statistics
        created_this_week = 0
        completed_this_week = 0
        week_ago = (datetime.now() - timedelta(days=7)).strftime(config.get("date_format"))
        
        for task in tasks:
            if task["createdAt"] > week_ago:
                created_this_week += 1
            
            if (task["status"] == "done" and 
                task.get("updatedAt", "") > week_ago):
                completed_this_week += 1
        
        return {
            "total": total_tasks,
            "status_counts": status_counts,
            "priority_counts": priority_counts,
            "categories": categories,
            "completion_rate": completion_rate,
            "due_stats": {
                "overdue": overdue,
                "due_today": due_today,
                "due_this_week": due_this_week
            },
            "weekly_stats": {
                "created_this_week": created_this_week,
                "completed_this_week": completed_this_week
            }
        }
    
    def print_statistics(self) -> None:
        """Print formatted statistics report."""
        stats = self.get_statistics()
        
        if stats.get("message"):
            print_info(stats["message"])
            return
        
        print_info("📊 Task Statistics Report")
        print("=" * 50)
        
        # Overall statistics
        print(f"\n📋 Overall Statistics:")
        print(f"   Total tasks: {stats['total']}")
        print(f"   Completion rate: {stats['completion_rate']:.1f}%")
        
        # Status breakdown
        print(f"\n📈 Status Breakdown:")
        for status, count in stats['status_counts'].items():
            percentage = (count / stats['total'] * 100) if stats['total'] > 0 else 0
            if COLORS_AVAILABLE:
                color = get_color_for_status(status)
                print(f"   {color}{status.capitalize()}: {count} ({percentage:.1f}%)")
            else:
                print(f"   {status.capitalize()}: {count} ({percentage:.1f}%)")
        
        # Priority breakdown
        print(f"\n🎯 Priority Breakdown:")
        for priority, count in stats['priority_counts'].items():
            percentage = (count / stats['total'] * 100) if stats['total'] > 0 else 0
            if COLORS_AVAILABLE:
                color = get_color_for_priority(priority)
                print(f"   {color}{priority.capitalize()}: {count} ({percentage:.1f}%)")
            else:
                print(f"   {priority.capitalize()}: {count} ({percentage:.1f}%)")
        
        # Category breakdown
        if stats['categories']:
            print(f"\n📂 Category Breakdown:")
            for category, count in sorted(stats['categories'].items()):
                percentage = (count / stats['total'] * 100) if stats['total'] > 0 else 0
                print(f"   {category.capitalize()}: {count} ({percentage:.1f}%)")
        
        # Due date warnings
        due_stats = stats['due_stats']
        if any(due_stats.values()):
            print(f"\n⏰ Due Date Summary:")
            if due_stats['overdue'] > 0:
                print_warning(f"   Overdue tasks: {due_stats['overdue']}")
            if due_stats['due_today'] > 0:
                print_warning(f"   Due today: {due_stats['due_today']}")
            if due_stats['due_this_week'] > 0:
                print_info(f"   Due this week: {due_stats['due_this_week']}")
        
        # Weekly productivity
        weekly = stats['weekly_stats']
        print(f"\n📅 This Week's Activity:")
        print(f"   Created: {weekly['created_this_week']} tasks")
        print(f"   Completed: {weekly['completed_this_week']} tasks")
        
        productivity_trend = weekly['completed_this_week'] - weekly['created_this_week']
        if productivity_trend > 0:
            print_success(f"   You're ahead! +{productivity_trend} net tasks completed")
        elif productivity_trend < 0:
            print_warning(f"   You're behind by {abs(productivity_trend)} tasks")
        else:
            print_info("   You're keeping pace!")
        
        print()  # Empty line at the end
    
    def add_task(self, description: str, category: str = "general", 
                 priority: str = "medium", due_date: Optional[str] = None) -> None:
        """Add a new task with category, priority, and optional due date."""
        if not description.strip():
            print("Error: Task description cannot be empty.")
            return
        
        # Validate description length
        max_length = config.get("max_description_length")
        if len(description.strip()) > max_length:
            print(f"Error: Task description too long. Maximum {max_length} characters allowed.")
            return
        
        # Validate priority
        valid_priorities = config.get("valid_priorities")
        if priority not in valid_priorities:
            print(f"Error: Invalid priority '{priority}'. Valid priorities are: {', '.join(valid_priorities)}")
            return
        
        # Parse due date if provided
        parsed_due_date = None
        if due_date:
            try:
                parsed_due_date = datetime.strptime(due_date, "%Y-%m-%d").strftime("%Y-%m-%d")
            except ValueError:
                print("Error: Invalid due date format. Use YYYY-MM-DD format.")
                return
        
        current_time = self._get_current_timestamp()
        new_task = {
            "id": self.tasks["next_id"],
            "description": description.strip(),
            "status": config.get("default_status"),
            "category": category.lower(),
            "priority": priority,
            "due_date": parsed_due_date,
            "createdAt": current_time,
            "updatedAt": current_time
        }
        
        self.tasks["tasks"].append(new_task)
        self.tasks["next_id"] += 1
        self._save_tasks()
        
        print_success(f"Task added successfully (ID: {new_task['id']})")
        if category != "general":
            print_info(f"Category: {category}")
        if priority != "medium":
            print_info(f"Priority: {priority}")
        if due_date:
            print_info(f"Due date: {due_date}")
    
    def update_task(self, task_id: int, new_description: str, new_category: Optional[str] = None,
                   new_priority: Optional[str] = None, new_due_date: Optional[str] = None) -> None:
        """Update task with enhanced options."""
        if not new_description.strip():
            print_error("Task description cannot be empty.")
            return
        
        # Validate description length
        max_length = config.get("max_description_length")
        if len(new_description.strip()) > max_length:
            print_error(f"Task description too long. Maximum {max_length} characters allowed.")
            return
        
        task = self._find_task_by_id(task_id)
        if not task:
            print_error(f"Task with ID {task_id} not found.")
            return
        
        # Validate priority if provided
        if new_priority and new_priority not in config.get("valid_priorities"):
            print_error(f"Invalid priority '{new_priority}'. Valid priorities are: {', '.join(config.get('valid_priorities'))}")
            return
        
        # Parse due date if provided
        if new_due_date:
            try:
                new_due_date = datetime.strptime(new_due_date, "%Y-%m-%d").strftime("%Y-%m-%d")
            except ValueError:
                print_error("Invalid due date format. Use YYYY-MM-DD format.")
                return
        
        # Update task fields
        task["description"] = new_description.strip()
        if new_category is not None:
            task["category"] = new_category.lower()
        if new_priority is not None:
            task["priority"] = new_priority
        if new_due_date is not None:
            task["due_date"] = new_due_date
        
        task["updatedAt"] = self._get_current_timestamp()
        self._save_tasks()
        
        print_success(f"Task {task_id} updated successfully.")
    
    def delete_task(self, task_id: int) -> None:
        """Delete a task."""
        task = self._find_task_by_id(task_id)
        if not task:
            print_error(f"Task with ID {task_id} not found.")
            return
        
        self.tasks["tasks"] = [t for t in self.tasks["tasks"] if t["id"] != task_id]
        self._save_tasks()
        
        print_success(f"Task {task_id} deleted successfully.")
    
    def mark_in_progress(self, task_id: int) -> None:
        """Mark task as in progress."""
        task = self._find_task_by_id(task_id)
        if not task:
            print_error(f"Task with ID {task_id} not found.")
            return
        
        if task["status"] == "in-progress":
            print_warning(f"Task {task_id} is already in progress.")
            return
        
        task["status"] = "in-progress"
        task["updatedAt"] = self._get_current_timestamp()
        self._save_tasks()
        
        print_success(f"Task {task_id} marked as in progress.")
    
    def mark_done(self, task_id: int) -> None:
        """Mark task as done."""
        task = self._find_task_by_id(task_id)
        if not task:
            print_error(f"Task with ID {task_id} not found.")
            return
        
        if task["status"] == "done":
            print_warning(f"Task {task_id} is already done.")
            return
        
        task["status"] = "done"
        task["updatedAt"] = self._get_current_timestamp()
        self._save_tasks()
        
        print_success(f"Task {task_id} marked as done.")
    
    def list_tasks(self, status_filter: Optional[str] = None, category_filter: Optional[str] = None,
                  priority_filter: Optional[str] = None, search_query: Optional[str] = None,
                  sort_by: str = "id", reverse: bool = False, 
                  due_soon: bool = False) -> None:
        """List tasks with enhanced filtering and formatting."""
        valid_statuses = config.get("valid_statuses")
        
        if status_filter and status_filter not in valid_statuses:
            print_error(f"Invalid status '{status_filter}'. Valid statuses are: {', '.join(valid_statuses)}")
            return
        
        # Start with all tasks
        tasks_to_show = self.tasks["tasks"]
        
        # Apply search filter
        if search_query:
            tasks_to_show = [
                task for task in tasks_to_show 
                if search_query.lower() in task["description"].lower()
            ]
        
        # Apply filters
        tasks_to_show = self.filter_tasks(
            tasks_to_show, status_filter, category_filter, priority_filter, due_soon
        )
        
        # Sort tasks
        tasks_to_show = self.sort_tasks(tasks_to_show, sort_by, reverse)
        
        if not tasks_to_show:
            filter_desc = []
            if status_filter:
                filter_desc.append(f"status '{status_filter}'")
            if category_filter:
                filter_desc.append(f"category '{category_filter}'")
            if priority_filter:
                filter_desc.append(f"priority '{priority_filter}'")
            if search_query:
                filter_desc.append(f"search '{search_query}'")
            if due_soon:
                filter_desc.append("due soon")
            
            if filter_desc:
                print_info(f"No tasks found matching: {', '.join(filter_desc)}")
            else:
                print_info("No tasks found.")
            return
        
        # Print formatted table
        print("\n" + format_task_table(tasks_to_show))
        print(f"\nTotal: {len(tasks_to_show)} task(s)")
        
        # Show filter info if any filters were applied
        if any([status_filter, category_filter, priority_filter, search_query, due_soon]):
            filter_info = []
            if status_filter:
                filter_info.append(f"status: {status_filter}")
            if category_filter:
                filter_info.append(f"category: {category_filter}")
            if priority_filter:
                filter_info.append(f"priority: {priority_filter}")
            if search_query:
                filter_info.append(f"search: '{search_query}'")
            if due_soon:
                filter_info.append("due soon")
            
            print_info(f"Filtered by: {', '.join(filter_info)}")
    
    def filter_tasks(self, tasks: List[Dict[str, Any]], status: Optional[str] = None, 
                    category: Optional[str] = None, priority: Optional[str] = None, 
                    due_soon: bool = False) -> List[Dict[str, Any]]:
        """Apply filters to task list."""
        filtered_tasks = tasks
        
        if status:
            filtered_tasks = [t for t in filtered_tasks if t["status"] == status]
        
        if category:
            filtered_tasks = [t for t in filtered_tasks if t.get("category", "general") == category.lower()]
        
        if priority:
            filtered_tasks = [t for t in filtered_tasks if t.get("priority", "medium") == priority]
        
        if due_soon:
            today = datetime.now().date()
            week_from_now = today + timedelta(days=7)
            filtered_tasks = [
                t for t in filtered_tasks 
                if t.get("due_date") and datetime.strptime(t["due_date"], "%Y-%m-%d").date() <= week_from_now
            ]
        
        return filtered_tasks


def create_parser() -> argparse.ArgumentParser:
    """Create and configure argument parser."""
    parser = argparse.ArgumentParser(
        description="Task Tracker CLI - Enhanced task management tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s add "Buy groceries" --priority high --category shopping
  %(prog)s update 1 "New description" --priority low
  %(prog)s list --status todo --category work
  %(prog)s search "grocery"
  %(prog)s stats
  %(prog)s mark-done 1
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Add command
    add_parser = subparsers.add_parser('add', help='Add a new task')
    add_parser.add_argument('description', help='Task description')
    add_parser.add_argument('--category', '-c', default='general', help='Task category')
    add_parser.add_argument('--priority', '-p', choices=['low', 'medium', 'high'], 
                           default='medium', help='Task priority')
    add_parser.add_argument('--due', '-d', help='Due date (YYYY-MM-DD)')
    
    # Update command
    update_parser = subparsers.add_parser('update', help='Update an existing task')
    update_parser.add_argument('id', type=int, help='Task ID')
    update_parser.add_argument('description', help='New task description')
    update_parser.add_argument('--category', '-c', help='New task category')
    update_parser.add_argument('--priority', '-p', choices=['low', 'medium', 'high'], 
                              help='New task priority')
    update_parser.add_argument('--due', '-d', help='New due date (YYYY-MM-DD)')
    
    # Delete command
    delete_parser = subparsers.add_parser('delete', help='Delete a task')
    delete_parser.add_argument('id', type=int, help='Task ID')
    
    # Mark commands
    mark_progress_parser = subparsers.add_parser('mark-in-progress', help='Mark task as in progress')
    mark_progress_parser.add_argument('id', type=int, help='Task ID')
    
    mark_done_parser = subparsers.add_parser('mark-done', help='Mark task as done')
    mark_done_parser.add_argument('id', type=int, help='Task ID')
    
    # List command
    list_parser = subparsers.add_parser('list', help='List tasks')
    list_parser.add_argument('status', nargs='?', choices=['todo', 'in-progress', 'done'], 
                            help='Filter by status')
    list_parser.add_argument('--category', '-c', help='Filter by category')
    list_parser.add_argument('--priority', '-p', choices=['low', 'medium', 'high'], 
                            help='Filter by priority')
    list_parser.add_argument('--due-soon', action='store_true', 
                            help='Show tasks due within a week')
    list_parser.add_argument('--sort', choices=['id', 'description', 'status', 'priority', 
                                               'category', 'created', 'updated', 'due_date'],
                            default='id', help='Sort by field')
    list_parser.add_argument('--reverse', action='store_true', help='Reverse sort order')
    
    # Search command
    search_parser = subparsers.add_parser('search', help='Search tasks')
    search_parser.add_argument('query', help='Search query')
    search_parser.add_argument('--status', choices=['todo', 'in-progress', 'done'], 
                              help='Filter by status')
    search_parser.add_argument('--category', '-c', help='Filter by category')
    search_parser.add_argument('--priority', '-p', choices=['low', 'medium', 'high'], 
                              help='Filter by priority')
    
    # Statistics command
    stats_parser = subparsers.add_parser('stats', help='Show task statistics')
    
    # Global options
    parser.add_argument('--data-file', help='Custom data file path')
    parser.add_argument('--no-color', action='store_true', help='Disable colored output')
    parser.add_argument('--version', action='version', version='Task Tracker CLI 2.0')
    
    return parser


def main():
    """Main entry point with enhanced argument parsing."""
    parser = create_parser()
    args = parser.parse_args()
    
    # If no command provided, show help
    if not args.command:
        parser.print_help()
        return
    
    # Initialize task tracker
    tracker = TaskTracker(args.data_file)
    
    try:
        # Handle global options
        if args.no_color:
            global COLORS_AVAILABLE
            COLORS_AVAILABLE = False
        
        # Execute commands
        if args.command == 'add':
            tracker.add_task(args.description, args.category, args.priority, args.due)
        
        elif args.command == 'update':
            tracker.update_task(args.id, args.description, args.category, 
                              args.priority, args.due)
        
        elif args.command == 'delete':
            tracker.delete_task(args.id)
        
        elif args.command == 'mark-in-progress':
            tracker.mark_in_progress(args.id)
        
        elif args.command == 'mark-done':
            tracker.mark_done(args.id)
        
        elif args.command == 'list':
            tracker.list_tasks(
                status_filter=args.status,
                category_filter=args.category,
                priority_filter=args.priority,
                due_soon=args.due_soon,
                sort_by=args.sort,
                reverse=args.reverse
            )
        
        elif args.command == 'search':
            # Get search results
            search_results = tracker.search_tasks(args.query)
            
            # Apply additional filters
            if args.status or args.category or args.priority:
                search_results = tracker.filter_tasks(
                    search_results, args.status, args.category, args.priority
                )
            
            if not search_results:
                print_info(f"No tasks found matching '{args.query}'")
            else:
                print(f"\n{format_task_table(search_results)}")
                print(f"\nFound: {len(search_results)} task(s) matching '{args.query}'")
        
        elif args.command == 'stats':
            tracker.print_statistics()
    
    except KeyboardInterrupt:
        print_warning("\nOperation cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print_error(f"An unexpected error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
