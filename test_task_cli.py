#!/usr/bin/env python3
"""
Enhanced Test suite for Task Tracker CLI v2.0

This file contains unit tests for the enhanced TaskTracker class and its methods.
Tests cover all the core functionality including add, update, delete,
mark operations, listing tasks, categories, priorities, search, and statistics.
Includes backward compatibility tests for original functionality.
"""

import unittest
import json
import tempfile
import os
import sys
from pathlib import Path
from io import StringIO
from contextlib import redirect_stdout, redirect_stderr

# Add the current directory to Python path to import our module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from task_cli import TaskTracker
from config import config


class TestTaskTracker(unittest.TestCase):
    """Test cases for enhanced TaskTracker class."""
    
    def setUp(self):
        """Set up test environment before each test."""
        # Create a temporary file for testing
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json')
        self.temp_file.close()
        self.tracker = TaskTracker(self.temp_file.name)
    
    def tearDown(self):
        """Clean up after each test."""
        # Remove temporary file
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)
        # Clean up backup directory if created
        backup_dir = Path("backups")
        if backup_dir.exists():
            for backup_file in backup_dir.glob("*.json"):
                backup_file.unlink()
            try:
                backup_dir.rmdir()
            except OSError:
                pass
    
    def test_initial_state(self):
        """Test initial state of enhanced TaskTracker."""
        self.assertEqual(len(self.tracker.tasks["tasks"]), 0)
        self.assertEqual(self.tracker.tasks["next_id"], 1)
        self.assertIn("metadata", self.tracker.tasks)
        self.assertIn("version", self.tracker.tasks["metadata"])
    
    def test_add_task(self):
        """Test adding a new task with backward compatibility."""
        # Capture output
        with StringIO() as buf, redirect_stdout(buf):
            self.tracker.add_task("Test task")
            output = buf.getvalue()
        
        # Check if task was added
        self.assertEqual(len(self.tracker.tasks["tasks"]), 1)
        task = self.tracker.tasks["tasks"][0]
        self.assertEqual(task["id"], 1)
        self.assertEqual(task["description"], "Test task")
        self.assertEqual(task["status"], "todo")
        self.assertEqual(task["category"], "general")  # Default category
        self.assertEqual(task["priority"], "medium")   # Default priority
        self.assertIsNotNone(task["createdAt"])
        self.assertIsNotNone(task["updatedAt"])
        self.assertEqual(self.tracker.tasks["next_id"], 2)
        self.assertIn("Task added successfully (ID: 1)", output)
    
    def test_add_task_enhanced(self):
        """Test adding a new task with enhanced features."""
        # Capture output
        with StringIO() as buf, redirect_stdout(buf):
            self.tracker.add_task("Test task", "work", "high", "2025-07-30")
            output = buf.getvalue()
        
        # Check if task was added
        self.assertEqual(len(self.tracker.tasks["tasks"]), 1)
        task = self.tracker.tasks["tasks"][0]
        self.assertEqual(task["id"], 1)
        self.assertEqual(task["description"], "Test task")
        self.assertEqual(task["status"], "todo")
        self.assertEqual(task["category"], "work")
        self.assertEqual(task["priority"], "high")
        self.assertEqual(task["due_date"], "2025-07-30")
        self.assertIsNotNone(task["createdAt"])
        self.assertIsNotNone(task["updatedAt"])
        self.assertEqual(self.tracker.tasks["next_id"], 2)
        self.assertIn("Task added successfully (ID: 1)", output)
    
    def test_add_empty_task(self):
        """Test adding an empty task (should not be added)."""
        initial_count = len(self.tracker.tasks["tasks"])
        
        with StringIO() as buf, redirect_stdout(buf):
            self.tracker.add_task("")
            output = buf.getvalue()
        
        self.assertEqual(len(self.tracker.tasks["tasks"]), initial_count)
        self.assertIn("Task description cannot be empty.", output)
        
        with StringIO() as buf, redirect_stdout(buf):
            self.tracker.add_task("   ")
            output = buf.getvalue()
        
        self.assertEqual(len(self.tracker.tasks["tasks"]), initial_count)
        self.assertIn("Task description cannot be empty.", output)
    
    def test_add_task_validation(self):
        """Test task validation for enhanced features."""
        initial_count = len(self.tracker.tasks["tasks"])
        
        # Test invalid priority
        with StringIO() as buf, redirect_stdout(buf):
            self.tracker.add_task("Test", "general", "invalid")
            output = buf.getvalue()
        self.assertEqual(len(self.tracker.tasks["tasks"]), initial_count)
        self.assertIn("Invalid priority", output)
        
        # Test invalid due date
        with StringIO() as buf, redirect_stdout(buf):
            self.tracker.add_task("Test", "general", "medium", "invalid-date")
            output = buf.getvalue()
        self.assertEqual(len(self.tracker.tasks["tasks"]), initial_count)
        self.assertIn("Invalid due date format", output)
    
    def test_update_task(self):
        """Test updating a task with backward compatibility."""
        # Add a task first
        self.tracker.add_task("Original task")
        original_created_at = self.tracker.tasks["tasks"][0]["createdAt"]
        
        # Update the task
        with StringIO() as buf, redirect_stdout(buf):
            self.tracker.update_task(1, "Updated task")
            output = buf.getvalue()
        
        # Check if task was updated
        task = self.tracker.tasks["tasks"][0]
        self.assertEqual(task["description"], "Updated task")
        self.assertEqual(task["createdAt"], original_created_at)  # Should not change
        self.assertNotEqual(task["updatedAt"], original_created_at)  # Should change
        self.assertIn("Task 1 updated successfully.", output)
    
    def test_update_task_enhanced(self):
        """Test updating a task with enhanced features."""
        # Add a task first
        self.tracker.add_task("Original task", "work", "medium")
        
        # Update with enhanced options
        with StringIO() as buf, redirect_stdout(buf):
            self.tracker.update_task(1, "Updated task", "personal", "high", "2025-08-01")
            output = buf.getvalue()
        
        # Check if task was updated
        task = self.tracker.tasks["tasks"][0]
        self.assertEqual(task["description"], "Updated task")
        self.assertEqual(task["category"], "personal")
        self.assertEqual(task["priority"], "high")
        self.assertEqual(task["due_date"], "2025-08-01")
        self.assertIn("Task 1 updated successfully.", output)
    
    def test_update_nonexistent_task(self):
        """Test updating a task that doesn't exist."""
        initial_count = len(self.tracker.tasks["tasks"])
        
        with StringIO() as buf, redirect_stdout(buf):
            self.tracker.update_task(999, "Updated task")
            output = buf.getvalue()
        
        self.assertEqual(len(self.tracker.tasks["tasks"]), initial_count)
        self.assertIn("Task with ID 999 not found.", output)
    
    def test_delete_task(self):
        """Test deleting a task."""
        # Add tasks
        self.tracker.add_task("Task 1")
        self.tracker.add_task("Task 2")
        self.assertEqual(len(self.tracker.tasks["tasks"]), 2)
        
        # Delete first task
        with StringIO() as buf, redirect_stdout(buf):
            self.tracker.delete_task(1)
            output = buf.getvalue()
        
        self.assertEqual(len(self.tracker.tasks["tasks"]), 1)
        self.assertEqual(self.tracker.tasks["tasks"][0]["id"], 2)
        self.assertIn("Task 1 deleted successfully.", output)
    
    def test_delete_nonexistent_task(self):
        """Test deleting a task that doesn't exist."""
        initial_count = len(self.tracker.tasks["tasks"])
        
        with StringIO() as buf, redirect_stdout(buf):
            self.tracker.delete_task(999)
            output = buf.getvalue()
        
        self.assertEqual(len(self.tracker.tasks["tasks"]), initial_count)
        self.assertIn("Task with ID 999 not found.", output)
    
    def test_mark_in_progress(self):
        """Test marking a task as in progress."""
        # Add a task
        self.tracker.add_task("Test task")
        original_updated_at = self.tracker.tasks["tasks"][0]["updatedAt"]
        
        # Mark as in progress
        with StringIO() as buf, redirect_stdout(buf):
            self.tracker.mark_in_progress(1)
            output = buf.getvalue()
        
        # Check status
        task = self.tracker.tasks["tasks"][0]
        self.assertEqual(task["status"], "in-progress")
        self.assertNotEqual(task["updatedAt"], original_updated_at)
        self.assertIn("Task 1 marked as in progress.", output)
    
    def test_mark_done(self):
        """Test marking a task as done."""
        # Add a task
        self.tracker.add_task("Test task")
        original_updated_at = self.tracker.tasks["tasks"][0]["updatedAt"]
        
        # Mark as done
        with StringIO() as buf, redirect_stdout(buf):
            self.tracker.mark_done(1)
            output = buf.getvalue()
        
        # Check status
        task = self.tracker.tasks["tasks"][0]
        self.assertEqual(task["status"], "done")
        self.assertNotEqual(task["updatedAt"], original_updated_at)
        self.assertIn("Task 1 marked as done.", output)
    
    def test_mark_nonexistent_task(self):
        """Test marking a non-existent task."""
        with StringIO() as buf, redirect_stdout(buf):
            self.tracker.mark_in_progress(999)
            output1 = buf.getvalue()
        
        with StringIO() as buf, redirect_stdout(buf):
            self.tracker.mark_done(999)
            output2 = buf.getvalue()
        
        self.assertIn("Task with ID 999 not found.", output1)
        self.assertIn("Task with ID 999 not found.", output2)
    
    def test_list_tasks_empty(self):
        """Test listing tasks when no tasks exist."""
        with StringIO() as buf, redirect_stdout(buf):
            self.tracker.list_tasks()
            output = buf.getvalue()
        
        self.assertIn("No tasks found.", output)
    
    def test_list_tasks_with_data(self):
        """Test listing tasks with data."""
        # Add some tasks
        self.tracker.add_task("Task 1")
        self.tracker.add_task("Task 2")
        self.tracker.mark_in_progress(1)
        self.tracker.mark_done(2)
        
        with StringIO() as buf, redirect_stdout(buf):
            self.tracker.list_tasks()
            output = buf.getvalue()
        
        self.assertIn("Task 1", output)
        self.assertIn("Task 2", output)
        self.assertIn("in-progress", output)
        self.assertIn("done", output)
        self.assertIn("Total: 2 task(s)", output)
    
    def test_list_tasks_with_filter(self):
        """Test listing tasks with status filter."""
        # Add tasks with different statuses
        self.tracker.add_task("Todo task")
        self.tracker.add_task("Progress task")
        self.tracker.add_task("Done task")
        
        self.tracker.mark_in_progress(2)
        self.tracker.mark_done(3)
        
        # Test filtering by todo
        with StringIO() as buf, redirect_stdout(buf):
            self.tracker.list_tasks(status_filter="todo")
            output = buf.getvalue()
        
        self.assertIn("Todo task", output)
        self.assertNotIn("Progress task", output)
        self.assertNotIn("Done task", output)
        self.assertIn("Total: 1 task(s)", output)
        
        # Test filtering by done
        with StringIO() as buf, redirect_stdout(buf):
            self.tracker.list_tasks(status_filter="done")
            output = buf.getvalue()
        
        self.assertNotIn("Todo task", output)
        self.assertNotIn("Progress task", output)
        self.assertIn("Done task", output)
        self.assertIn("Total: 1 task(s)", output)
    
    def test_list_tasks_enhanced(self):
        """Test enhanced list functionality."""
        # Add test tasks
        self.tracker.add_task("Work task", "work", "high")
        self.tracker.add_task("Personal task", "personal", "low")
        self.tracker.mark_done(1)
        
        # Test listing with filters
        with StringIO() as buf, redirect_stdout(buf):
            self.tracker.list_tasks(category_filter="work")
            output = buf.getvalue()
        
        self.assertIn("Work task", output)
        self.assertNotIn("Personal task", output)
    
    def test_list_tasks_invalid_filter(self):
        """Test listing tasks with invalid filter."""
        with StringIO() as buf, redirect_stdout(buf):
            self.tracker.list_tasks(status_filter="invalid")
            output = buf.getvalue()
        
        self.assertIn("Invalid status 'invalid'", output)
    
    def test_search_tasks(self):
        """Test task search functionality."""
        # Add test tasks
        self.tracker.add_task("Buy groceries", "shopping", "high")
        self.tracker.add_task("Write documentation", "work", "medium")
        self.tracker.add_task("Review grocery list", "shopping", "low")
        
        # Search for "grocer" - should find both "Buy groceries" and "Review grocery list" 
        # because both contain "grocer" (from "groceries" and "grocery")
        results = self.tracker.search_tasks("grocer")
        self.assertEqual(len(results), 2)
        
        # Search for "documentation"
        results = self.tracker.search_tasks("documentation")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["description"], "Write documentation")
    
    def test_filter_tasks(self):
        """Test task filtering functionality."""
        # Add test tasks with different attributes
        self.tracker.add_task("Task 1", "work", "high")
        self.tracker.add_task("Task 2", "work", "low")
        self.tracker.add_task("Task 3", "personal", "high")
        
        # Filter by category
        filtered = self.tracker.filter_tasks(self.tracker.tasks["tasks"], category="work")
        self.assertEqual(len(filtered), 2)
        
        # Filter by priority
        filtered = self.tracker.filter_tasks(self.tracker.tasks["tasks"], priority="high")
        self.assertEqual(len(filtered), 2)
        
        # Filter by both category and priority
        filtered = self.tracker.filter_tasks(self.tracker.tasks["tasks"], category="work", priority="high")
        self.assertEqual(len(filtered), 1)
    
    def test_sort_tasks(self):
        """Test task sorting functionality."""
        # Add test tasks
        self.tracker.add_task("Z task", "work", "low")
        self.tracker.add_task("A task", "personal", "high")
        
        tasks = self.tracker.tasks["tasks"]
        
        # Sort by description
        sorted_tasks = self.tracker.sort_tasks(tasks, "description")
        self.assertEqual(sorted_tasks[0]["description"], "A task")
        self.assertEqual(sorted_tasks[1]["description"], "Z task")
        
        # Sort by priority (reverse) - priority index: low=0, medium=1, high=2
        # So reverse=True should put high (index 2) first, then low (index 0)
        sorted_tasks = self.tracker.sort_tasks(tasks, "priority", reverse=True)
        self.assertEqual(sorted_tasks[0]["priority"], "high")  # A task
        self.assertEqual(sorted_tasks[1]["priority"], "low")   # Z task
    
    def test_statistics(self):
        """Test statistics functionality."""
        # Add test tasks with different statuses and priorities
        self.tracker.add_task("Task 1", "work", "high")
        self.tracker.add_task("Task 2", "work", "medium")
        self.tracker.add_task("Task 3", "personal", "low")
        
        # Mark some tasks as done
        self.tracker.mark_done(1)
        self.tracker.mark_in_progress(2)
        
        stats = self.tracker.get_statistics()
        
        self.assertEqual(stats["total"], 3)
        self.assertEqual(stats["status_counts"]["done"], 1)
        self.assertEqual(stats["status_counts"]["in-progress"], 1)
        self.assertEqual(stats["status_counts"]["todo"], 1)
        self.assertAlmostEqual(stats["completion_rate"], 33.3, places=1)
        
        # Test category breakdown
        self.assertEqual(stats["categories"]["work"], 2)
        self.assertEqual(stats["categories"]["personal"], 1)
        
        # Test priority breakdown
        self.assertEqual(stats["priority_counts"]["high"], 1)
        self.assertEqual(stats["priority_counts"]["medium"], 1)
        self.assertEqual(stats["priority_counts"]["low"], 1)
    
    def test_find_task_by_id(self):
        """Test finding task by ID."""
        # Add tasks
        self.tracker.add_task("Task 1")
        self.tracker.add_task("Task 2")
        
        # Find existing task
        task = self.tracker._find_task_by_id(1)
        self.assertIsNotNone(task)
        self.assertEqual(task["description"], "Task 1")
        
        # Find non-existent task
        task = self.tracker._find_task_by_id(999)
        self.assertIsNone(task)
    
    def test_task_persistence(self):
        """Test that tasks are persisted to file."""
        # Add a task
        self.tracker.add_task("Persistent task")
        
        # Create new tracker instance with same file
        new_tracker = TaskTracker(self.temp_file.name)
        
        # Check if task is loaded
        self.assertEqual(len(new_tracker.tasks["tasks"]), 1)
        self.assertEqual(new_tracker.tasks["tasks"][0]["description"], "Persistent task")
        self.assertEqual(new_tracker.tasks["next_id"], 2)
    
    def test_multiple_tasks_workflow(self):
        """Test a complete workflow with multiple tasks."""
        # Add multiple tasks
        self.tracker.add_task("Task 1")
        self.tracker.add_task("Task 2")
        self.tracker.add_task("Task 3")
        
        # Update a task
        self.tracker.update_task(2, "Updated Task 2")
        
        # Mark tasks with different statuses
        self.tracker.mark_in_progress(1)
        self.tracker.mark_done(3)
        
        # Verify final state
        tasks = self.tracker.tasks["tasks"]
        self.assertEqual(len(tasks), 3)
        
        # Task 1 should be in progress
        task1 = self.tracker._find_task_by_id(1)
        self.assertEqual(task1["status"], "in-progress")
        
        # Task 2 should be updated and todo
        task2 = self.tracker._find_task_by_id(2)
        self.assertEqual(task2["description"], "Updated Task 2")
        self.assertEqual(task2["status"], "todo")
        
        # Task 3 should be done
        task3 = self.tracker._find_task_by_id(3)
        self.assertEqual(task3["status"], "done")
    
    def test_invalid_json_file(self):
        """Test handling of invalid JSON file."""
        # Write invalid JSON to file
        with open(self.temp_file.name, 'w') as f:
            f.write("invalid json content")
        
        # Should handle gracefully and create new structure
        with StringIO() as buf, redirect_stdout(buf):
            tracker = TaskTracker(self.temp_file.name)
            output = buf.getvalue()
        
        self.assertEqual(len(tracker.tasks["tasks"]), 0)
        self.assertEqual(tracker.tasks["next_id"], 1)
        self.assertIn("Error loading tasks file", output)
    
    def test_migration_old_format(self):
        """Test migration from old task format."""
        # Create old format data
        old_data = {
            "tasks": [
                {
                    "id": 1,
                    "description": "Old task",
                    "status": "todo",
                    "createdAt": "2025-07-22 10:00:00.000000",
                    "updatedAt": "2025-07-22 10:00:00.000000"
                }
            ],
            "next_id": 2
        }
        
        # Write old format to file
        with open(self.temp_file.name, 'w') as f:
            json.dump(old_data, f)
        
        # Load with new tracker
        tracker = TaskTracker(self.temp_file.name)
        
        # Check migration
        task = tracker.tasks["tasks"][0]
        self.assertEqual(task["category"], "general")
        self.assertEqual(task["priority"], "medium")
        self.assertIsNone(task["due_date"])
        self.assertIn("metadata", tracker.tasks)


