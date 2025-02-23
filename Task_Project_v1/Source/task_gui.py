"""
task_gui.py - Contains the TaskGUI class.
Uses customtkinter to create GUI.
"""

import customtkinter as ctk # type: ignore
import tkinter.messagebox as messagebox
from datetime import datetime, timedelta
from pathlib import Path
from task import Task
from task_manager import TaskManager
from helpers import PRIORITY_LEVELS, get_task_color, sort_tasks, export_tasks_to_txt

class TaskGUI(ctk.CTk):
    """
    Class for the main GUI window.
    Creates a sidebar and main panel to display and manage tasks.
    """
    def __init__(self, task_manager: TaskManager):
        """
        Init method.
        Sets up the main window, sidebar, and task display area.
        """
        super().__init__()
        self.task_manager = task_manager
        self.title("Task Manager")
        self.geometry("900x600")
        self.minsize(800, 500)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Sidebar frame for buttons and controls
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nswe")
        self.sidebar_frame.grid_rowconfigure(5, weight=1)

        # Button to add new tasks
        self.add_task_button = ctk.CTkButton(self.sidebar_frame, text="Add Task", command=self.open_add_task_modal)
        self.add_task_button.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")
        
        # Refresh button to reload tasks
        self.refresh_button = ctk.CTkButton(self.sidebar_frame, text="Refresh", command=self.display_tasks)
        self.refresh_button.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        
        # Export tasks button
        self.export_button = ctk.CTkButton(self.sidebar_frame, text="Export Tasks", command=self.export_tasks)
        self.export_button.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
        
        # Switch to show/hide completed tasks
        self.show_completed_var = ctk.BooleanVar(value=False)
        self.show_completed_switch = ctk.CTkSwitch(self.sidebar_frame, text="Show Completed", variable=self.show_completed_var, command=self.toggle_completed)
        self.show_completed_switch.grid(row=3, column=0, padx=20, pady=10, sticky="ew")
        
        # Search entry to filter tasks
        self.search_entry = ctk.CTkEntry(self.sidebar_frame, placeholder_text="Search tasks...")
        self.search_entry.grid(row=4, column=0, padx=20, pady=10, sticky="ew")
        self.search_entry.bind("<Return>", self.search_tasks)
        
        # Switch to disable colors in the task list
        self.disable_colors_switch = ctk.CTkSwitch(self.sidebar_frame, text="Disable Colors", command=self.toggle_disable_colors)
        self.disable_colors_switch.grid(row=6, column=0, padx=20, pady=(10, 0), sticky="ew")
        self.disable_colors_switch.deselect()
        
        # Legend frame to explain color meanings
        self.legend_frame = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent", corner_radius=0)
        self.legend_frame.grid(row=7, column=0, padx=20, pady=(10, 20), sticky="w")
        self.red_legend_label = ctk.CTkLabel(self.legend_frame, text="Red: Overdue", anchor="w")
        self.red_legend_label.pack(anchor="w")
        self.orange_legend_label = ctk.CTkLabel(self.legend_frame, text="Orange: Due in 30 days", anchor="w")
        self.orange_legend_label.pack(anchor="w")
        self.blue_legend_label = ctk.CTkLabel(self.legend_frame, text="Blue: Due in >30 days", anchor="w")
        self.blue_legend_label.pack(anchor="w")
        self.white_legend_label = ctk.CTkLabel(self.legend_frame, text="White: No due date", anchor="w")
        self.white_legend_label.pack(anchor="w")
        self.green_legend_label = ctk.CTkLabel(self.legend_frame, text="Green: Completed", anchor="w")
        self.update_legend()

        # Main panel for displaying tasks
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        # Scrollable frame to list tasks
        self.task_scroll_frame = ctk.CTkScrollableFrame(self.main_frame, label_text="Tasks")
        self.task_scroll_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # Initially display tasks
        self.display_tasks()

        # Save tasks when window is closed
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.after(100, self.update_legend)

    def update_legend(self) -> None:
        """
        Updates the color legend based on current settings.
        Shows/hides the 'green' label depending on if completed tasks are shown.
        """
        color_map = {"red": "#ff073a", "orange": "#ffa500", "blue": "#1E90FF", "white": "#FFFFFF", "green": "#32CD32"}
        text_color = {k: (v if not self.disable_colors_switch.get() else "white") for k, v in color_map.items()}
        self.red_legend_label.configure(text_color=text_color["red"])
        self.orange_legend_label.configure(text_color=text_color["orange"])
        self.blue_legend_label.configure(text_color=text_color["blue"])
        self.white_legend_label.configure(text_color=text_color["white"])
        if self.show_completed_var.get():
            if not self.green_legend_label.winfo_ismapped():
                self.green_legend_label.pack(anchor="w")
            self.green_legend_label.configure(text_color=text_color["green"])
        else:
            if self.green_legend_label.winfo_ismapped():
                self.green_legend_label.pack_forget()

    def toggle_disable_colors(self) -> None:
        """
        Method toggles the disable colors setting and refreshes task list.
        """
        self.display_tasks()
        self.update_legend()

    def display_tasks(self) -> None:
        """
        Refreshes the task list.
        Filters tasks based on search and show completed switch,
        Sorts and displays tasks with proper colors.
        """
        # Clear current task widgets
        for widget in self.task_scroll_frame.winfo_children():
            widget.destroy()
        query = self.search_entry.get().lower()
        tasks_to_display = [t for t in self.task_manager.tasks if not t.deleted and (query in t.description.lower() if query else True)]
        if not self.show_completed_var.get():
            tasks_to_display = [t for t in tasks_to_display if not t.completed]
        tasks_to_display = sort_tasks(tasks_to_display)
        color_map = {"red": "#ff073a", "orange": "#ffa500", "blue": "#1E90FF", "white": "#FFFFFF", "green": "#32CD32"}
        text_color = "white" if self.disable_colors_switch.get() else "black"
        for task in tasks_to_display:
            task_color = get_task_color(task)
            bg_color = None if self.disable_colors_switch.get() else color_map.get(task_color, "#CCCCCC")
            task_frame = ctk.CTkFrame(self.task_scroll_frame, fg_color=bg_color, corner_radius=8)
            task_frame.pack(fill="x", padx=5, pady=5)
            due_str = task.due_date.strftime("%d/%m/%y") if task.due_date else "No due date"
            summary = f"{task.description} | {('Completed' if task.completed else 'Incomplete')} | Due: {due_str} | Priority: {PRIORITY_LEVELS.get(task.priority, 'Unknown')}"
            task_label = ctk.CTkLabel(task_frame, text=summary, anchor="w", text_color=text_color)
            task_label.pack(side="left", padx=10, pady=10, fill="x", expand=True)
            details_button = ctk.CTkButton(task_frame, text="Details", width=80, command=lambda t=task: self.open_task_detail(t))
            details_button.pack(side="right", padx=10, pady=10)

    def search_tasks(self, event) -> None:
        """
        Filters tasks based on search field.
        """
        self.display_tasks()

    def toggle_completed(self) -> None:
        """
        Toggles visibility of completed tasks.
        Updates the switch color and refreshes task list.
        """
        if self.show_completed_var.get():
            self.show_completed_switch.configure(fg_color="#32CD32")
        else:
            self.show_completed_switch.configure(fg_color="gray")
        self.display_tasks()
        self.update_legend()

    def open_task_detail(self, task: Task) -> None:
        """
        Opens a modal window showing details for a task.
        Provides options to mark as complete/ongoing, edit, or delete the task.
        """
        detail_window = ctk.CTkToplevel(self)
        detail_window.title("Task Details")
        detail_window.geometry("400x400")
        detail_window.attributes("-topmost", True)
        detail_window.after(500, lambda: detail_window.attributes("-topmost", False))
        detail_window.lift()
        detail_window.focus_force()
        ctk.CTkLabel(detail_window, text=f"Description: {task.description}").pack(pady=5)
        due_str = task.due_date.strftime("%d/%m/%y") if task.due_date else "No due date"
        ctk.CTkLabel(detail_window, text=f"Due Date: {due_str}").pack(pady=5)
        ctk.CTkLabel(detail_window, text=f"Priority: {PRIORITY_LEVELS.get(task.priority, 'Unknown')}").pack(pady=5)
        ctk.CTkLabel(detail_window, text=f"Additional Info: {task.additional_info or 'None'}").pack(pady=5)
        ctk.CTkLabel(detail_window, text=f"Created: {task.created_date.strftime('%d/%m/%y')}").pack(pady=5)
        ctk.CTkLabel(detail_window, text=f"Status: {'Completed' if task.completed else 'Incomplete'}").pack(pady=5)
        
        def toggle_completion():
            """
            Toggles the task's completion status.
            """
            if not task.completed:
                task.mark_completed()
            else:
                task.completed = False
            self.task_manager.save()
            detail_window.destroy()
            self.display_tasks()
            self.update_legend()
        
        mark_text = "Mark as Ongoing" if task.completed else "Mark Completed"
        ctk.CTkButton(detail_window, text=mark_text, command=toggle_completion).pack(pady=5)
        
        def open_edit():
            """
            Closes the detail window and opens the edit window.
            """
            detail_window.destroy()
            self.open_edit_task_modal(task)
        
        ctk.CTkButton(detail_window, text="Edit Task", command=open_edit).pack(pady=5)
        
        def delete_task():
            """
            Deletes the task after a confirmation.
            """
            if messagebox.askyesno("Delete Task", "Are you sure you want to delete this task?"):
                self.task_manager.tasks.remove(task)
                self.task_manager.save()
                detail_window.destroy()
                self.display_tasks()
                self.update_legend()
        
        ctk.CTkButton(detail_window, text="Delete Task", fg_color="red", command=delete_task).pack(pady=5)
        ctk.CTkButton(detail_window, text="Close", command=detail_window.destroy).pack(pady=5)

    def open_add_task_modal(self) -> None:
        """
        Opens a window to add a new task.
        """
        modal = ctk.CTkToplevel(self)
        modal.title("Add Task")
        modal.geometry("400x400")
        modal.attributes("-topmost", True)
        modal.after(500, lambda: modal.attributes("-topmost", False))
        modal.lift()
        modal.focus_force()
        ctk.CTkLabel(modal, text="Description:").pack(pady=5)
        description_entry = ctk.CTkEntry(modal)
        description_entry.pack(pady=5, fill="x", padx=10)
        ctk.CTkLabel(modal, text="Due Date (DD/MM/YY):").pack(pady=5)
        due_date_entry = ctk.CTkEntry(modal)
        due_date_entry.pack(pady=5, fill="x", padx=10)
        ctk.CTkLabel(modal, text="Priority:").pack(pady=5)
        priority_combobox = ctk.CTkComboBox(modal, values=["Low", "Normal", "High"])
        priority_combobox.set("Normal")
        priority_combobox.pack(pady=5, fill="x", padx=10)
        ctk.CTkLabel(modal, text="Additional Info:").pack(pady=5)
        additional_info_entry = ctk.CTkEntry(modal)
        additional_info_entry.pack(pady=5, fill="x", padx=10)
        
        def submit_task():
            """
            Validates input and adds the new task.
            """
            description = description_entry.get().strip()
            if not description:
                messagebox.showerror("Error", "Description cannot be empty!")
                return
            due_date_str = due_date_entry.get().strip()
            due_date = None
            if due_date_str:
                try:
                    due_date = datetime.strptime(due_date_str, "%d/%m/%y")
                except ValueError:
                    messagebox.showerror("Error", "Invalid due date format! Use DD/MM/YY")
                    return
            priority_text = priority_combobox.get()
            reverse_priority = {"Low": 1, "Normal": 2, "High": 3}
            priority_value = reverse_priority.get(priority_text, 2)
            additional_info = additional_info_entry.get().strip()
            new_task = Task(
                description=description,
                completed=False,
                due_date=due_date,
                priority=priority_value,
                additional_info=additional_info if additional_info else None
            )
            self.task_manager.tasks.append(new_task)
            self.task_manager.save()
            modal.destroy()
            self.display_tasks()
            self.update_legend()
        
        ctk.CTkButton(modal, text="Add Task", command=submit_task).pack(pady=10)

    def open_edit_task_modal(self, task: Task) -> None:
        """
        Opens a window to edit an existing task.
        """
        modal = ctk.CTkToplevel(self)
        modal.title("Edit Task")
        modal.geometry("400x400")
        modal.attributes("-topmost", True)
        modal.after(500, lambda: modal.attributes("-topmost", False))
        modal.lift()
        modal.focus_force()
        ctk.CTkLabel(modal, text="Description:").pack(pady=5)
        description_entry = ctk.CTkEntry(modal)
        description_entry.insert(0, task.description)
        description_entry.pack(pady=5, fill="x", padx=10)
        ctk.CTkLabel(modal, text="Due Date (DD/MM/YY):").pack(pady=5)
        due_date_entry = ctk.CTkEntry(modal)
        if task.due_date:
            due_date_entry.insert(0, task.due_date.strftime("%d/%m/%y"))
        due_date_entry.pack(pady=5, fill="x", padx=10)
        ctk.CTkLabel(modal, text="Priority:").pack(pady=5)
        priority_combobox = ctk.CTkComboBox(modal, values=["Low", "Normal", "High"])
        current_priority = PRIORITY_LEVELS.get(task.priority, "Normal")
        priority_combobox.set(current_priority)
        priority_combobox.pack(pady=5, fill="x", padx=10)
        ctk.CTkLabel(modal, text="Additional Info:").pack(pady=5)
        additional_info_entry = ctk.CTkEntry(modal)
        if task.additional_info:
            additional_info_entry.insert(0, task.additional_info)
        additional_info_entry.pack(pady=5, fill="x", padx=10)
        
        def submit_edit():
            """
            Saves the changes made to the task.
            """
            new_description = description_entry.get().strip()
            if not new_description:
                messagebox.showerror("Error", "Description cannot be empty!")
                return
            task.description = new_description
            due_date_str = due_date_entry.get().strip()
            if due_date_str:
                try:
                    task.due_date = datetime.strptime(due_date_str, "%d/%m/%y")
                except ValueError:
                    messagebox.showerror("Error", "Invalid due date format! Use DD/MM/YY")
                    return
            else:
                task.due_date = None
            priority_text = priority_combobox.get()
            reverse_priority = {"Low": 1, "Normal": 2, "High": 3}
            task.priority = reverse_priority.get(priority_text, 2)
            additional_info = additional_info_entry.get().strip()
            task.additional_info = additional_info if additional_info else None
            self.task_manager.save()
            modal.destroy()
            self.display_tasks()
            self.update_legend()
        
        ctk.CTkButton(modal, text="Save Changes", command=submit_edit).pack(pady=10)

    def export_tasks(self) -> None:
        """
        Exports incomplete tasks to a .txt in current directory.
        """
        export_path = Path.cwd() / "tasks_export.txt"
        export_tasks_to_txt(self.task_manager.tasks, export_path)
        messagebox.showinfo("Export", f"Tasks exported to {export_path}!")

    def on_close(self) -> None:
        """
        Saves tasks and closes the app.
        """
        self.task_manager.save()
        self.destroy()
