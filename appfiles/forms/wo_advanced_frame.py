"""Yo!"""

from typing import Callable
import customtkinter as ctk #type:ignore

from appfiles.library.taskitem import TaskItem
from appfiles.library.workorder import SAFETY_TASK
from appfiles.library.workorderform_dict import WorkOrderFormDict
from appfiles.widgets.task_entry import TaskEntry


class WorkOrderAdvancedFrame(ctk.CTkFrame):
    """Yo!"""
    def __init__(self, master: ctk.CTk | ctk.CTkToplevel | ctk.CTkFrame,
                 vardict: WorkOrderFormDict):
        super().__init__(master=master)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.task_count = 2
        self.__pack_task_frame(vardict)
        self.__pack_checkbox_frame(vardict)
        self.__pack_entry_frame(vardict)
        self.vardict: WorkOrderFormDict = vardict



    def __pack_task_frame(self, vardict = WorkOrderFormDict) -> None:
        taskframe: ctk.CTkFrame = ctk.CTkFrame(self)
        taskframe.grid_columnconfigure(1, weight=1)
        taskframe.grid_rowconfigure(0, weight=1)
        addbtn: ctk.CTkButton = ctk.CTkButton(taskframe, width=28, text="+",
                                                   font=ctk.CTkFont("Courier New", 20, "bold"),
                                                   command=self.add_button)

        self.taskitemframe: ctk.CTkScrollableFrame = ctk.CTkScrollableFrame(taskframe)

        self.taskentries: list[TaskEntry] = []

        has_safety_message: bool = False
        for task in vardict['task_list']:
            self.taskentries.append(TaskEntry(self.taskitemframe, task.number, task))
            if task.summary == "Safety Message":
                has_safety_message = True

        if not has_safety_message:
            self.taskentries.insert(0, TaskEntry(self.taskitemframe, 0, SAFETY_TASK))

        if len(self.taskentries) == 1:
            self.taskentries.append(TaskEntry(self.taskitemframe, 10))

        self.taskentries[0].summary_entry.configure(state=ctk.DISABLED)
        self.taskentries[0].reference_entry.configure(state=ctk.DISABLED)
        self.taskentries[0].del_btn.grid_forget()
        self.taskentries[1].del_btn.grid_forget()

        addbtn.grid(row=0, column=0, padx=(20,10), pady=20, sticky='w')
        self.taskitemframe.grid(row=0, column=1, rowspan=8, padx=(0,20), pady=20, sticky='nsew')
        for i, task in enumerate(self.taskentries):
            task.grid(row=i, column=0, padx=10, pady=10, sticky='ew')

        taskframe.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')



    def __pack_checkbox_frame(self, vardict = WorkOrderFormDict) -> None:
        checkboxframe: ctk.CTkFrame = ctk.CTkFrame(self)
        list_of_boxes: dict = {
            "task_lead_required":"Task Lead Required",
            "tech_witness_point":"Tech Witness Point",
            "peer_review_required":"Peer Review Required",
            "peer_review_attached":"Peer Review Attached",
            "ehs_required":"EHS Required",
            "qamip":"QAMIP",
            "qa_review_required":"QA Review Required"}
        i: int = 1
        for dict_key, text_string in list_of_boxes.items():
            self.__create_checkbox(checkboxframe, text_string, i, vardict[dict_key])
            i += 1
        checkboxframe.grid(row=0, column=1, padx=10, pady=10, sticky='nsew')
        checkboxframe.grid_rowconfigure((0, 8), weight=1)



    def __pack_entry_frame(self, vardict: WorkOrderFormDict) -> None:
        entryframe: ctk.CTkFrame = ctk.CTkFrame(self)
        entryframe.grid_columnconfigure((0, 4), weight=1)
        ncr_ckbx: ctk.CTkCheckBox = ctk.CTkCheckBox(entryframe, text="NCR Required",
                                                variable=vardict['ncr_required'],
                                                command=self.__ncr_required_check)
        ncr_ckbx.grid(row=0, rowspan=2, column=1, padx=10, pady=10, sticky='w')
        ncr_no_lbl: ctk.CTkLabel = ctk.CTkLabel(entryframe, text="NCR Number (if applicable):",
                                               justify='left', anchor='n')
        ncr_no_lbl.grid(row=0, column=2, padx=20, pady=(10,0), sticky='ew')
        self.ncr_no: ctk.CTkEntry = ctk.CTkEntry(entryframe, textvariable=vardict['ncr_number'],
                                                 state='disabled')
        self.ncr_no.grid(row=1, column=2, padx=20, pady=(0,10), sticky='ew')

        rel_wo_lbl: ctk.CTkLabel = ctk.CTkLabel(entryframe, text="Related Workorder Number:",
                                               justify='left', anchor='n')
        rel_wo_lbl.grid(row=0, column=3, padx=20, pady=(10,0), sticky='ew')
        rel_wo: ctk.CTkEntry = ctk.CTkEntry(entryframe, textvariable=vardict['related_wo'])
        rel_wo.grid(row=1, column=3, padx=80, pady=(0,10), sticky='ew')

        entryframe.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky='nsew')




    def add_button(self) -> None:
        """Yo!"""
        new_entry = TaskEntry(self.taskitemframe, len(self.taskentries) * 10)
        new_entry.set_lambda(self.__delete_button_get_lambda(new_entry))
        new_entry.grid(row=len(self.taskentries), column=0, padx=10, pady=10, sticky='ew')
        self.taskentries.append(new_entry)



    def __delete_button_get_lambda(self, entry: TaskEntry) -> Callable:
        return lambda ev:self.del_button(entry)



    def del_button(self, entry: TaskEntry) -> None:
        """Yo!"""
        found: bool = False
        for task in self.taskentries:
            if task.taskno == entry.taskno:
                found = True
                task.grid_forget()
                continue
            if found:
                task.taskno -= 10
                task.grid_forget()
                task.taskno_label.configure(text=f"Task number {str(task.taskno).ljust(2, '0')}")
                task.grid(row=int(task.taskno/10), column=0, padx=10, pady=10, sticky='ew')
        self.taskentries.remove(entry)



    def convert_to_taskitems(self) -> list[TaskItem]:
        """Yo!"""
        resp: list[TaskItem] = []
        for i, frame in enumerate(self.taskentries):
            if i == 0:
                resp.append(SAFETY_TASK)
                continue
            number: int = i*10
            summary: str = frame.summary_entry.get()
            reference: str = frame.reference_entry.get()
            row: int = i + 15
            item = TaskItem(number, summary, reference, row)
            resp.append(item)
        return resp



    def __create_checkbox(self, master, text: str, row: int,
                          var: ctk.BooleanVar) -> ctk.CTkCheckBox:
        resp: ctk.CTkCheckBox = ctk.CTkCheckBox(master=master, text=text,
                                                variable=var)
        resp.grid(row=row, column=0, padx=(10,20), pady=10, sticky='nsew')


    def __ncr_required_check(self) -> bool:
        if self.vardict['ncr_required'].get():
            self.ncr_no.configure(state='normal')
        else:
            self.vardict['ncr_number'].set("N/A")
            self.ncr_no.configure(state='readonly')
