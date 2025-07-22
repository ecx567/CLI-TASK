# Task Tracker CLI v2.0 - Enhanced Edition

A sophisticated and feature-rich command-line interface (CLI) application for managing your tasks and to-do lists. Built with Python following roadmap.sh requirements and enhanced with modern productivity features. This tool helps you track what you need to do, what you have done, and what you are currently working on with powerful organization and visualization capabilities.

## 🚀 Enhanced Features

### Core Functionality
- **Add Tasks**: Create new tasks with descriptions, categories, priorities, and due dates
- **Update Tasks**: Modify existing task descriptions and attributes
- **Delete Tasks**: Remove tasks you no longer need
- **Mark Progress**: Change task status to "in-progress" or "done"
- **List Tasks**: View all tasks or filter by multiple criteria
- **Persistent Storage**: All tasks are saved to JSON with automatic backups

### New Enhanced Features ⭐
- **Categories**: Organize tasks by categories (work, personal, shopping, etc.)
- **Priorities**: Set task priorities (high, medium, low) with visual indicators
- **Due Dates**: Set and track due dates with urgency warnings
- **Advanced Search**: Search tasks by content with powerful filtering
- **Beautiful Tables**: Enhanced table formatting with colors and proper alignment
- **Statistics & Reports**: Comprehensive productivity analytics and insights
- **Smart Filtering**: Filter by status, category, priority, due dates, and more
- **Flexible Sorting**: Sort tasks by any field in ascending or descending order
- **Backup System**: Automatic backup creation with configurable retention
- **Configuration**: Customizable settings via config file or environment variables
- **Enhanced CLI**: Modern argument parsing with help and validation
- **Unicode Support**: Full support for international characters and emojis
- **Error Handling**: Graceful handling of errors with helpful messages

## 📋 Requirements

- Python 3.6 or higher
- colorama (for enhanced colors)
- tabulate (for beautiful table formatting)

## 🔧 Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/ecx567/CLI-TASK.git
   cd CLI-TASK
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Make the script executable (optional, for Unix-like systems):
   ```bash
   chmod +x task_cli.py
   ```

## 📖 Usage

The enhanced CLI uses modern argument parsing with subcommands:

```bash
python task_cli.py <command> [arguments] [options]
```

### Available Commands

#### 1. Add a new task (Enhanced)
```bash
python task_cli.py add "Task description" [options]
```

**Options:**
- `--category, -c`: Task category (default: general)
- `--priority, -p`: Priority level (low, medium, high)
- `--due, -d`: Due date in YYYY-MM-DD format

**Examples:**
```bash
python task_cli.py add "Buy groceries" --category shopping --priority high
python task_cli.py add "Finish project" --category work --priority medium --due 2025-07-30
python task_cli.py add "Call mom" --priority high --due 2025-07-23
```

#### 2. Update an existing task (Enhanced)
```bash
python task_cli.py update <task_id> "New description" [options]
```

**Options:**
- `--category, -c`: New category
- `--priority, -p`: New priority
- `--due, -d`: New due date

**Examples:**
```bash
python task_cli.py update 1 "Buy groceries and cook dinner"
python task_cli.py update 2 "Complete quarterly report" --priority high --due 2025-07-25
```

#### 3. Delete a task
```bash
python task_cli.py delete <task_id>
```

#### 4. Mark task status
```bash
python task_cli.py mark-in-progress <task_id>
python task_cli.py mark-done <task_id>
```

#### 5. List tasks (Enhanced)
```bash
python task_cli.py list [status] [options]
```

**Options:**
- `--category, -c`: Filter by category
- `--priority, -p`: Filter by priority
- `--due-soon`: Show tasks due within a week
- `--sort`: Sort by field (id, description, status, priority, category, created, updated, due_date)
- `--reverse`: Reverse sort order

**Examples:**
```bash
python task_cli.py list                                    # All tasks
python task_cli.py list todo                              # Only TODO tasks
python task_cli.py list --category work                   # Work tasks only
python task_cli.py list --priority high                   # High priority tasks
python task_cli.py list --due-soon                        # Tasks due soon
python task_cli.py list --sort priority --reverse         # Sort by priority (high to low)
python task_cli.py list todo --category work --sort due_date  # Complex filtering
```

#### 6. Search tasks (New)
```bash
python task_cli.py search "query" [options]
```

**Options:**
- `--status`: Filter results by status
- `--category, -c`: Filter results by category  
- `--priority, -p`: Filter results by priority

