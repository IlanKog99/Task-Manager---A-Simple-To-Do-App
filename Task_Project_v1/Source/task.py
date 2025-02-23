"""
task.py - The core Task class that makes everything work.
Handles task properties like descriptions, due dates, priorities, etc.
"""

from datetime import datetime
from helpers import PRIORITY_LEVELS

class Task:
    """
    Task class for each task in the task manager.
    Keeps track of everything about a task: description, due date, priority, and additional info.
    """
    def __init__(self, description: str, completed: bool = False, due_date: datetime | None = None, 
                priority: int = 2, additional_info: str | None = None, created_date: datetime | None = None, 
                deleted: bool = False):
        """
        Sets up a new task with all its details.
        - description: What's this task about?
        - completed: Done or not? (defaults to not)
        - due_date: When's it due? (optional)
        - priority: How important? (1=Low, 2=Normal, 3=High - defaults to 2)
        - additional_info: Any extra notes (optional)
        - created_date: Date of creation (defaults to now)
        - deleted: False by default
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
        Marks task as done.
        Handles weird edge cases where user found a way to mark a task as done twice.
        """
        if self.completed:
            print("Hey, this task is already done!")
        else:
            self.completed = True

    def reschedule(self, new_due_date_str: str) -> None:
        """
        Changes when the task is due.
        Gets a date string in DD/MM/YY format.
        Changes string to datetime object which handles invalid dates.
        """
        try:
            new_due_date = datetime.strptime(new_due_date_str, "%d/%m/%y")
            self.due_date = new_due_date
        except ValueError:
            print("Oops! That's not a valid date. Use DD/MM/YY format please!")

    def update_priority(self, new_priority: int) -> None:
        """
        Changes task priority.
        Uses 1 for Low, 2 for Normal, or 3 for High priority.
        """
        if new_priority in PRIORITY_LEVELS:
            self.priority = new_priority
        else:
            print("That's not a valid priority! Pick 1 (Low), 2 (Normal), or 3 (High).")

    def update_description(self, new_description: str) -> None:
        """
        Changes task description.
        Can't be empty.
        Description is used as name for the task.
        """
        if new_description.strip():
            self.description = new_description
        else:
            print("Come on, we need some description here!")

    def update_additional_info(self, new_info: str) -> None:
        """
        Updates additional info field.
        Optional can be left blank, will be set to None.
        """
        self.additional_info = new_info if new_info and new_info.strip() else None

    def to_dict(self) -> dict:
        """
        Converts task into a dict, used for saving to JSON.
        Handles date formatting.
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
        Converts dict back to Task object.
        Handles date parsing.
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
        Returns a nice readable string version of the task.
        Shows all task info (description, status, due date, priority, and creation date) in a readable format.
        """
        status = "Completed" if self.completed else "Incomplete"
        due_date_str = self.due_date.strftime("%d/%m/%y") if self.due_date else "No due date"
        priority_str = PRIORITY_LEVELS.get(self.priority, "Unknown")
        created_date_str = self.created_date.strftime("%d/%m/%y")
        return f"{self.description.ljust(30)} | {status.ljust(10)} | {due_date_str.ljust(10)} | {priority_str.ljust(10)} | Created: {created_date_str}"
