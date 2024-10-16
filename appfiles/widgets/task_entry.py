
import os
from typing import Callable
import customtkinter as ctk     #type: ignore
from PIL import Image
from appfiles.library.taskitem import TaskItem


class TaskEntry(ctk.CTkFrame):
    def __init__(self, master: ctk.CTk | ctk.CTkToplevel | ctk.CTkFrame, taskno: int, task: TaskItem = TaskItem(-1, "", "", -1)):
        super().__init__(master)
        self.taskno = taskno
        del_image: Image = Image.open(os.path.join(os.getcwd(), "appfiles\\res\\del_icon.png"))
        del_icon: ctk.CTkImage = ctk.CTkImage(dark_image=del_image, size=(24,24))
        del_icon.configure()
        self.taskno_label: ctk.CTkLabel = ctk.CTkLabel(self, text=f"Task number {str(taskno).ljust(2, '0')}", width=100)
        self.summary_entry: ctk.CTkEntry = ctk.CTkEntry(self, placeholder_text="Task Summary")
        self.reference_entry: ctk.CTkEntry = ctk.CTkEntry(self, placeholder_text="Reference Document")
        self.del_btn: ctk.CTkButton = ctk.CTkButton(self, text="X", width=28, font=ctk.CTkFont("Courier New", 20, "bold"))

        if task.number > -1:
            self.summary_entry.insert(0, task.summary)
            self.reference_entry.insert(0, task.reference)
        
        self.taskno_label.grid(row=0,column=0, padx=10, pady=5, sticky='w')
        self.summary_entry.grid(row=0,column=1, padx=10, pady=5, sticky='w')
        self.reference_entry.grid(row=0,column=2, padx=10, pady=5, sticky='w')
        self.del_btn.grid(row=0,column=3, padx=10, pady=5, sticky='w')


    def to_taskitem(self) -> TaskItem:
        return TaskItem(
            task_number=self.taskno,
            summary=self.summary_entry.get(),
            ref=self.reference_entry.get(),
            row=int(self.taskno/10)+15
        )
    

    def set_lambda(self, delete_function: Callable) -> None:
        self.del_btn.bind("<Button-1>", delete_function)