**Examples:**
```bash
python task_cli.py search "grocery"                       # Find all tasks containing "grocery"
python task_cli.py search "report" --category work        # Search work tasks for "report"
python task_cli.py search "urgent" --priority high        # Search high-priority tasks for "urgent"
```

#### 7. Statistics and Reports (New)
```bash
python task_cli.py stats
```

Shows comprehensive statistics including:
- Overall completion rate
- Status breakdown with percentages
- Priority distribution
- Category analysis
- Due date warnings (overdue, due today, due this week)
- Weekly productivity metrics

### Global Options

- `--data-file`: Use custom data file location
- `--no-color`: Disable colored output
- `--version`: Show version information
- `--help, -h`: Show help message

## 📊 Sample Enhanced Output

### Task List with Beautiful Formatting
```
+------+--------------------------------+-------------+----------+----------+--------------+-----------+
|   ID | Description                    | Status      | Priority | Category | Due Date     | Created   |
+======+================================+=============+==========+==========+==============+===========+
|    1 | Buy groceries and cook dinner  | in-progress | high     | shopping | Due in 2 days| 07-22 10:30|
|    2 | Write project documentation    | done        | medium   | work     | No due date  | 07-22 10:31|
|    3 | Review code changes            | todo        | high     | work     | Due today    | 07-22 10:32|
|    4 | Plan summer vacation           | todo        | low      | personal | Due in 15 day| 07-22 10:33|
+------+--------------------------------+-------------+----------+----------+--------------+-----------+

Total: 4 task(s)
```

### Statistics Report
```
📊 Task Statistics Report
==================================================

📋 Overall Statistics:
   Total tasks: 8
   Completion rate: 37.5%

📈 Status Breakdown:
   Todo: 4 (50.0%)
   In-progress: 1 (12.5%)
   Done: 3 (37.5%)

🎯 Priority Breakdown:
   High: 3 (37.5%)
   Medium: 3 (37.5%)
   Low: 2 (25.0%)

📂 Category Breakdown:
   Work: 4 (50.0%)
   Personal: 2 (25.0%)
   Shopping: 2 (25.0%)

⏰ Due Date Summary:
   ⚠ Overdue tasks: 1
   ⚠ Due today: 2
   ℹ Due this week: 3

📅 This Week's Activity:
   Created: 8 tasks
   Completed: 3 tasks
   ⚠ You're behind by 5 tasks
```

## 🏗️ Enhanced Task Properties

Each task now includes:

- **id**: Unique identifier (auto-generated)
- **description**: Task description
- **status**: Current status (todo, in-progress, done)
- **category**: Task category for organization
- **priority**: Priority level (low, medium, high)
- **due_date**: Optional due date (YYYY-MM-DD)
- **createdAt**: Creation timestamp
- **updatedAt**: Last modification timestamp

## 💾 Enhanced Data Storage

### JSON Structure v2.0
```json
{
  "tasks": [
    {
      "id": 1,
      "description": "Buy groceries",
      "status": "todo",
      "category": "shopping",
      "priority": "high",
      "due_date": "2025-07-25",
      "createdAt": "2025-07-22 10:30:15.123456",
      "updatedAt": "2025-07-22 10:30:15.123456"
    }
  ],
  "next_id": 2,
  "metadata": {
    "version": "2.0",
    "created": "2025-07-22 10:30:15.123456",
    "last_modified": "2025-07-22 10:30:15.123456"
  }
}
```

### Backup System
- Automatic backups created before each save operation
- Backups stored in `backups/` directory
- Configurable retention (default: 5 backups)
- Timestamped backup files: `tasks_backup_YYYYMMDD_HHMMSS.json`

### Configuration
Create `config.json` for custom settings:
```json
{
  "data_file": "my_tasks.json",
  "backup_enabled": true,
  "backup_count": 10,
  "tasks_per_page": 25,
  "colors": {
    "high": "red",
    "medium": "yellow",
    "low": "green"
  }
}
```

## 🚨 Enhanced Error Handling

The application provides helpful error messages for:
- **Validation errors**: Empty descriptions, invalid priorities, invalid dates
- **Not found errors**: Non-existent task IDs
- **Format errors**: Invalid date formats, command syntax
- **File errors**: Corrupted JSON, permission issues
- **Input errors**: Invalid filters, malformed queries

## 🧪 Testing

Run the comprehensive test suite:

```bash
# Original test suite (backward compatibility)
python test_task_cli.py

# Enhanced test suite (new features)
python test_task_cli_enhanced.py
```

The enhanced test suite includes:
- Unit tests for all new functionality
- Backward compatibility tests
- Enhanced feature testing (categories, priorities, search)
- Statistics and filtering tests
- Error condition testing
- Data migration testing

