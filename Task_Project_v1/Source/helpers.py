"""
helpers.py - Global constants and helper funcs for the task app.
This file holds the file path, priority mapping, and helper funcs for loading,
saving, sorting, and exporting tasks.
"""

import os
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Any, Dict

# Global mapping for task priorities
PRIORITY_LEVELS: Dict[int, str] = {1: "Low", 2: "Normal", 3: "High"}

# Tasks file will live in the current working directory (where the exe runs)
TASKS_FILE: Path = Path.cwd() / "tasks.json"

def load_tasks() -> List[Any]:
    """
    Func loads tasks from the JSON file.
    
    Tries to read TASKS_FILE and converts each dict into a Task object.
    If file is missing or busted, returns an empty list.
    """
    try:
        with open(TASKS_FILE, "r") as f:
            # Importing Task here to avoid circular import probs
            from task import Task
            return [Task.from_dict(data) for data in json.load(f)]
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_tasks(tasks: List[Any]) -> None:
    """
    Func saves the list of tasks to a JSON file.
    
    Converts each Task into a dict and dumps it into TASKS_FILE.
    """
    tasks_data = [task.to_dict() for task in tasks]
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks_data, f, indent=2)

def get_task_color(task) -> str:
    """
    Func determines the color for a task based on its status and due date.
    
    Returns:
      - "green" if task is completed.
      - "red" if overdue.
      - "orange" if due within 30 days.
      - "blue" if due in more than 30 days.
      - "white" if no due date.
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
    Func sorts tasks based on color and priority.
    
    Sorting order: red (most urgent), then orange, blue, white, and finally green.
    Within the same color, tasks with higher priority come first.
    """
    color_order = {"red": 0, "orange": 1, "blue": 2, "white": 3, "green": 4}
    return sorted(
        tasks,
        key=lambda x: (
            color_order.get(get_task_color(x), 5),  # Lower value means higher urgency
            -x.priority  # Higher priority number = more important
        )
    )

def export_tasks_to_txt(tasks: List[Any], file_path: Path) -> None:
    """
    Func exports incomplete tasks to a text file.
    
    Goes through tasks and writes a formatted line for each task that's not completed or deleted.
    """
    with open(file_path, "w") as f:
        for task in tasks:
            if not task.deleted and not task.completed:
                task_str = str(task)
                additional_info = task.additional_info or "No additional info"
                f.write(f"{task_str} | Info: {additional_info}\n")
