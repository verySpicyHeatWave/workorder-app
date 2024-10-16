from tkinter import *

from lib.workorder import *
from lib.global_resources import *
from lib.forms.workorder_base import WorkOrderForm




class EditWorkOrderForm(WorkOrderForm):    
    """This class generates a tkinter form intended to update an existing TWOIS form"""

    # Initializer
    def __init__(this, master, workorder: WorkOrder) -> None:
        WorkOrderForm.__init__(this, master)
        this.title(f"Edit TWOIS# {workorder.number}")
        this._submit_button.configure(text=f"Update TWOIS", command=this._update_workorder)
        this.workorder = workorder

        #populate the form with info from the work order
        this._workorder_title_input.delete(0, END)
        this._workorder_title_input.configure(font=('Segoe UI', 9, 'roman'), fg="black")
        this._workorder_title_input.insert(0, this.workorder.title)

        this._start_date_txt.delete(0, END)
        this._start_date_txt.configure(font=('Segoe UI', 9, 'roman'), fg="black")
        this._start_date_txt.insert(0, str(this.workorder.planned_date))

        #task list
        this._tasklist_txt.delete(0.0, END)
        this._tasklist_txt.configure(font=('Segoe UI', 9, 'roman'), fg="black")
        taskstr = ""
        for task in workorder.tasks:
            if task.number > 0:
                taskstr += f"{task.summary};{task.reference}\n"
        this._tasklist_txt.insert(0.0, taskstr)

        #description
        this._description_txt.delete(0.0, END)
        this._description_txt.configure(font=('Segoe UI', 9, 'roman'), fg="black")
        this._description_txt.insert(0.0, this.workorder.description)

        #priority
        this._priority_cmb.current(workorder.priority_index)

        #location
        this._location_cmb.current(workorder.location_index)

        #wo type (pm, cm, oth)
        this._workorder_type_cmb.current(workorder.workorder_type_index)

        #PAC required check box
        #BCOBB: Check if a PAC is required here!

        #BCOBB: Populate the this._advanced_options dictionary
        # will also need to populate the advanced options form if it comes up

    
    def _update_workorder(this) -> None:
        this._generate_workorder(False, this.workorder.number)