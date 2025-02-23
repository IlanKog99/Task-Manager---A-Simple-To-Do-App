import os
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Optional, Dict, Any

# Constants for task priority levels
PRIORITY_LEVELS: Dict[int, str] = {1: "Low", 2: "Normal", 3: "High"}
DESKTOP_PATH: Path = Path.home() / "Desktop"
TASKS_FILE: Path = DESKTOP_PATH / "tasks.json"

class Task:
    """
    Represents a single task with various attributes and methods for management.
    """
    def __init__(
        self, 
        description: str, 
        completed: bool = False, 
        due_date: Optional[datetime] = None, 
        priority: int = 2, 
        additional_info: Optional[str] = None,
        created_date: Optional[datetime] = None,
        deleted: bool = False
    ):
        self.description = description
        self.completed = completed
        self.due_date = due_date
        self.priority = priority
        self.additional_info = additional_info
        self.created_date = created_date or datetime.now()
        self.deleted = deleted

    def mark_completed(self) -> None:
        """Mark the task as completed."""
        if self.completed:
            print("Task is already completed!")
        else:
            self.completed = True

    def reschedule(self, new_due_date_str: str) -> None:
        """
        Reschedule the task with a new due date.
        """
        try:
            new_due_date = datetime.strptime(new_due_date_str, "%d/%m/%y")
            self.due_date = new_due_date
        except ValueError:
            print("Invalid date format! Please use DD/MM/YY.")

    def update_priority(self, new_priority: int) -> None:
        """Update task priority."""
        if new_priority in PRIORITY_LEVELS:
            self.priority = new_priority
        else:
            print("Invalid priority level! Choose 1 (Low), 2 (Normal), or 3 (High).")

    def update_description(self, new_description: str) -> None:
        """Update task description."""
        if new_description.strip():
            self.description = new_description
        else:
            print("Description cannot be empty!")

    def update_additional_info(self, new_info: Optional[str]) -> None:
        """Update additional information for the task."""
        self.additional_info = new_info if new_info and new_info.strip() else None

    def to_dict(self) -> Dict[str, Any]:
        """Convert task to a dictionary for JSON serialization."""
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
    def from_dict(cls, data: Dict[str, Any]) -> 'Task':
        """Create a Task instance from a dictionary."""
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
        """Generate a formatted string representation of the task."""
        status = "Completed" if self.completed else "Incomplete"
        due_date_str = self.due_date.strftime("%d/%m/%y") if self.due_date else "No due date"
        priority_str = PRIORITY_LEVELS.get(self.priority, "Unknown")
        created_date_str = self.created_date.strftime("%d/%m/%y")
        return f"{self.description.ljust(30)} | {status.ljust(10)} | {due_date_str.ljust(10)} | {priority_str.ljust(10)} | Created: {created_date_str}"

def clear_screen() -> None:
    """Clear the console screen across different operating systems."""
    os.system('cls' if os.name == 'nt' else 'clear')

def load_tasks() -> List[Task]:
    """Load tasks from a JSON file."""
    try:
        with open(TASKS_FILE, "r") as f:
            return [Task.from_dict(data) for data in json.load(f)]
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_tasks(tasks: List[Task]) -> None:
    """Save tasks to a JSON file."""
    tasks_data = [task.to_dict() for task in tasks]
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks_data, f, indent=2)

def task_exists(tasks: List[Task], description: str) -> bool:
    """Check if a task with the given description already exists."""
    return any(task.description.lower() == description.lower() for task in tasks)

def color_text(txt: str, color: str, write_line: bool = False) -> str:
    '''Returns a colored string.
    Args:
        txt - string to be colored.
        color - color to be used.
        write_line - if True, will print the colored text (False by default).'''
    colors = {
        "red": "\033[31m",
        "neon_red": "\033[38;5;196m",
        "dark_red": "\033[38;5;52m",
        "crimson": "\033[38;5;88m",
        "green": "\033[38;5;28m",
        "dark_green": "\033[38;5;22m",
        "orange": "\033[33m",
        "blue": "\033[34m",
        "cyan": "\033[36m",
        "magenta": "\033[35m",
        "white": "\033[37m",
    }
    reset = "\033[0m"
    if write_line:
        print(f"{colors.get(color, reset)}{txt}{reset}")
    return f"{colors.get(color, reset)}{txt}{reset}"

