"""
helpers.py - All the stuff needed across the app.
Keeps track of file paths, priority levels, has funcs for loading, saving, sorting, etc.
"""

import os
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Any, Dict

# Quick lookup for task priorities
PRIORITY_LEVELS: Dict[int, str] = {1: "Low", 2: "Normal", 3: "High"}

# Keep tasks.json in the same folder as the exe
TASKS_FILE: Path = Path.cwd() / "tasks.json"

def load_tasks() -> List[Any]:
    """
    Grabs tasks from JSON.
    If something's wrong with the file or it doesn't exist, returns an empty list.
    """
    try:
        with open(TASKS_FILE, "r") as f:
            from task import Task
            return [Task.from_dict(data) for data in json.load(f)]
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_tasks(tasks: List[Any]) -> None:
    """
    Converts Task obj to a dict and saves it.
    """
    tasks_data = [task.to_dict() for task in tasks]
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks_data, f, indent=2)

def get_task_color(task) -> str:
    """
    Sets color to task based on status and due date:
    - Green = Done
    - Red = Overdue
    - Orange = Due soon (within 30 days)
    - Blue = Due later
    - White = No due date set
    """
    if task.completed:
        return "green"
    elif task.due_date:
        today = datetime.now()
        if task.due_date < today:
            return "red"
        elif (task.due_date - today) <= timedelta(days=30):
            return "orange"
        else:
            return "blue"
    return "white"

def sort_tasks(tasks: List[Any]) -> List[Any]:
    """
    Sorts tasks by due date and priority (color).
    In each color, higher priority tasks come first.
    """
    color_order = {"red": 0, "orange": 1, "blue": 2, "white": 3, "green": 4}
    return sorted(
        tasks,
        key=lambda x: (
            color_order.get(get_task_color(x), 5),  # Lower = more urgent
            -x.priority  # Higher priority = more important
        )
    )

def export_tasks_to_txt(tasks: List[Any], file_path: Path) -> None:
    """
    Export incomplete tasks to .txt.
    """
    with open(file_path, "w") as f:
        for task in tasks:
            if not task.deleted and not task.completed:
                task_str = str(task)
                additional_info = task.additional_info or "No additional info"
                f.write(f"{task_str} | Info: {additional_info}\n")