## 🎭 Demo

Run the enhanced interactive demo:

```bash
python demo.py
```

The demo showcases:
- All enhanced features
- Complex filtering examples
- Search functionality
- Statistics reporting
- Error handling
- Unicode support

## 📁 Enhanced Project Structure

```
CLI-TASK/
├── task_cli.py              # Main enhanced application
├── config.py                # Configuration management
├── utils.py                 # Utility functions (colors, formatting)
├── test_task_cli.py         # Original test suite
├── test_task_cli_enhanced.py # Enhanced test suite
├── demo.py                  # Enhanced interactive demo
├── README.md                # This documentation
├── requirements.txt         # Dependencies
├── tasks.json               # Data file (created automatically)
├── config.json              # Configuration file (optional)
└── backups/                 # Automatic backups directory
    ├── tasks_backup_20250722_103015.json
    └── tasks_backup_20250722_103230.json
```

## 🔧 Implementation Details

- **Language**: Python 3.6+
- **Storage**: Enhanced JSON format with metadata
- **Architecture**: Modular object-oriented design
- **CLI Framework**: argparse with subcommands
- **Colors**: colorama for cross-platform terminal colors
- **Tables**: tabulate for beautiful table formatting
- **Configuration**: JSON-based with environment variable support
- **Backup**: Automatic with configurable retention
- **Type Hints**: Full type annotation support
- **Testing**: Comprehensive test coverage

## ✅ Enhanced Requirements Compliance

### Original Requirements ✅
- ✅ Add, Update, and Delete tasks
- ✅ Mark a task as in progress or done  
- ✅ List all tasks
- ✅ List tasks by status
- ✅ JSON file storage
- ✅ Error handling

### Enhanced Features ✅
- ✅ Advanced filtering and search
- ✅ Categories and priorities
- ✅ Due dates with urgency indicators
- ✅ Beautiful table formatting with colors
- ✅ Comprehensive statistics and reporting
- ✅ Flexible sorting options
- ✅ Automatic backup system
- ✅ Modern CLI with argparse
- ✅ Configuration management
- ✅ Enhanced error messages
- ✅ Unicode support
- ✅ Backward compatibility

## 🎯 Use Cases

### Personal Task Management
```bash
# Morning routine
python task_cli.py add "Review daily goals" --category personal --priority high
python task_cli.py list --due-soon --sort due_date

# Work tasks
python task_cli.py add "Prepare presentation" --category work --priority high --due 2025-07-25
python task_cli.py list --category work --sort priority --reverse

# Shopping
python task_cli.py add "Buy milk" --category shopping --priority medium
python task_cli.py search "buy" --category shopping
```

### Team Project Management
```bash
# Sprint planning
python task_cli.py add "Implement user authentication" --category development --priority high --due 2025-07-30
python task_cli.py add "Write unit tests" --category testing --priority medium --due 2025-08-01
python task_cli.py add "Deploy to staging" --category deployment --priority low --due 2025-08-05

# Daily standup
python task_cli.py list in-progress
python task_cli.py stats
```

### Academic/Research Work
```bash
# Research tasks
python task_cli.py add "Read papers on ML algorithms" --category research --priority medium --due 2025-07-28
python task_cli.py add "Finish literature review" --category writing --priority high --due 2025-07-30

# Assignment tracking
python task_cli.py list --category coursework --sort due_date
python task_cli.py search "assignment" --priority high
```

## 🤝 Contributing

We welcome contributions! Areas for enhancement:

1. **New Features**: Additional export formats, recurring tasks, time tracking
2. **Integrations**: Calendar sync, cloud storage, notification systems
3. **UI Improvements**: Progress bars, charts, better mobile support
4. **Performance**: Database backend, indexing, caching
5. **Documentation**: Tutorials, examples, API documentation

## 📄 License

This project is open source and available under the MIT License.

## 🎯 Project Evolution

**v1.0** - Basic task management with core CRUD operations
**v2.0** - Enhanced edition with:
- Categories and priorities
- Due dates and urgency tracking
- Advanced search and filtering  
- Beautiful table formatting
- Comprehensive statistics
- Backup system
- Modern CLI interface
- Configuration management

**Future Roadmap:**
- v2.1: Recurring tasks, time tracking
- v2.2: Cloud synchronization, team collaboration
- v2.3: Mobile app companion, API
- v3.0: AI-powered task suggestions, analytics

---

**🎉 Enhanced Task Tracking for Modern Productivity! 🚀✨**

*Built with ❤️ following roadmap.sh project requirements and enhanced for real-world productivity needs*
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
