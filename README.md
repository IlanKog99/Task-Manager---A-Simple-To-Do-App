# Task Manager

A lightweight, GUI-based task manager built with **CustomTkinter**. Easily add, edit, delete, and track tasks with priority levels, due dates, and persistent storage.

## Future Plans

---

- **Settings file** to store user preferences (colors, task visibility, etc.).
- **Dedicated Settings menu** in the app for easier configuration.
- **Custom user paths** for:
  - tasks.json storage location.
  - tasks.txt export file destination.
- **Duplicate task detection**: Notify users about duplicate tasks and handle them appropriately.

## Features

- **Task Management**: Add, edit, delete, and mark tasks as completed.
- **Priority Sorting**: Tasks sorted by urgency (High, Normal, Low).
- **Color-Coded System**:
  - 🔴 Overdue tasks
  - 🟠 Due within 30 days
  - 🔵 Due beyond 30 days
  - ⚪ No due date
  - ✅ Completed tasks
- **Search & Filtering**: Find tasks quickly by description.
- **Export Tasks**: Save incomplete tasks to a formatted text file.
- **Persistent Storage**: Tasks stored in a JSON file in the app directory.
- **Configurable settings**: Show/hide completed tasks, disable colors for a plain view.
- **Modular code design**: Each class is in its own file for better maintainability.

## Installation

### Download the Latest Release

1. Go to the [Releases](https://github.com/IlanKog99/Task-Manager---A-Simple-To-Do-App/releases) page.
2. Download `task-manager-v1.0.0.exe` from the latest release.
3. Run the EXE file (no installation required).

### Notes on Included Files
- The `tasks.json` and `tasks_export.txt` files are provided **only as examples** and are **not required** to use the program.
- The `Task_Project_v1` folder contains the **source code** and example files.

## Changelog - Task Manager V1.0.0

---

**Release Date: 2025-02-23**

### Bug Fixes & Improvements:

- Fixed file path issues for JSON persistence when running as an EXE.
- Improved task sorting logic based on color and priority.
- Streamlined user interface for a smoother experience.
- Enhanced error handling for task input validation.

### Known Issues:

- Slight startup delay in Onefile mode as the EXE unpacks resources.
- Further enhancements and refinements planned for future updates.

## Feedback & Issues

If you encounter any issues or have feature requests, please open an issue in the repository.

