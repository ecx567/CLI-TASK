#!/usr/bin/env python3
"""
Configuration module for Task Tracker CLI

This module handles all configuration settings for the Task Tracker CLI,
including default values, environment variables, and user preferences.
"""

import os
import json
from pathlib import Path
from typing import Dict, Any, Optional


class Config:
    """Configuration management class."""
    
    # Default configuration values
    DEFAULT_CONFIG = {
        "data_file": "tasks.json",
        "date_format": "%Y-%m-%d %H:%M:%S.%f",
        "display_date_format": "%Y-%m-%d %H:%M:%S",
        "max_description_length": 1000,
        "tasks_per_page": 20,
        "default_status": "todo",
        "valid_statuses": ["todo", "in-progress", "done"],
        "valid_priorities": ["low", "medium", "high"],
        "backup_enabled": True,
        "backup_count": 5,
        "colors": {
            "todo": "yellow",
            "in-progress": "blue", 
            "done": "green",
            "high": "red",
            "medium": "yellow",
            "low": "cyan"
        }
    }
    
    def __init__(self, config_file: str = "config.json"):
        """Initialize configuration."""
        self.config_file = Path(config_file)
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file or environment variables."""
        config = self.DEFAULT_CONFIG.copy()
        
        # Load from config file if exists
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    file_config = json.load(f)
                    config.update(file_config)
            except (json.JSONDecodeError, IOError):
                pass  # Use defaults if config file is invalid
        
        # Override with environment variables
        env_mappings = {
            "TASK_CLI_DATA_FILE": "data_file",
            "TASK_CLI_DATE_FORMAT": "date_format",
            "TASK_CLI_MAX_DESC_LENGTH": "max_description_length",
            "TASK_CLI_TASKS_PER_PAGE": "tasks_per_page"
        }
        
        for env_var, config_key in env_mappings.items():
            env_value = os.getenv(env_var)
            if env_value:
                if config_key in ["max_description_length", "tasks_per_page"]:
                    try:
                        config[config_key] = int(env_value)
                    except ValueError:
                        pass
                else:
                    config[config_key] = env_value
        
        return config
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value."""
        return self.config.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """Set configuration value."""
        self.config[key] = value
    
    def save_config(self) -> None:
        """Save current configuration to file."""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
        except IOError as e:
            print(f"Warning: Could not save configuration: {e}")
    
    def reset_to_defaults(self) -> None:
        """Reset configuration to default values."""
        self.config = self.DEFAULT_CONFIG.copy()
        self.save_config()


# Global configuration instance
config = Config()
