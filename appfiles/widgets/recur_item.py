"""Yo!"""

# import random as rng
# from datetime import date
# from typing import Callable
import customtkinter as ctk #type: ignore

# from appfiles.widgets.twois_detail import TWOISDetailButton, TWOISDetailFrame
from appfiles.library.recurringtask import RecurringTask
# from appfiles.library.workorder import WorkOrder
# from appfiles.library.taskitem import TaskItem

class RecurringTaskPanel(ctk.CTkFrame):
    """Yo!"""
    def __init__(self, master: ctk.CTk | ctk.CTkToplevel | ctk.CTkFrame, task: RecurringTask):
        super().__init__(master=master, fg_color=("gray80", "gray21"))
        self.task: RecurringTask = task
        self.bvar: ctk.BooleanVar = ctk.BooleanVar(self, False)
        xpos: int = 0
        checkbox: ctk.CTkCheckBox = ctk.CTkCheckBox(self, variable=self.bvar, text=str(self.task))
        checkbox.grid(row=0, column=0, padx=20, pady=10, sticky='w')
        xpos += 1

        self.grid_columnconfigure(1, weight=1)

        date_lbl: ctk.CTkLabel = ctk.CTkLabel(self, text=f"Next due date: {str(self.task.due_date)}",
                                              anchor='e', justify='right')
        date_lbl.grid(row=0, column=2, padx=20, pady=10, sticky='e')
        xpos += 1

        # recur_txt: str = f"Recurs every {self.task.recur} day"
        # if self.task.recur > 1:
        #     recur_txt += "s"
        # recur_lbl: ctk.CTkLabel = ctk.CTkLabel(self, text=recur_txt,
        #                                       anchor='w', justify='left')
        # recur_lbl.grid(row=0, column=xpos, padx=20, pady=20)
        # xpos += 1




    def is_checked(self) -> bool:
        """A method which returns True or False depending on whether its checkbox is checked."""
        return self.bvar.get()
