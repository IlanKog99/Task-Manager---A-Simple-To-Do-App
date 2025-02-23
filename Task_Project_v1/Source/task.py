"""
task.py - Contains the Task class.
This file defines the Task object which holds details like description, due date, priority, etc.
"""

from datetime import datetime
from helpers import PRIORITY_LEVELS

class Task:
    """
    Class for a task.
    
    Stores info like description, due date, priority, additional info, creation date, and deletion flag.
    """
    def __init__(self, description: str, completed: bool = False, due_date: datetime | None = None, 
                priority: int = 2, additional_info: str | None = None, created_date: datetime | None = None, 
                deleted: bool = False):
        """
        Init method.
        
        Args:
        description: What the task is about.
        completed: Bool flag if task's done.
        due_date: When the task is due.
        priority: Task's priority (1=Low, 2=Normal, 3=High).
        additional_info:additional info.
        created_date: When the task was made (defaults to now).
        deleted: Bool flag if task is marked as deleted.
        """
        self.description = description
        self.completed = completed
        self.due_date = due_date
        self.priority = priority
        self.additional_info = additional_info
        self.created_date = created_date or datetime.now()
        self.deleted = deleted

    def mark_completed(self) -> None:
        """
        Method marks the task as completed.
        
        If already done, prints a warning.
        """
        if self.completed:
            print("Task is already completed!")
        else:
            self.completed = True

    def reschedule(self, new_due_date_str: str) -> None:
        """
        Method reschedules the task.
        
        Args:
          new_due_date_str: New due date in DD/MM/YY format.
        """
        try:
            new_due_date = datetime.strptime(new_due_date_str, "%d/%m/%y")
            self.due_date = new_due_date
        except ValueError:
            print("Invalid date format! Please use DD/MM/YY.")

    def update_priority(self, new_priority: int) -> None:
        """
        Method updates the task's priority.
        
        Args:
          new_priority: New priority value (1, 2, or 3).
        """
        if new_priority in PRIORITY_LEVELS:
            self.priority = new_priority
        else:
            print("Invalid priority level! Choose 1 (Low), 2 (Normal), or 3 (High).")

    def update_description(self, new_description: str) -> None:
        """
        Method updates the task's description.
        
        Args:
          new_description: The new description text.
        """
        if new_description.strip():
            self.description = new_description
        else:
            print("Description cannot be empty!")

    def update_additional_info(self, new_info: str) -> None:
        """
        Method updates extra info for the task.
        
        Args:
          new_info: The new additional info.
        """
        self.additional_info = new_info if new_info and new_info.strip() else None

    def to_dict(self) -> dict:
        """
        Method converts the Task to a dict for JSON saving.
        
        Returns a dict with all the task info.
        """
        return {
            "description": self.description,
            "completed": self.completed,
            "due_date": self.due_date.strftime("%d/%m/%y") if self.due_date else None,
            "priority": self.priority,
            "additional_info": self.additional_info,
            "created_date": self.created_date.strftime("%d/%m/%y"),
            "deleted": self.deleted
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Task':
        """
        Class method that builds a Task from a dict.
        
        Args:
          data: Dict with task details.
        
        Returns a Task object.
        """
        due_date_str = data.get("due_date")
        created_date_str = data.get("created_date")
        due_date = datetime.strptime(due_date_str, "%d/%m/%y") if due_date_str else None
        created_date = datetime.strptime(created_date_str, "%d/%m/%y") if created_date_str else None
        return cls(
            description=data["description"],
            completed=data["completed"],
            due_date=due_date,
            priority=data["priority"],
            additional_info=data["additional_info"],
            created_date=created_date,
            deleted=data.get("deleted", False)
        )

    def __str__(self) -> str:
        """
        Method returns a formatted string for the task.
        
        Shows description, status, due date, priority, and creation date.
        """
        status = "Completed" if self.completed else "Incomplete"
        due_date_str = self.due_date.strftime("%d/%m/%y") if self.due_date else "No due date"
        priority_str = PRIORITY_LEVELS.get(self.priority, "Unknown")
        created_date_str = self.created_date.strftime("%d/%m/%y")
        return f"{self.description.ljust(30)} | {status.ljust(10)} | {due_date_str.ljust(10)} | {priority_str.ljust(10)} | Created: {created_date_str}"
