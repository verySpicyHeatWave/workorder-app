"""Yo!"""

from datetime import date, timedelta
from enum import Enum
from tkinter import messagebox
import customtkinter as ctk     #type: ignore
from appfiles.forms.wo_advanced_frame import WorkOrderAdvancedFrame
from appfiles.forms.wo_general_frame import WorkOrderGeneralFrame
from appfiles.library.site import Site
from appfiles.library.special import Special
from appfiles.library.workorder import WorkOrder, SAFETY_TASK
from appfiles.library.workorder_dict import WorkOrderDict
from appfiles.library.workorder_type import WorkOrderType
from appfiles.library.workorderform_dict import WorkOrderFormDict
from appfiles.utils.appglobals import default_building, default_room, primary_user
from appfiles.utils.appglobals import default_site, default_special, default_wotype
from appfiles.utils.utils import date_to_string, is_a_valid_date_string, string_to_date
from appfiles.utils.workorder import is_a_valid_ncr_number

GENERAL: str = "General Details"
DETAILS: str = "Details"
ADVANCED: str = "Advanced Options"


class WorkOrderFormMode(Enum):
    """Yo!"""
    NEW = 0
    EDIT = 1
    TEMPLATE = 2
    RECURRING = 3


class WorkOrderForm(ctk.CTkToplevel):
    """A new window which will manage the creation or modification of workorder objects."""
    def __init__(self, master: ctk.CTk | ctk.CTkToplevel | ctk.CTkFrame,
                 mode: WorkOrderFormMode = WorkOrderFormMode.NEW,
                 workorder: WorkOrder = WorkOrder()):
        ##BCOBB: Feed this a string: 'new', 'edit', 'template', or 'recurring'. Also feed it an optional workorder.
        super().__init__(master=master)
        self.vardict: WorkOrderFormDict = self.__load_dict_defaults()
        self.mode: WorkOrderFormMode = mode
        self.wo_for_edit = workorder
        if self.mode == WorkOrderFormMode.EDIT:
            self.vardict = self.__load_dict_from_wo_to_edit()
        self.geometry("900x620")
        self.resizable(False, False)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.tabview = ctk.CTkTabview(self)

        self.tabview.grid(row=0, column=0, padx=20, pady=(20,0), sticky='nsew')
        self.tabview.add(GENERAL)
        self.tabview.tab(GENERAL).grid_columnconfigure(0, weight=1)
        self.tabview.tab(GENERAL).grid_rowconfigure(0, weight=1)
        self.general_frame: WorkOrderGeneralFrame = WorkOrderGeneralFrame(
            self.tabview.tab(GENERAL), self.vardict)
        self.general_frame.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

        self.tabview.add(ADVANCED)
        self.tabview.tab(ADVANCED).grid_columnconfigure(0, weight=1)
        self.tabview.tab(ADVANCED).grid_rowconfigure(0, weight=1)
        self.advanced_frame: WorkOrderAdvancedFrame = WorkOrderAdvancedFrame(
            self.tabview.tab(ADVANCED), self.vardict)
        self.advanced_frame.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

        self.btnframe: ctk.CTkFrame = self.__create_buttonframe()
        self.btnframe.grid(row=1, column=0,  padx=(20, 20), pady=(0, 20), sticky='nsew')

        match self.mode:
            case WorkOrderFormMode.NEW:
                self.title("Generate New Work Order")
            case WorkOrderFormMode.EDIT:
                self.title("Edit Work Order: " + self.wo_for_edit.get_full_workorder_number())
                self.vardict = self.__load_dict_from_wo_to_edit()
                self.general_frame.title_entry.insert(0, self.wo_for_edit.title)
                self.general_frame.title_entry.configure(state='disabled')
                self.general_frame.date_entry.insert(0, date_to_string(self.wo_for_edit.due_date))
                self.general_frame.descrip_entry.insert(0.0, self.wo_for_edit.description)
            case WorkOrderFormMode.TEMPLATE:
                self.title("Create Work Order Template")
            case WorkOrderFormMode.RECURRING:
                self.title("Create Recurring Task Work Order")

        # self.grab_set()

    # def __del__(self):


    def __submit_workorder(self) -> None:
        if not self.__inputs_are_valid():
            return

        match self.mode:
            case WorkOrderFormMode.NEW:
                self.get_workorder().save()
            case WorkOrderFormMode.EDIT:
                self.wo_for_edit.edit(**self.__workorder_kwargs())
                self.wo_for_edit.save()
            case WorkOrderFormMode.TEMPLATE:
                #BCOBB: Prompt user to enter a filename?
                self.get_workorder().save_as_wo_template('BCOBB')
            case WorkOrderFormMode.RECURRING:
                self.get_workorder().save()
        self.destroy()


    def __reset_form(self) -> None:
        del self.general_frame
        del self.advanced_frame
        self.vardict = self.__load_dict_defaults()
        self.general_frame: WorkOrderGeneralFrame = WorkOrderGeneralFrame(
            self.tabview.tab(GENERAL), self.vardict)
        self.general_frame.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

        self.advanced_frame: WorkOrderAdvancedFrame = WorkOrderAdvancedFrame(
            self.tabview.tab(ADVANCED), self.vardict)
        self.advanced_frame.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')


    def __inputs_are_valid(self) -> bool:
        in_str: str = self.general_frame.title_entry.get()
        e_title: str = "Bad Title Length"
        e_message: str = "The work order title must be between 15 and 60 characters."
        if len(in_str) < 15 or len(in_str) > WorkOrder.MAX_TITLE:
            messagebox.showerror(e_title, e_message)
            return False

        in_str = self.general_frame.date_entry.get()
        e_title = "Malformed Date Input"
        e_message = ("You must enter a valid Planned Execution Date in the pattern MM/DD/YYYY "
                     "and the date must be from 14 days in the past to 500 days in the future.")
        if not is_a_valid_date_string(in_str):
            messagebox.showerror(e_title, e_message)
            return False
        ds: list[str] = in_str.split('/')
        try:
            d: date = date(int(ds[2]), int(ds[0]), int(ds[1]))
            if d < date.today() - timedelta(days=14) or d > date.today() + timedelta(days=500):
                raise ValueError
        except ValueError:
            messagebox.showerror(e_title, e_message)
            return False

        e_title = "Bad Building Number"
        e_message = "Building number must be an integer between 10 and 99,999"
        if not self.vardict["building"].get().isdigit():
            messagebox.showerror(e_title, e_message)
            return False
        in_int: int = int(self.vardict["building"].get())
        if in_int < 10 or in_int > 99_999:
            messagebox.showerror(e_title, e_message)
            return False

        e_title = "Bad Room Number"
        e_message = "Room number must be an integer between 1 and 999"
        if not self.vardict["room"].get().isdigit():
            messagebox.showerror(e_title, e_message)
            return False
        in_int: int = int(self.vardict["room"].get())
        if in_int < 1 or in_int > 999:
            messagebox.showerror(e_title, e_message)
            return False

        tlist = self.advanced_frame.convert_to_taskitems()
        for task in tlist:
            in_str = task.summary
            if in_str == SAFETY_TASK.summary:
                continue
            if in_str == "":
                e_title = "Missing Task Summary: Task " + str(task.number)
                e_message = ("All Task Items beyond Task 0 (Safety Message) must be given a "
                             "summary description, and task 10 is required.")
                messagebox.showerror(e_title, e_message)
                return False
            in_str = task.reference
            if in_str == "":
                e_title = "Missing Task Reference: Task " + str(task.number)
                e_message = ("All Task Items beyond Task 0 (Safety Message) must reference a "
                             "document, and task 10 is required.")
                messagebox.showerror(e_title, e_message)
                return False

        in_str = self.vardict['ncr_number'].get()
        e_title = "NCR Number Required"
        e_message = ("If the NCR Required checkbox is checked then you must "
                     "provide a VALID NCR Number (e.g. NCR000000W).")
        if self.vardict['ncr_required'].get() and not is_a_valid_ncr_number(in_str):
            messagebox.showerror(e_title, e_message)
            return False
        return True


    def __cancel(self) -> None:
        self.destroy()


    def __create_buttonframe(self) -> ctk.CTkFrame:
        resp: ctk.CTkFrame = ctk.CTkFrame(self)
        submit_btn: ctk.CTkButton = ctk.CTkButton(resp, text="Submit",
                                                  command=self.__submit_workorder)
        reset_btn: ctk.CTkButton = ctk.CTkButton(resp, text="Reset",
                                                 command=self.__reset_form)
        cancel_btn: ctk.CTkButton = ctk.CTkButton(resp, text="Cancel",
                                                  command=self.__cancel)
        resp.grid_columnconfigure((0,4), weight=1)
        submit_btn.grid(row=0, column=1, padx=20, pady=20)
        reset_btn.grid(row=0, column=2, padx=20, pady=20)
        cancel_btn.grid(row=0, column=3, padx=20, pady=20)
        return resp


    def __load_dict_defaults(self) -> WorkOrderFormDict:
        resp: WorkOrderFormDict = WorkOrderFormDict(
            site=ctk.StringVar(None, default_site.name),
            special=ctk.StringVar(None, default_special.name),
            type=ctk.StringVar(None, default_wotype.name),
            priority=ctk.IntVar(None, 3),
            creator=ctk.StringVar(None, primary_user.name),
            building=ctk.StringVar(None, str(default_building)),
            room=ctk.StringVar(None, str(default_room)),
            related_wo=ctk.StringVar(None, ""),
            pac_required=ctk.BooleanVar(None, False),
            ncr_required=ctk.BooleanVar(None, False),
            ncr_number=ctk.StringVar(None, "N/A"),
            task_lead_required=ctk.BooleanVar(None, False),
            tech_witness_point=ctk.BooleanVar(None, False),
            peer_review_required=ctk.BooleanVar(None, False),
            peer_review_attached=ctk.BooleanVar(None, False),
            ehs_required=ctk.BooleanVar(None, False),
            qamip=ctk.BooleanVar(None, False),
            qa_review_required=ctk.BooleanVar(None, False),
            task_list=[SAFETY_TASK]
        )
        return resp
    

    def __load_dict_from_wo_to_edit(self) -> WorkOrderFormDict:
        resp: WorkOrderFormDict = WorkOrderFormDict(
            site=ctk.StringVar(None, self.wo_for_edit.site.name),
            special=ctk.StringVar(None, self.wo_for_edit.special.name),
            type=ctk.StringVar(None, self.wo_for_edit.type.name),
            priority=ctk.IntVar(None, self.wo_for_edit.priority),
            creator=ctk.StringVar(None, self.wo_for_edit.creator),
            building=ctk.StringVar(None, str(self.wo_for_edit.building)),
            room=ctk.StringVar(None, str(self.wo_for_edit.room)),
            related_wo=ctk.StringVar(None, self.wo_for_edit.related_wo),
            pac_required=ctk.BooleanVar(None, self.wo_for_edit.pac_required),
            ncr_required=ctk.BooleanVar(None, self.wo_for_edit.ncr_required),
            ncr_number=ctk.StringVar(None, self.wo_for_edit.ncr_number),
            task_lead_required=ctk.BooleanVar(None, self.wo_for_edit.task_lead_required),
            tech_witness_point=ctk.BooleanVar(None, self.wo_for_edit.tech_witness_point),
            peer_review_required=ctk.BooleanVar(None, self.wo_for_edit.peer_review_required),
            peer_review_attached=ctk.BooleanVar(None, self.wo_for_edit.peer_review_attached),
            ehs_required=ctk.BooleanVar(None, self.wo_for_edit.ehs_required),
            qamip=ctk.BooleanVar(None, self.wo_for_edit.qamip),
            qa_review_required=ctk.BooleanVar(None, self.wo_for_edit.qa_review_required),
            task_list=self.wo_for_edit.task_list
        )
        return resp
    

    def __workorder_kwargs(self) -> WorkOrderDict:
        wokwargs: WorkOrderDict = WorkOrderDict(
            description=self.general_frame.descrip_entry.get(0.0, ctk.END).strip('\n'),
            due_date=string_to_date(self.general_frame.date_entry.get()),
            wo_number="", # We don't apply work order numbers here, so send blank string
            site=Site.parse(self.vardict["site"].get()),
            special=Special.parse(self.vardict["special"].get()),
            title=self.general_frame.title_entry.get(),
            type=WorkOrderType.parse(self.vardict["type"].get()),
            priority=self.vardict["priority"].get(),
            creator=self.vardict["creator"].get(),
            building=int(self.vardict["building"].get()),
            room=int(self.vardict["room"].get()),
            related_wo=self.vardict["related_wo"].get(),
            pac_required=self.vardict["pac_required"].get(),
            ncr_required=self.vardict["ncr_required"].get(),
            ncr_number=self.vardict["ncr_number"].get(),
            task_lead_required=self.vardict["task_lead_required"].get(),
            tech_witness_point=self.vardict["tech_witness_point"].get(),
            peer_review_required=self.vardict["peer_review_required"].get(),
            peer_review_attached=self.vardict["peer_review_attached"].get(),
            ehs_required=self.vardict["ehs_required"].get(),
            qamip=self.vardict["qamip"].get(),
            qa_review_required=self.vardict["qa_review_required"].get(),
            task_list=self.advanced_frame.convert_to_taskitems()
        )
        return wokwargs


    def get_workorder(self) -> WorkOrder:
        """A method which turns all of the form information into a workorder object
        and returns it.
        """
        wokwargs: WorkOrderDict = self.__workorder_kwargs()
        return WorkOrder(**wokwargs)
