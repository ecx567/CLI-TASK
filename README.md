# Task Tracker CLI

A simple and efficient command-line interface (CLI) application for managing your tasks and to-do lists. Built with Python following the requirements from roadmap.sh, this tool allows you to track what you need to do, what you have done, and what you are currently working on.

## 🚀 Features

- **Add Tasks**: Create new tasks with descriptions
- **Update Tasks**: Modify existing task descriptions  
- **Delete Tasks**: Remove tasks you no longer need
- **Mark Progress**: Change task status to "in-progress" or "done"
- **List Tasks**: View all tasks or filter by status (todo, in-progress, done)
- **Persistent Storage**: All tasks are saved to a JSON file
- **Error Handling**: Graceful handling of errors and edge cases
- **Unicode Support**: Full support for international characters

## 📋 Requirements

- Python 3.6 or higher
- No external dependencies (uses only Python standard library)

## 🔧 Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/ecx567/CLI-TASK.git
   cd CLI-TASK
   ```

2. Make the script executable (optional, for Unix-like systems):
   ```bash
   chmod +x task_cli.py
   ```

## 📖 Usage

The basic syntax is:
```bash
python task_cli.py <command> [arguments]
```

### Available Commands

#### 1. Add a new task
```bash
python task_cli.py add "Your task description"
```
**Example:**
```bash
python task_cli.py add "Buy groceries"
# Output: Task added successfully (ID: 1)
```

#### 2. Update an existing task
```bash
python task_cli.py update <task_id> "New description"
```
**Example:**
```bash
python task_cli.py update 1 "Buy groceries and cook dinner"
# Output: Task 1 updated successfully.
```

#### 3. Delete a task
```bash
python task_cli.py delete <task_id>
```
**Example:**
```bash
python task_cli.py delete 1
# Output: Task 1 deleted successfully.
```

#### 4. Mark task as in progress
```bash
python task_cli.py mark-in-progress <task_id>
```
**Example:**
```bash
python task_cli.py mark-in-progress 1
# Output: Task 1 marked as in progress.
```

#### 5. Mark task as done
```bash
python task_cli.py mark-done <task_id>
```
**Example:**
```bash
python task_cli.py mark-done 1
# Output: Task 1 marked as done.
```

#### 6. List all tasks
```bash
python task_cli.py list
```

#### 7. List tasks by status
```bash
python task_cli.py list <status>
```
Where `<status>` can be:
- `todo` - Tasks not yet started
- `in-progress` - Tasks currently being worked on  
- `done` - Completed tasks

**Examples:**
```bash
python task_cli.py list todo
python task_cli.py list in-progress
python task_cli.py list done
```

### 📝 Command Examples

Here's a complete workflow example:

```bash
# Add some tasks
python task_cli.py add "Buy groceries"
python task_cli.py add "Write project documentation"
python task_cli.py add "Review code changes"

# Update a task
python task_cli.py update 1 "Buy groceries and prepare dinner"

# Mark tasks with different statuses
python task_cli.py mark-in-progress 1
python task_cli.py mark-done 3

# List all tasks
python task_cli.py list

# List only completed tasks
python task_cli.py list done

# List only pending tasks  
python task_cli.py list todo

# Delete a task
python task_cli.py delete 2
```

### 📊 Sample Output

When you list tasks, you'll see output like this:

```
ID   Description                    Status       Created                     Updated                    
----------------------------------------------------------------------------------------------------
1    Buy groceries and prepare...   in-progress  2025-07-21 18:46:43.123456  2025-07-21 19:15:22.789012
2    Write project documentation    todo         2025-07-21 18:47:05.234567  2025-07-21 18:47:05.234567
3    Review code changes            done         2025-07-21 18:47:20.345678  2025-07-21 19:20:10.890123

Total: 3 task(s)
```

## 🏗️ Task Properties

Each task has the following properties:

- **id**: A unique identifier for the task (auto-generated)
- **description**: A short description of the task
- **status**: The current status (`todo`, `in-progress`, or `done`)
- **createdAt**: The date and time when the task was created
- **updatedAt**: The date and time when the task was last updated

## 💾 Data Storage

Tasks are stored in a JSON file called `tasks.json` in the same directory as the script. The file is created automatically when you add your first task.

Example of the JSON structure:
```json
{
  "tasks": [
    {
      "id": 1,
      "description": "Buy groceries",
      "status": "todo",
      "createdAt": "2025-07-21 18:46:43.123456",
      "updatedAt": "2025-07-21 18:46:43.123456"
    }
  ],
  "next_id": 2
}
```

## 🚨 Error Handling

The application handles various error scenarios gracefully:

- **Empty task descriptions**: Will not create tasks with empty or whitespace-only descriptions
- **Invalid task IDs**: Will show an error message if you try to operate on a non-existent task
- **Corrupted JSON file**: Will create a new clean file if the existing one is corrupted
- **File permission issues**: Will display appropriate error messages
- **Invalid status filters**: Will show valid status options

## 🧪 Testing

Run the comprehensive test suite to ensure everything works correctly:

```bash
python test_task_cli.py
```

The test suite includes:
- Unit tests for all core functionality
- Edge case testing (Unicode, long descriptions, whitespace)
- Data persistence testing
- Error condition testing
- Status transition testing

## 📁 Project Structure

```
CLI-TASK/
├── task_cli.py          # Main application file
├── test_task_cli.py     # Comprehensive test suite
├── README.md            # This documentation file
└── tasks.json           # Data file (created automatically)
```

## 🔧 Implementation Details

- **Language**: Python 3.6+
- **Storage**: JSON file in the current directory
- **Architecture**: Object-oriented design with a main `TaskTracker` class
- **Command-line parsing**: Uses positional arguments for simplicity
- **Date/time handling**: High-precision timestamps with microseconds
- **File operations**: Uses Python's `pathlib` and `json` modules
- **Type hints**: Full type annotation support

## 📝 Requirements Compliance

This implementation follows all the specified requirements:

✅ **Functional Requirements:**
- Add, Update, and Delete tasks
- Mark a task as in progress or done
- List all tasks
- List tasks that are done
- List tasks that are not done  
- List tasks that are in progress

✅ **Technical Constraints:**
- Uses positional arguments in command line
- Uses a JSON file to store tasks in current directory
- JSON file is created if it does not exist
- Uses native file system module (no external libraries)
- Handles errors and edge cases gracefully
- Can be built with any programming language (Python chosen)

## 🤝 Contributing

Feel free to contribute to this project by:
1. Reporting bugs
2. Suggesting new features
3. Submitting pull requests
4. Improving documentation

## 📄 License

This project is open source and available under the MIT License.

## 🎯 Project Goals

Created as part of a programming practice project to demonstrate:
- Command-line interface development
- File system operations and JSON data handling
- Error handling and edge cases
- Unit testing and code quality
- Clean code organization and documentation
- Git workflow and version control

---

**Happy task tracking! 🎯✨**

*Built with ❤️ following roadmap.sh project requirements*
