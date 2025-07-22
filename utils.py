
"""
Utilities module for Task Tracker CLI

This module provides utility functions for formatting, colors, and display.
"""

import shutil
from datetime import datetime, timedelta
from typing import List, Dict, Any
from config import config

try:
    from colorama import init, Fore, Back, Style
    init(autoreset=True)
    COLORS_AVAILABLE = True
except ImportError:
    COLORS_AVAILABLE = False
    # Fallback color definitions
    class Fore:
        RED = ""
        GREEN = ""
        YELLOW = ""
        BLUE = ""
        CYAN = ""
        MAGENTA = ""
        WHITE = ""
        RESET = ""
    
    class Style:
        BRIGHT = ""
        DIM = ""
        RESET_ALL = ""

try:
    from tabulate import tabulate
    TABULATE_AVAILABLE = True
except ImportError:
    TABULATE_AVAILABLE = False


def get_color_for_status(status: str) -> str:
    """Get color code for task status."""
    if not COLORS_AVAILABLE:
        return ""
    
    color_map = {
        "todo": Fore.YELLOW,
        "in-progress": Fore.BLUE,
        "done": Fore.GREEN
    }
    return color_map.get(status, Fore.WHITE)


def get_color_for_priority(priority: str) -> str:
    """Get color code for task priority."""
    if not COLORS_AVAILABLE:
        return ""
    
    color_map = {
        "high": Fore.RED + Style.BRIGHT,
        "medium": Fore.YELLOW,
        "low": Fore.CYAN
    }
    return color_map.get(priority, Fore.WHITE)


def format_date(date_str: str, short: bool = False) -> str:
    """Format date string for display."""
    try:
        date_format = config.get("date_format")
        dt = datetime.strptime(date_str, date_format)
        
        if short:
            return dt.strftime("%m-%d %H:%M")
        else:
            display_format = config.get("display_date_format")
            return dt.strftime(display_format)
    except (ValueError, TypeError):
        return date_str or "N/A"


def format_due_date(due_date: str) -> str:
    """Format due date with color coding based on urgency."""
    if not due_date:
        return "No due date"
    
    try:
        due = datetime.strptime(due_date, "%Y-%m-%d").date()
        today = datetime.now().date()
        days_until = (due - today).days
        
        if days_until < 0:
            color = Fore.RED + Style.BRIGHT if COLORS_AVAILABLE else ""
            return f"{color}Overdue ({abs(days_until)} days)"
        elif days_until == 0:
            color = Fore.RED if COLORS_AVAILABLE else ""
            return f"{color}Due today"
        elif days_until <= 3:
            color = Fore.YELLOW if COLORS_AVAILABLE else ""
            return f"{color}Due in {days_until} days"
        else:
            return f"Due in {days_until} days"
    except ValueError:
        return due_date


def get_terminal_width() -> int:
    """Get terminal width for formatting."""
    try:
        return shutil.get_terminal_size().columns
    except Exception:
        return 80  # Default width


def truncate_text(text: str, max_length: int) -> str:
    """Truncate text with ellipsis if too long."""
    if len(text) <= max_length:
        return text
    return text[:max_length - 3] + "..."


def format_task_table(tasks: List[Dict[str, Any]], show_colors: bool = True) -> str:
    """Format tasks as a table using tabulate if available."""
    if not tasks:
        return "No tasks found."
    
    # Prepare table data
    headers = ["ID", "Description", "Status", "Priority", "Category", "Due Date", "Created"]
    table_data = []
    
    terminal_width = get_terminal_width()
    desc_width = max(20, min(40, terminal_width // 4))
    
    for task in tasks:
        status = task["status"]
        priority = task["priority"]
        
        # Apply colors if available and requested
        if show_colors and COLORS_AVAILABLE:
            status_colored = f"{get_color_for_status(status)}{status}{Style.RESET_ALL}"
            priority_colored = f"{get_color_for_priority(priority)}{priority}{Style.RESET_ALL}"
        else:
            status_colored = status
            priority_colored = priority
        
        row = [
            task["id"],
            truncate_text(task["description"], desc_width),
            status_colored,
            priority_colored,
            task.get("category", "general"),
            format_due_date(task.get("due_date")),
            format_date(task["createdAt"], short=True)
        ]
        table_data.append(row)
    
    if TABULATE_AVAILABLE:
        return tabulate(table_data, headers=headers, tablefmt="grid")
    else:
        # Fallback to simple formatting
        return format_simple_table(headers, table_data)


def format_simple_table(headers: List[str], data: List[List[str]]) -> str:
    """Simple table formatting fallback."""
    # Calculate column widths
    col_widths = [len(header) for header in headers]
    for row in data:
        for i, cell in enumerate(row):
            # Strip ANSI color codes for width calculation
            clean_cell = strip_ansi_codes(str(cell))
            col_widths[i] = max(col_widths[i], len(clean_cell))
    
    # Create format string
    format_str = " | ".join(f"{{:<{width}}}" for width in col_widths)
    
    # Build table
    result = []
    result.append(format_str.format(*headers))
    result.append("-" * (sum(col_widths) + 3 * (len(headers) - 1)))
    
    for row in data:
        formatted_row = []
        for i, cell in enumerate(row):
            if COLORS_AVAILABLE and any(color in str(cell) for color in [Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.CYAN]):
                # For colored cells, pad after stripping color codes
                clean_cell = strip_ansi_codes(str(cell))
                padding = col_widths[i] - len(clean_cell)
                formatted_row.append(str(cell) + " " * padding)
            else:
                formatted_row.append(f"{cell:<{col_widths[i]}}")
        result.append(" | ".join(formatted_row))
    
    return "\n".join(result)


def strip_ansi_codes(text: str) -> str:
    """Strip ANSI color codes from text."""
    import re
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', text)


def print_success(message: str) -> None:
    """Print success message with green color."""
    if COLORS_AVAILABLE:
        print(f"{Fore.GREEN}✓ {message}{Style.RESET_ALL}")
    else:
        print(f"✓ {message}")


def print_error(message: str) -> None:
    """Print error message with red color."""
    if COLORS_AVAILABLE:
        print(f"{Fore.RED}✗ {message}{Style.RESET_ALL}")
    else:
        print(f"✗ {message}")


def print_warning(message: str) -> None:
    """Print warning message with yellow color."""
    if COLORS_AVAILABLE:
        print(f"{Fore.YELLOW}⚠ {message}{Style.RESET_ALL}")
    else:
        print(f"⚠ {message}")


def print_info(message: str) -> None:
    """Print info message with blue color."""
    if COLORS_AVAILABLE:
        print(f"{Fore.BLUE}ℹ {message}{Style.RESET_ALL}")
    else:
        print(f"ℹ {message}")
