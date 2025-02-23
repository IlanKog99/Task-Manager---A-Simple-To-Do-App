"""
task_manager.py - Main logic for loading and saving.
"""

from typing import List
from task import Task
from helpers import TASKS_FILE, load_tasks, save_tasks

class TaskManager:
    """
    The TaskManager class - keeps tasks organized.
    Loads tasks on start up and makes sure they get saved when needed.
    """
    def __init__(self):
        """
        Loads tasks from JSON file.
        """
        self.tasks: List[Task] = load_tasks() # type: ignore

    def save(self) -> None:
        """
        Saves tasks to JSON file.
        """
        save_tasks(self.tasks)
