"""Yo!"""

import customtkinter as ctk #type:ignore

from appfiles.library.site import Site
from appfiles.library.special import Special
from appfiles.library.workorder_type import WorkOrderType
from appfiles.library.workorderform_dict import WorkOrderFormDict
from appfiles.utils.appglobals import default_site, default_special, default_wotype


class WorkOrderGeneralFrame(ctk.CTkFrame):
    """Yo!"""
    def __init__(self, master: ctk.CTk | ctk.CTkToplevel | ctk.CTkFrame,
                 vardict: WorkOrderFormDict):
        super().__init__(master=master)
        self.grid_columnconfigure((0,1,2,3), weight=1)
        self.grid_rowconfigure((7), weight=1)

        self.__pack_row_1()
        self.__pack_row_2(vardict)
        self.__pack_row_3(vardict)

        #pack row 4
        descrip_lbl: ctk.CTkLabel = ctk.CTkLabel(self, text="Brief Description of Work (Optional):",
                                               justify='left', anchor='w')
        self.descrip_entry: ctk.CTkTextbox = ctk.CTkTextbox(self)

        descrip_lbl.grid(row=6, column=0, columnspan=5, padx=20, pady=(20,0), sticky='ew')
        self.descrip_entry.grid(row=7, column=0, columnspan=5, padx=20, pady=(0,20), sticky='ew')



    def __pack_row_1(self) -> None:
        placeholder: str = 'Enter a title here, e.g. "14-Day AntiVirus (AV) Update (OPS GMM)"'

        title_lbl: ctk.CTkLabel = ctk.CTkLabel(self, text="Work Order Title:",
                                               justify='left', anchor='w')
        self.title_entry: ctk.CTkEntry = ctk.CTkEntry(self, placeholder_text=placeholder)

        date_lbl: ctk.CTkLabel = ctk.CTkLabel(self, text="Planned Execution Date:",
                                               justify='left', anchor='w')
        self.date_entry: ctk.CTkEntry = ctk.CTkEntry(self, placeholder_text='MM/DD/YYYY')

        title_lbl.grid(row=0, column=0,  columnspan=3, padx=20, pady=(10,0), sticky='ew')
        self.title_entry.grid(row=1, column=0, columnspan=3, padx=20, pady=(0,10), sticky='ew')
        date_lbl.grid(row=0, column=3, padx=20, pady=(10,0), sticky='ew')
        self.date_entry.grid(row=1, column=3, padx=20, pady=(0,10), sticky='ew')



    def __pack_row_2(self, vardict: WorkOrderFormDict) -> None:
        site_lbl: ctk.CTkLabel = ctk.CTkLabel(self, text="Site:", justify='left', anchor='w')
        site_sel = ctk.CTkOptionMenu(self, values=[v.name for v in Site], variable=vardict["site"])
        site_sel.set(default_site.name)

        bldg_lbl: ctk.CTkLabel = ctk.CTkLabel(self, text="Building:", justify='left', anchor='w')
        bldg_entry: ctk.CTkEntry = ctk.CTkEntry(self, textvariable=vardict["building"])

        room_lbl: ctk.CTkLabel = ctk.CTkLabel(self, text="Room:", justify='left', anchor='w')
        room_entry: ctk.CTkEntry = ctk.CTkEntry(self, textvariable=vardict["room"])

        pacrequired_lbl: ctk.CTkLabel = ctk.CTkLabel(self, text="PAC Required:", justify='left',
                                                     anchor='w')
        pacreq_ckbx = ctk.CTkCheckBox(self, variable=vardict['pac_required'], text="Yes / No")

        site_lbl.grid(row=2, column=0, padx=20, pady=(10,0), sticky='ew')
        site_sel.grid(row=3, column=0, padx=20, pady=(0,10), sticky='ew')
        bldg_lbl.grid(row=2, column=1, padx=20, pady=(10,0), sticky='ew')
        bldg_entry.grid(row=3, column=1, padx=20, pady=(0,10), sticky='ew')
        room_lbl.grid(row=2, column=2, padx=20, pady=(10,0), sticky='ew')
        room_entry.grid(row=3, column=2, padx=20, pady=(0,10), sticky='ew')
        pacrequired_lbl.grid(row=2, column=3, padx=20, pady=(10,0), sticky='ew')
        pacreq_ckbx.grid(row=3, column=3, padx=20, pady=(0,10), sticky='ew')



    def __pack_row_3(self, vardict: WorkOrderFormDict) -> None:
        priority_lbl: ctk.CTkLabel = ctk.CTkLabel(self, text="Priority:",
                                               justify='left', anchor='w')
        priority_btn = ctk.CTkSegmentedButton(self, variable=vardict["priority"])
        priority_btn.configure(values=["1", "2", "3"])
        priority_btn.set("3")

        special_lbl: ctk.CTkLabel = ctk.CTkLabel(self, text="Special(Department):",
                                               justify='left', anchor='w')
        special_btn = ctk.CTkSegmentedButton(self, variable=vardict["special"])
        special_btn.configure(values=[s.name for s in Special])
        special_btn.set(default_special.name)

        wotype_lbl: ctk.CTkLabel = ctk.CTkLabel(self, text="Work Order Type:",
                                               justify='left', anchor='w')
        wotype_btn = ctk.CTkSegmentedButton(self, variable=vardict['type'])
        wotype_btn.configure(values=[s.name for s in WorkOrderType])
        wotype_btn.set(default_wotype.name)

        creator_lbl: ctk.CTkLabel = ctk.CTkLabel(self, text="Work Order Owner:",
                                               justify='left', anchor='w')

        # BCOBB: Change this to a dropdown and use the list of people to populate it
        creator_entry: ctk.CTkEntry = ctk.CTkEntry(self, textvariable=vardict["creator"])

        priority_lbl.grid(row=4, column=0, padx=20, pady=(10,0), sticky='ew')
        priority_btn.grid(row=5, column=0,padx=20, pady=(0,10), sticky='ew')
        special_lbl.grid(row=4, column=1, padx=20, pady=(10,0), sticky='ew')
        special_btn.grid(row=5, column=1, padx=20, pady=(0,10), sticky='ew')
        wotype_lbl.grid(row=4, column=2, padx=20, pady=(10,0), sticky='ew')
        wotype_btn.grid(row=5, column=2, padx=20, pady=(0,10), sticky='ew')
        creator_lbl.grid(row=4, column=3, padx=20, pady=(10,0), sticky='ew')
        creator_entry.grid(row=5, column=3, padx=20, pady=(0,10), sticky='ew')