def get_task_color(task: Task) -> str:
    """Determine the color for a task based on its status and due date."""
    if task.completed:
        return "green"
    elif task.due_date:
        today = datetime.now()
        if task.due_date < today:
            return "neon_red"
        elif (task.due_date - today) <= timedelta(days=30):
            return "orange"
        else:
            return "blue"
    return "white"

def sort_tasks(tasks: List[Task]) -> List[Task]:
    """Sort tasks by color and priority."""
    color_order = {"neon_red": 0, "orange": 1, "blue": 2, "white": 3, "green": 4}
    return sorted(
        tasks,
        key=lambda x: (
            color_order.get(get_task_color(x), 5),  # Sort by color
            -x.priority  # Sort by priority (high to low)
        )
    )

def export_tasks_to_txt(tasks: List[Task], file_path: Path) -> None:
    """Export only incomplete tasks to a text file with colored formatting, including additional info."""
    with open(file_path, "w") as f:
        for task in tasks:
            if not task.deleted and not task.completed:
                color = get_task_color(task)
                task_str = str(task)
                additional_info = task.additional_info or "No additional info"  # Handle missing info
                f.write(f"{task_str} | Info: {additional_info}\n")  # Added info to export

def display_tasks(tasks: List[Task]) -> None:
    clear_screen()
    if not tasks:
        print("No tasks available!")
        return

    active_tasks = [task for task in tasks if not task.deleted]
    sorted_tasks = sort_tasks(active_tasks)

    print("\nTo-Do List:")
    print("Color Legend: ", end="")
    print(color_text("Red = Overdue", "neon_red"), end=" | ")
    print(color_text("Orange = Due in 30 days", "orange"), end=" | ")
    print(color_text("Blue = Due in >30 days", "blue"), end=" | ")
    print(color_text("White = No due date", "white"), end=" | ")
    print(color_text("Green = Completed", "green"))
    print("-" * 120)

    for i, task in enumerate(sorted_tasks, 1):
        color = get_task_color(task)
        task_str = str(task)
        additional_info = task.additional_info or "No additional info"

        # Color each part separately
        colored_task_str = color_text(task_str, color)
        colored_info_label = color_text(" | Info: ", color)  # Color " | Info: "
        colored_additional_info = color_text(additional_info, color)

        print(f"{i}. {colored_task_str}{colored_info_label}{colored_additional_info}")

    print("-" * 120)

def confirm_delete_task(task: Task) -> bool:
    """Display the task details and ask for confirmation to delete."""
    clear_screen()
    print("\nTask to be deleted:")
    print("-" * 90)
    print(task)
    print("-" * 90)
    confirmation = input("\nAre you sure you want to delete this task? This action cannot be undone. (y/N): ").strip().lower()
    return confirmation == "y"

def manage_and_view_tasks(tasks: List[Task]) -> None:
    """Combined menu for viewing and managing tasks."""
    while True:
        display_tasks(tasks)
        if not tasks:
            input("\nPress Enter to return to the main menu...")
            return

        print("\nOptions:")
        print("1. Export to .txt file")
        print("2. Continue to Managing")
        print("3. Return to Main Menu")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            export_path = DESKTOP_PATH / "tasks_export.txt"
            export_tasks_to_txt(tasks, export_path)
            print(f"Tasks exported to {export_path}!")
            input("\nPress Enter to continue...")
        elif choice == "2":
            manage_tasks_menu(tasks)
        elif choice == "3":
            return
        else:
            print("Invalid choice!")
            input("\nPress Enter to continue...")

