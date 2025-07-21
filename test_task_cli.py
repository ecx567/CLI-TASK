#!/usr/bin/env python3
"""
Test suite for Task Tracker CLI

This file contains unit tests for the TaskTracker class and its methods.
Tests cover all the core functionality including add, update, delete,
mark operations, and listing tasks.
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


class TestTaskTracker(unittest.TestCase):
    """Test cases for TaskTracker class."""
    
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
    
    def test_initial_state(self):
        """Test initial state of TaskTracker."""
        self.assertEqual(len(self.tracker.tasks["tasks"]), 0)
        self.assertEqual(self.tracker.tasks["next_id"], 1)
    
    def test_add_task(self):
        """Test adding a new task."""
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
        self.assertIn("Error: Task description cannot be empty.", output)
        
        with StringIO() as buf, redirect_stdout(buf):
            self.tracker.add_task("   ")
            output = buf.getvalue()
        
        self.assertEqual(len(self.tracker.tasks["tasks"]), initial_count)
        self.assertIn("Error: Task description cannot be empty.", output)
    
    def test_update_task(self):
        """Test updating a task."""
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
    
    def test_update_nonexistent_task(self):
        """Test updating a task that doesn't exist."""
        initial_count = len(self.tracker.tasks["tasks"])
        
        with StringIO() as buf, redirect_stdout(buf):
            self.tracker.update_task(999, "Updated task")
            output = buf.getvalue()
        
        self.assertEqual(len(self.tracker.tasks["tasks"]), initial_count)
        self.assertIn("Error: Task with ID 999 not found.", output)
    
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
        self.assertIn("Error: Task with ID 999 not found.", output)
    
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
        
        self.assertIn("Error: Task with ID 999 not found.", output1)
        self.assertIn("Error: Task with ID 999 not found.", output2)
    
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
            self.tracker.list_tasks("todo")
            output = buf.getvalue()
        
        self.assertIn("Todo task", output)
        self.assertNotIn("Progress task", output)
        self.assertNotIn("Done task", output)
        self.assertIn("Total: 1 task(s)", output)
        
        # Test filtering by done
        with StringIO() as buf, redirect_stdout(buf):
            self.tracker.list_tasks("done")
            output = buf.getvalue()
        
        self.assertNotIn("Todo task", output)
        self.assertNotIn("Progress task", output)
        self.assertIn("Done task", output)
        self.assertIn("Total: 1 task(s)", output)
    
    def test_list_tasks_invalid_filter(self):
        """Test listing tasks with invalid filter."""
        with StringIO() as buf, redirect_stdout(buf):
            self.tracker.list_tasks("invalid")
            output = buf.getvalue()
        
        self.assertIn("Error: Invalid status 'invalid'", output)
    
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
        long_description = "A" * 1000
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
    print("Running Task Tracker CLI Tests...")
    print("=" * 50)
    unittest.main(verbosity=2)
