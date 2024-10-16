from lib.global_resources import IN_PROGRESS_DIR, get_next_pending_workorder_number
from lib.forms.workorder_base import WorkOrderForm

class NewWorkOrderForm(WorkOrderForm):
    """This class generates a tkinter form intended to create a new TWOIS form"""

    def __init__(this, master) -> None:
        WorkOrderForm.__init__(this, master)
        this.title("Generate new TWOIS form")
        this._submit_button.configure(text="Generate TWOIS", command=this._populate_new_workorder)
        
    def _populate_new_workorder(this) -> None:
        this._generate_workorder(True, get_next_pending_workorder_number())
