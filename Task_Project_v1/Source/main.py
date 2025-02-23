"""
main.py - Where everything kicks off.
Sets up TaskManager and launches the GUI.
"""

from task_manager import TaskManager
from task_gui import TaskGUI

def main():
    """
    Create TaskManager instance and launch the GUI.
    """
    task_manager = TaskManager()
    app = TaskGUI(task_manager)
    app.mainloop()

if __name__ == "__main__":
    main()