def manage_tasks_menu(tasks: List[Task]) -> None:
    """Task management menu."""
    while True:
        display_tasks(tasks)
        if not tasks:
            return

        print("\nTask Management Menu:")
        print("1. Mark Task Completed")
        print("2. Reschedule Task")
        print("3. Update Priority")
        print("4. Change Description")
        print("5. Update Additional Info")
        print("6. Delete Task")
        print("7. Mark Task as Ongoing")
        print("0. Return to Previous Menu")

        choice = input("Choose an option: ").strip()

        try:
            task_num = -1
            if choice in ['1', '2', '3', '4', '5', '6', '7']:
                while True:
                    try:
                        task_num = int(input("Enter task number (0 to cancel): ")) - 1
                        if task_num == -1:
                            return
                        active_tasks = [task for task in tasks if not task.deleted]
                        sorted_tasks = sort_tasks(active_tasks)

                        if 0 <= task_num < len(sorted_tasks): # Check against sorted list
                            selected_task = sorted_tasks[task_num]  # Get task from sorted list
                            task_index = tasks.index(selected_task)  # Find original index
                            break
                        else:
                            print("Invalid task number!")
                    except ValueError:
                        print("Please enter a valid number!")

                if task_num != -1: # if the user didn't cancel
                    if choice == '1':
                        tasks[task_index].mark_completed() # Use the original index
                        print("Task marked as completed!")
                    elif choice == '2':
                        new_date = input("Enter new due date (DD/MM/YY): ").strip()
                        tasks[task_index].reschedule(new_date)
                    elif choice == '3':
                        new_pri = input("Enter new priority (1-3): ").strip()
                        tasks[task_index].update_priority(int(new_pri))
                    elif choice == '4':
                        new_desc = input("Enter new task description: ").strip()
                        tasks[task_index].update_description(new_desc)
                    elif choice == '5':
                        new_info = input("Enter new additional info (or blank to remove): ").strip()
                        tasks[task_index].update_additional_info(new_info or None)
                    elif choice == '6':
                        if confirm_delete_task(tasks[task_index]):
                            tasks.pop(task_index)
                            print("Task deleted successfully!")
                        else:
                            print("Deletion canceled.")
                    elif choice == '7':
                        tasks[task_index].completed = False
                        print("Task marked as ongoing!")

            elif choice == '0':
                return

            else:
                print("Invalid choice!")

        except ValueError:
            print("Please enter a valid number!")

        input("\nPress Enter to continue...")

def add_task(tasks: List[Task]) -> None:
    """Interactively add a new task to the task list."""
    # Task description input
    while True:
        description = input("\nEnter task description (or 'back' to cancel): ").strip()
        if description.lower() in ['back', 'cancel']:
            print("Canceling task creation...")
            return
        if description:
            # Check for existing task
            if task_exists(tasks, description):
                print("\nA task with this description already exists!")
                choice = input("Do you want to add it anyway? (y/N): ").strip().lower()
                if choice != 'y':
                    return
            break
        print("Error: Description cannot be empty!")

    # Due date input
    due_date = None
    while True:
        due_date_str = input("Enter due date (DD/MM/YY) or leave blank: ").strip()
        if due_date_str.lower() in ['back', 'cancel']:
            return
        if not due_date_str:
            break
        try:
            due_date = datetime.strptime(due_date_str, "%d/%m/%y")
            break
        except ValueError:
            print("Invalid date! Please use DD/MM/YY format or leave blank.")

    # Priority input
    priority = 2  # Default value
    while True:
        priority_str = input("Enter priority (1=Low, 2=Normal, 3=High) [default 2]: ").strip()
        if priority_str.lower() in ['back', 'cancel']:
            return
        if not priority_str:
            break
        try:
            priority = int(priority_str)
            if priority not in PRIORITY_LEVELS:
                print("Priority must be 1, 2, or 3!")
                continue
            break
        except ValueError:
            print("Invalid input! Please enter a number.")

    # Additional info input
    additional_info = input("Enter additional notes (optional): ").strip()

    # Create and add task
    tasks.append(Task(
        description=description,
        due_date=due_date,
        priority=priority,
        additional_info=additional_info or None
    ))
    print("Task added successfully!")

def main():
    """Main application loop for task management."""
    tasks = load_tasks()
    
    while True:
        clear_screen()
        print("\n--- Task Manager ---")
        print("1. Add a Task")
        print("2. Manage & View Tasks")
        print("3. Save & Exit")
        
        choice = input("\nChoose an option: ").strip()
        
        if choice == "1":
            add_task(tasks)
        elif choice == "2":
            manage_and_view_tasks(tasks)
        elif choice == "3":
            save_tasks(tasks)
            print("Tasks saved. Goodbye!")
            break
        else:
            clear_screen()
            print("\nInvalid choice! Please try again.")

if __name__ == "__main__":
    main()