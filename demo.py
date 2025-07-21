#!/usr/bin/env python3
"""
Demo script for Task Tracker CLI

This script demonstrates all the functionality of the Task Tracker CLI
by running a series of commands that showcase each feature.
"""

import subprocess
import sys
import time
import os

def run_command(command, description):
    """Run a command and display the output with description."""
    print(f"\n{'='*60}")
    print(f"📝 {description}")
    print(f"{'='*60}")
    print(f"Command: {command}")
    print("-" * 60)
    
    # Run the command
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(f"Error: {result.stderr}")
    except Exception as e:
        print(f"Failed to run command: {e}")
    
    time.sleep(1)  # Brief pause for readability

def main():
    """Run the demo."""
    print("🚀 Task Tracker CLI Demo")
    print("This demo will showcase all features of the Task Tracker CLI")
    
    # Change to the script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    # Remove existing tasks.json if it exists
    if os.path.exists("tasks.json"):
        os.remove("tasks.json")
        print("\n🧹 Cleaned up existing tasks.json file")
    
    # Demo commands
    commands = [
        ("python task_cli.py", "Show help message"),
        ("python task_cli.py add \"Buy groceries\"", "Add first task"),
        ("python task_cli.py add \"Write project documentation\"", "Add second task"),
        ("python task_cli.py add \"Review code changes\"", "Add third task"),
        ("python task_cli.py add \"Deploy application\"", "Add fourth task"),
        ("python task_cli.py list", "List all tasks"),
        ("python task_cli.py update 1 \"Buy groceries and cook dinner\"", "Update task description"),
        ("python task_cli.py mark-in-progress 1", "Mark task as in progress"),
        ("python task_cli.py mark-in-progress 2", "Mark another task as in progress"),
        ("python task_cli.py mark-done 3", "Mark task as done"),
        ("python task_cli.py list", "List all tasks with updated statuses"),
        ("python task_cli.py list todo", "List only TODO tasks"),
        ("python task_cli.py list in-progress", "List only IN-PROGRESS tasks"),
        ("python task_cli.py list done", "List only DONE tasks"),
        ("python task_cli.py delete 4", "Delete a task"),
        ("python task_cli.py list", "List tasks after deletion"),
        ("python task_cli.py add \"Test Unicode: café, niño, corazón 💖\"", "Test Unicode support"),
        ("python task_cli.py list", "Show task with Unicode characters"),
    ]
    
    # Run each command
    for command, description in commands:
        run_command(command, description)
    
    # Error handling demonstrations
    print(f"\n{'='*60}")
    print("🚨 Error Handling Demonstrations")
    print(f"{'='*60}")
    
    error_commands = [
        ("python task_cli.py add \"\"", "Try to add empty task"),
        ("python task_cli.py update 999 \"Non-existent task\"", "Try to update non-existent task"),
        ("python task_cli.py delete 999", "Try to delete non-existent task"),
        ("python task_cli.py mark-done 999", "Try to mark non-existent task as done"),
        ("python task_cli.py list invalid-status", "Try to list with invalid status"),
        ("python task_cli.py unknown-command", "Try unknown command"),
    ]
    
    for command, description in error_commands:
        run_command(command, description)
    
    print(f"\n{'='*60}")
    print("✅ Demo completed!")
    print("📁 Check the tasks.json file to see the persistent storage format")
    print("🧪 Run 'python test_task_cli.py' to execute the test suite")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
