#!/usr/bin/env python3
"""
Enhanced Demo script for Task Tracker CLI v2.0

This script demonstrates all the enhanced functionality of the Task Tracker CLI
including new features like categories, priorities, due dates, search, and statistics.
"""

import subprocess
import sys
import time
import os

def run_command(command, description):
    """Run a command and display the output with description."""
    print(f"\n{'='*70}")
    print(f"📝 {description}")
    print(f"{'='*70}")
    print(f"Command: {command}")
    print("-" * 70)
    
    # Run the command
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(f"Error: {result.stderr}")
    except Exception as e:
        print(f"Failed to run command: {e}")
    
    time.sleep(1.5)  # Brief pause for readability

def main():
    """Run the enhanced demo."""
    print("🚀 Task Tracker CLI v2.0 - Enhanced Demo")
    print("=" * 50)
    print("This demo showcases all the new enhanced features:")
    print("• Categories and Priorities")
    print("• Due dates")
    print("• Enhanced search and filtering")
    print("• Beautiful table formatting")
    print("• Statistics and reports")
    print("• Improved argument parsing")
    
    # Change to the script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    # Remove existing tasks.json if it exists
    if os.path.exists("tasks.json"):
        os.remove("tasks.json")
        print("\n🧹 Cleaned up existing tasks.json file")
    
    # Basic functionality demo
    basic_commands = [
        ("python task_cli.py --help", "Show enhanced help message"),
        ("python task_cli.py add \"Buy groceries\" --category shopping --priority high", "Add high-priority shopping task"),
        ("python task_cli.py add \"Write project documentation\" --category work --priority medium --due 2025-07-30", "Add work task with due date"),
        ("python task_cli.py add \"Review code changes\" --category work --priority high", "Add another work task"),
        ("python task_cli.py add \"Plan vacation\" --category personal --priority low --due 2025-08-15", "Add personal task"),
        ("python task_cli.py add \"Fix bug in authentication\" --category work --priority high --due 2025-07-25", "Add urgent work task"),
    ]
    
    print(f"\n{'🎯 BASIC FUNCTIONALITY DEMO':=^70}")
    for command, description in basic_commands:
        run_command(command, description)
    
    # Enhanced listing and filtering demo
    listing_commands = [
        ("python task_cli.py list", "List all tasks with enhanced formatting"),
        ("python task_cli.py list --category work", "Filter tasks by work category"),
        ("python task_cli.py list --priority high", "Filter tasks by high priority"),
        ("python task_cli.py list --status todo --sort priority --reverse", "List TODO tasks sorted by priority (high to low)"),
        ("python task_cli.py list --due-soon", "Show tasks due within a week"),
    ]
    
    print(f"\n{'📋 ENHANCED LISTING & FILTERING':=^70}")
    for command, description in listing_commands:
        run_command(command, description)
    
    # Task management demo
    management_commands = [
        ("python task_cli.py mark-in-progress 1", "Mark shopping task as in progress"),
        ("python task_cli.py mark-in-progress 3", "Mark code review as in progress"), 
        ("python task_cli.py mark-done 2", "Mark documentation task as done"),
        ("python task_cli.py update 4 \"Plan summer vacation to Europe\" --priority medium", "Update vacation task"),
    ]
    
    print(f"\n{'⚙️ TASK MANAGEMENT DEMO':=^70}")
    for command, description in management_commands:
        run_command(command, description)
    
    # Search functionality demo
    search_commands = [
        ("python task_cli.py search \"vacation\"", "Search for vacation-related tasks"),
        ("python task_cli.py search \"bug\" --status todo", "Search for bugs in TODO tasks"),
        ("python task_cli.py search \"work\" --category work --priority high", "Search work tasks with high priority"),
    ]
    
    print(f"\n{'🔍 SEARCH FUNCTIONALITY DEMO':=^70}")
    for command, description in search_commands:
        run_command(command, description)
    
    # Statistics demo
    stats_commands = [
        ("python task_cli.py stats", "Show comprehensive statistics report"),
        ("python task_cli.py list --sort due_date", "List tasks sorted by due date"),
        ("python task_cli.py list --status in-progress", "Show current work in progress"),
    ]
    
    print(f"\n{'📊 STATISTICS & REPORTING DEMO':=^70}")
    for command, description in stats_commands:
        run_command(command, description)
    
    # Error handling demonstrations
    print(f"\n{'🚨 ERROR HANDLING DEMONSTRATIONS':=^70}")
    
    error_commands = [
        ("python task_cli.py add \"\"", "Try to add empty task"),
        ("python task_cli.py add \"Test\" --priority invalid", "Try invalid priority"),
        ("python task_cli.py add \"Test\" --due invalid-date", "Try invalid due date"),
        ("python task_cli.py update 999 \"Non-existent task\"", "Try to update non-existent task"),
        ("python task_cli.py delete 999", "Try to delete non-existent task"),
        ("python task_cli.py list --status invalid", "Try invalid status filter"),
        ("python task_cli.py search \"nonexistent\"", "Search for non-existent content"),
    ]
    
    for command, description in error_commands:
        run_command(command, description)
    
    # Advanced features demo
    print(f"\n{'🔧 ADVANCED FEATURES DEMO':=^70}")
    
    advanced_commands = [
        ("python task_cli.py add \"Test very long task description that exceeds normal limits to demonstrate text truncation in the table display functionality\" --category testing", "Test long description handling"),
        ("python task_cli.py add \"Test Unicode: café, niño, corazón 💖\" --category testing --priority medium", "Test Unicode support"),
        ("python task_cli.py list --sort description", "Sort tasks alphabetically by description"),
        ("python task_cli.py list --no-color", "List tasks without colors"),
    ]
    
    for command, description in advanced_commands:
        run_command(command, description)
    
    # Final statistics
    run_command("python task_cli.py stats", "Final comprehensive statistics")
    
    print(f"\n{'='*70}")
    print("✅ Enhanced Demo completed!")
    print("🎉 New features demonstrated:")
    print("   • Categories and priorities")
    print("   • Due dates and urgency indicators")
    print("   • Advanced search and filtering")
    print("   • Beautiful table formatting")
    print("   • Comprehensive statistics")
    print("   • Enhanced argument parsing")
    print("   • Improved error messages")
    print("   • Unicode support")
    print("   • Sorting and reverse sorting")
    print("   • Backup system (automatic)")
    print()
    print("📁 Files created:")
    print("   • tasks.json - Main data file")
    print("   • backups/ - Automatic backup directory")
    print("   • config.json - Configuration file (if customized)")
    print()
    print("🧪 Next steps:")
    print("   • Run 'python test_task_cli.py' to execute the test suite")
    print("   • Try 'python task_cli.py --help' for full command reference")
    print("   • Explore filtering combinations and sorting options")
    print(f"{'='*70}")

if __name__ == "__main__":
    main()
