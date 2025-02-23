# Task Manager

A lightweight, GUI-based task manager built with **CustomTkinter**. Easily add, edit, delete, and track tasks with priority levels, due dates, and persistent storage.

## Future Plans

---

- **Settings file** to store user preferences (colors, task visibility, etc.).
- **Dedicated Settings menu** in the app for easier configuration.
- **Custom user paths** for:
  - tasks.json storage location.
  - tasks.txt export file destination.
- **Duplicate task detection**: Warn users if a task already exists before adding it.

## Features

- **Task Management**: Add, edit, delete, and mark tasks as completed.
- **Priority Sorting**: Sort tasks by urgency (High, Normal, Low).
- **Color-Coded System**:
  - 🔴 Overdue tasks
  - 🟠 Due within 30 days
  - 🔵 Due beyond 30 days
  - ⚪ No due date
  - ✅ Completed tasks
- **Search & Filtering**: Quickly find tasks by description.
- **Export Tasks**: Save incomplete tasks to a text file.
- **Persistent Storage**: Tasks are stored in a JSON file for future use.
- **Configurable settings**: Toggle completed task visibility, disable colors, etc.
- **Well-structured code**: Each major function is in its own file.

## Installation

### Download the Latest Release

1. Go to the [Releases](https://github.com/yourusername/task-manager/releases) page.
2. Download `task-manager-v1.0.0.exe` from the latest release.
3. Run the EXE file (no installation required).

### Notes on Included Files
- The `tasks.json` and `tasks_export.txt` files are **just examples**—you don’t need them to use the program.
- The `Task_Project_v1` folder contains **the source code and sample files**.

## Changelog - Task Manager V1.0.0

---

**Release Date: 2025-02-23**

### Bug Fixes & Improvements:

- Fixed issues with saving/loading JSON when running as an EXE.
- Tweaked task sorting for better organization.
- Smoothed out UI interactions for a better experience.
- Improved error handling when adding tasks.

### Known Issues:

- The EXE takes a second to load due to Onefile mode unpacking.
- More refinements are planned in upcoming updates.

## Feedback & Issues

Found a bug? Got a feature idea? Open an issue in the repository!

