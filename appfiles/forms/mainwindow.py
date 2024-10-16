"""This file defines the MainWindow class which serves as the application's primary window."""

import customtkinter as ctk #type: ignore

from appfiles.forms.config_frame import ConfigurationFrame
from appfiles.forms.status_frame import TWOISStatusFrame
from appfiles.forms.recur_frame import RecurringTaskFrame
from appfiles.forms.workorder_form import WorkOrderForm, WorkOrderFormMode

WIN_W: int = 1100
WIN_H: int = 600
STAT_TAB: str = "TWOIS Status"
RECUR_TAB: str = "Recurring Tasks"
CFG_TAB: str = "Configuration"
BTN_W: int = 175

class MainWindow(ctk.CTk):
    """Class which defines the primary window of the TWOIS Management App. It only houses more
    useful widgets."""
    def __init__(self):
        super().__init__()

        # configure window
        self.title("TWOIS Manager")
        self.geometry(f"{WIN_W}x{WIN_H}")
        self.resizable(False, False)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.sidebar: ctk.CTkFrame = self.__populate_sidebar_frame()
        self.tabview: ctk.CTkTabview = ctk.CTkTabview(self)

        self.tabview.add(STAT_TAB)
        self.tabview.tab(STAT_TAB).grid_columnconfigure(0, weight=1)
        self.tabview.tab(STAT_TAB).grid_rowconfigure(0, weight=1)
        self.twois_status: TWOISStatusFrame = TWOISStatusFrame(self.tabview.tab(STAT_TAB))

        self.tabview.add(RECUR_TAB)
        self.tabview.tab(RECUR_TAB).grid_columnconfigure(0, weight=1)
        self.tabview.tab(RECUR_TAB).grid_rowconfigure(0, weight=1)
        self.recurring_tasks: RecurringTaskFrame = RecurringTaskFrame(self.tabview.tab(RECUR_TAB))

        self.tabview.add(CFG_TAB)
        self.tabview.tab(CFG_TAB).grid_columnconfigure(0, weight=1)
        self.tabview.tab(CFG_TAB).grid_rowconfigure(0, weight=1)
        self.config_frame: ConfigurationFrame = ConfigurationFrame(self.tabview.tab(CFG_TAB))

        self.sidebar.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.tabview.grid(row=0, column=1, padx=(20, 20), pady=(20, 20), sticky="nsew")
        self.twois_status.grid(row=0, column=0, rowspan=4, padx=20, pady=10, sticky="nsew")
        self.recurring_tasks.grid(row=0, column=0, rowspan=4, padx=20, pady=10, sticky="nsew")
        self.config_frame.grid(row=0, column=0, rowspan=4, padx=20, pady=10, sticky="nsew")


    def __sidebar_button_event(self): ##BCOBB: DELETE THIS METHOD
        print("BCOBB: FINISH YOUR FUCKING JOB BRO")


    def launch_new_workorder_window(self):
        """Method is used to launch a new Work Order form."""
        WorkOrderForm(self, WorkOrderFormMode.NEW)


    def launch_new_workorder_template_window(self):
        """Method is used to launch a new Work Order form."""
        WorkOrderForm(self, WorkOrderFormMode.TEMPLATE)


    def refresh_app(self) -> None:
        """A method which will forget all of the tabularized windows' placement and reinitialize
        them with new information."""
        self.twois_status.refresh_contents()
        # BCOBB: The other two frames should also refresh


    def __populate_sidebar_frame(self) -> ctk.CTkFrame:
        resp: ctk.CTkFrame = ctk.CTkFrame(self, width=140, corner_radius=0)
        resp.grid_rowconfigure((1,3), weight=1)

        logo_lbl = ctk.CTkLabel(resp, text="TWOIS Manager",
                                  font=ctk.CTkFont(size=20, weight="bold"))

        new_wo_btn = ctk.CTkButton(resp,
                                      command=self.launch_new_workorder_window,
                                      text="Create New TWOIS", width=BTN_W)

        new_template_btn = ctk.CTkButton(resp,
                                         command=self.launch_new_workorder_template_window,
                                         text="Create TWOIS Template", width=BTN_W)

        # BCOBB: Could I leverage the "Approve Workorder" method used elsewhere?
        load_wo_btn = ctk.CTkButton(resp,
                                       command=self.__sidebar_button_event,
                                       text="Load Approved TWOIS", width=BTN_W)

        load_wo_template_btn = ctk.CTkButton(resp,
                                                command=self.__sidebar_button_event,
                                                text="Load TWOIS from Template", width=BTN_W)

        refresh_btn = ctk.CTkButton(resp,
                                    command=self.refresh_app,
                                    text="Refresh App", width=BTN_W)

        logo_lbl.grid(row=0, column=0, padx=20, pady=(20, 10))
        new_wo_btn.grid(row=5, column=0, padx=10, pady=10)
        new_template_btn.grid(row=6, column=0, padx=20, pady=10)
        load_wo_btn.grid(row=7, column=0, padx=20, pady=10)
        load_wo_template_btn.grid(row=8, column=0, padx=20, pady=10)
        refresh_btn.grid(row=9, column=0, padx=10, pady=(30,20))

        return resp