class TestTaskTrackerEdgeCases(unittest.TestCase):
    """Test edge cases and error conditions."""
    
    def setUp(self):
        """Set up test environment."""
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json')
        self.temp_file.close()
        self.tracker = TaskTracker(self.temp_file.name)
    
    def tearDown(self):
        """Clean up after each test."""
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)
    
    def test_whitespace_trimming(self):
        """Test that whitespace is properly trimmed."""
        self.tracker.add_task("  Task with spaces  ")
        task = self.tracker.tasks["tasks"][0]
        self.assertEqual(task["description"], "Task with spaces")
        
        self.tracker.update_task(1, "  Updated task  ")
        task = self.tracker.tasks["tasks"][0]
        self.assertEqual(task["description"], "Updated task")
    
    def test_unicode_characters(self):
        """Test handling of Unicode characters."""
        unicode_task = "Tarea con acentos: café, niño, corazón 💖"
        self.tracker.add_task(unicode_task)
        task = self.tracker.tasks["tasks"][0]
        self.assertEqual(task["description"], unicode_task)
    
    def test_very_long_description(self):
        """Test handling of very long task descriptions."""
        long_description = "A" * 500  # Within limit
        self.tracker.add_task(long_description)
        task = self.tracker.tasks["tasks"][0]
        self.assertEqual(task["description"], long_description)
    
    def test_status_transitions(self):
        """Test marking tasks that are already in the target status."""
        self.tracker.add_task("Test task")
        
        # Mark as in-progress twice
        self.tracker.mark_in_progress(1)
        with StringIO() as buf, redirect_stdout(buf):
            self.tracker.mark_in_progress(1)
            output = buf.getvalue()
        self.assertIn("Task 1 is already in progress.", output)
        
        # Mark as done twice
        self.tracker.mark_done(1)
        with StringIO() as buf, redirect_stdout(buf):
            self.tracker.mark_done(1)
            output = buf.getvalue()
        self.assertIn("Task 1 is already done.", output)


if __name__ == "__main__":
    # Run all tests
    print("Running Enhanced Task Tracker CLI Tests...")
    print("=" * 60)
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test cases
    suite.addTests(loader.loadTestsFromTestCase(TestTaskTracker))
    suite.addTests(loader.loadTestsFromTestCase(TestTaskTrackerEdgeCases))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "=" * 60)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.wasSuccessful():
        print("🎉 All tests passed!")
    else:
        print("❌ Some tests failed!")
        sys.exit(1)
