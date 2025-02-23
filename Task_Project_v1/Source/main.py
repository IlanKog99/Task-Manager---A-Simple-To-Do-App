"""
main.py - Entry point for the task manager app.
Initializes the TaskManager and launches the GUI.
"""

from task_manager import TaskManager
from task_gui import TaskGUI

def main():
    """
    Func initializes TaskManager and starts the GUI main loop.
    """
    task_manager = TaskManager()
    app = TaskGUI(task_manager)
    app.mainloop()

if __name__ == "__main__":
    main()
