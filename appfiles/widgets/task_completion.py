"""Yo!"""

from datetime import date
import customtkinter as ctk #type: ignore

from appfiles.library.completiondata import TaskCompletionData
from appfiles.library.taskitem import TaskItem
from appfiles.library.workorder import WorkOrder
from appfiles.utils.appglobals import people
from appfiles.utils.utils import date_to_string, string_to_date



class TaskCompletionFrame(ctk.CTkScrollableFrame):
    """Yo!"""
    def __init__(self, master, workorder: WorkOrder):
        super().__init__(master=master)
        self.workorder = workorder
        self.taskwidgets: list[TaskCompletionWidget] = []
        for i, task in enumerate(self.workorder.task_list):
            twid: TaskCompletionWidget = TaskCompletionWidget(self, task)
            twid.grid(row=i, column=0, padx=10, pady=5, sticky='ew')
            self.taskwidgets.append(twid)



class TaskCompletionWidget(ctk.CTkFrame):
    """Yo!"""
    def __init__(self, master, task: TaskItem):
        super().__init__(master=master)
        self.task = task
        self.grid_columnconfigure(0, weight=1)
        taskno_str: str = f"Task {str(self.task.number).ljust(2,'0')}"
        tasknolbl: ctk.CTkLabel = ctk.CTkLabel(self, anchor='w', text=taskno_str)
        tasknolbl.grid(row=0, column=0, padx=10, pady=(10, 0), sticky='w')
        tasklbl: ctk.CTkLabel = ctk.CTkLabel(self, anchor='w', text=self.task.summary, width=150)
        tasklbl.grid(row=1, column=0, padx=10, pady=(0, 10), sticky='w')

        datelbl: ctk.CTkLabel = ctk.CTkLabel(self, text="Completion Date")
        datelbl.grid(row=0, column=1, padx=10, pady=(10, 0), sticky='w')
        self.dateentry: ctk.CTkEntry = ctk.CTkEntry(self)
        self.dateentry.insert(0, date_to_string(date.today()))
        self.dateentry.grid(row=1, column=1, padx=10, pady=(0, 10), sticky='w')

        techlbl: ctk.CTkLabel = ctk.CTkLabel(self, text="Technician")
        techlbl.grid(row=0, column=2, padx=10, pady=(10, 0), sticky='w')
        self.techentry: ctk.CTkOptionMenu = ctk.CTkOptionMenu(self,
                                                              values=[p.name for p in people])
        self.techentry.set(people[0].name)
        self.techentry.grid(row=1, column=2, padx=10, pady=(0, 10), sticky='w')

        techqtylbl: ctk.CTkLabel = ctk.CTkLabel(self, text="Qty. Techs")
        techqtylbl.grid(row=0, column=3, padx=10, pady=(10, 0), sticky='w')
        self.techqtyentry: ctk.CTkEntry = ctk.CTkEntry(self, width=75)
        self.techqtyentry.insert(0, "1")
        self.techqtyentry.grid(row=1, column=3, padx=10, pady=(0, 10), sticky='w')

        hourslbl: ctk.CTkLabel = ctk.CTkLabel(self, text="Hours")
        hourslbl.grid(row=0, column=4, padx=10, pady=(10, 0), sticky='w')
        self.hoursentry: ctk.CTkEntry = ctk.CTkEntry(self, width=75)
        self.hoursentry.insert(0, "0.1")
        self.hoursentry.grid(row=1, column=4, padx=10, pady=(0, 10), sticky='w')


    def get_data(self) -> TaskCompletionData | None:
        """Yo!"""
        if not self.__inputs_are_valid():
            return None
        cdate: date = string_to_date(self.dateentry.get())
        tech: str = self.techentry.get()
        techqty: int = int(self.techqtyentry.get())
        hours: float = float(self.hoursentry.get())
        return TaskCompletionData(cdate, tech, techqty, hours)


    def __inputs_are_valid(self) -> bool:
        print("BCOBB: DO INPUT VALIDATION ON TASK COMPLETION DATA CLASS")
        return True
