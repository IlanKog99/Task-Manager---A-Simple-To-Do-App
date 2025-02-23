"""
task_manager.py - Contains the TaskManager class.
This file is all about managing the list of tasks: loading 'em from file and saving 'em back.
"""

from typing import List
from task import Task
from helpers import TASKS_FILE, load_tasks, save_tasks

class TaskManager:
    """
    Class to manage tasks.
    
    Loads tasks from a JSON file and saves them when needed.
    """
    def __init__(self):
        """
        Init method.
        
        Loads tasks from file and stores them in self.tasks.
        """
        self.tasks: List[Task] = load_tasks() # type: ignore

    def save(self) -> None:
        """
        Method saves current tasks to the JSON file.
        """
        save_tasks(self.tasks)
