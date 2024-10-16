"""Yo!"""

from datetime import date

import customtkinter as ctk     #type: ignore
from appfiles.library.completiondata import TaskCompletionData, WorkorderCompletionData
from appfiles.library.logcomment import LogComment
from appfiles.library.workorder import WorkOrder
from appfiles.utils.appglobals import primary_user
from appfiles.utils.utils import date_to_string, string_to_date
from appfiles.widgets.task_completion import TaskCompletionFrame



class CompletionForm(ctk.CTkToplevel):
    """A new window which will manage the creation or modification of workorder objects."""
    def __init__(self, master: ctk.CTk | ctk.CTkToplevel | ctk.CTkFrame,
                 workorder: WorkOrder = WorkOrder()):
        super().__init__(master=master)
        self.title(f"Complete TWOIS# {workorder.get_full_workorder_number()}")
        self.geometry("800x500")
        self.resizable(False, False)
        self.grid_columnconfigure((0,1,2,3), weight=1)
        self.grid_rowconfigure(2, weight=1)

        self.workorder: WorkOrder = workorder
        self.newcomments: list[LogComment] = []

        startdatelbl: ctk.CTkLabel = ctk.CTkLabel(self, anchor='w',text="Start Date")
        startdatelbl.grid(row=0, column=0, padx=35, pady=(20, 0), sticky='ew')
        self.startdateentry: ctk.CTkEntry = ctk.CTkEntry(self)
        self.startdateentry.insert(0, date_to_string(date.today()))
        self.startdateentry.grid(row=1, column=0, padx=35, pady=(0, 20), sticky='ew')

        enddatelbl: ctk.CTkLabel = ctk.CTkLabel(self, anchor='w', text="End Date")
        enddatelbl.grid(row=0, column=1, padx=35, pady=(20, 0), sticky='ew')
        self.enddateentry: ctk.CTkEntry = ctk.CTkEntry(self)
        self.enddateentry.insert(0, date_to_string(date.today()))
        self.enddateentry.grid(row=1, column=1, padx=35, pady=(0, 20), sticky='ew')

        restoredatelbl: ctk.CTkLabel = ctk.CTkLabel(self, anchor='w', text="Restoration Date")
        restoredatelbl.grid(row=0, column=2, padx=35, pady=(20, 0), sticky='ew')
        self.restoredateentry: ctk.CTkEntry = ctk.CTkEntry(self)
        self.restoredateentry.insert(0, date_to_string(date.today()))
        self.restoredateentry.grid(row=1, column=2, padx=35, pady=(0, 20), sticky='ew')

        repairtimelbl: ctk.CTkLabel = ctk.CTkLabel(self, anchor='w', text="Repair Time")
        repairtimelbl.grid(row=0, column=3, padx=35, pady=(20, 0), sticky='ew')
        self.repairtimeentry: ctk.CTkEntry = ctk.CTkEntry(self, placeholder_text="HH:MM")
        # self.repairtimeentry.insert(0, date_to_string(repairtime.today()))
        self.repairtimeentry.grid(row=1, column=3, padx=35, pady=(0, 20), sticky='ew')

        self.taskframe: TaskCompletionFrame = TaskCompletionFrame(self, workorder)
        self.taskframe.grid(row=2, column=0, columnspan=4, padx=20, pady=0, sticky='nsew')

        btnframe: ctk.CTkFrame = ctk.CTkFrame(self)
        btnframe.grid_columnconfigure((0,4), weight=1)
        btnframe.grid(row=3, column=0, columnspan=4, padx=20, pady=20, sticky='ew')

        self.submit_btn: ctk.CTkButton = ctk.CTkButton(btnframe, text="Submit",
                                                       width=80, command=self.__submit)
        self.submit_btn.grid(row=0, column=1, padx=60, pady=20)

        self.addlogs_btn: ctk.CTkButton = ctk.CTkButton(btnframe, text="Add Log Comments",
                                                        width=150, command=self.__add_comment)
        self.addlogs_btn.grid(row=0, column=2, padx=20, pady=20)

        self.cancel_btn: ctk.CTkButton = ctk.CTkButton(btnframe, text="Cancel",
                                                       width=80, command=self.__cancel)
        self.cancel_btn.grid(row=0, column=3, padx=60, pady=20)


    def __add_comment(self) -> None:
        box = ctk.CTkInputDialog(text="Enter the new log comment text:", title="Add Log Comment")
        box.geometry("400x200")
        inval = box.get_input()
        if inval is None:
            return

        lsize = len(self.newcomments) + len(self.workorder.comments)
        self.newcomments.append(LogComment(inval, primary_user.name, date.today(), lsize))
        print(self.newcomments)


    def __cancel(self) -> None:
        self.destroy()


    def __submit(self) -> None:
        if not self.__inputs_are_valid():
            return
        wo = self.workorder
        taskcomp_datalist: list[TaskCompletionData] = []
        for widget in self.taskframe.taskwidgets:
            comp_data = widget.get_data()
            if comp_data is None:
                return
            taskcomp_datalist.append(comp_data)
        if len(taskcomp_datalist) != len(wo.task_list):
            return
        for i, task in enumerate(wo.task_list):
            task.complete(taskcomp_datalist[i])
        wo.log_comment(self.newcomments)
        wo_comp_data: WorkorderCompletionData = WorkorderCompletionData(
            string_to_date(self.startdateentry.get()),
            string_to_date(self.enddateentry.get()),
            string_to_date(self.restoredateentry.get()),
            self.repairtimeentry.get())
        if not wo.complete(wo_comp_data):
            return
        self.destroy()


    def __inputs_are_valid(self) -> bool:
        print("BCOBB: DO THE INPUT VALIDATION ON THE COMPLETION FORM!")
        return True
