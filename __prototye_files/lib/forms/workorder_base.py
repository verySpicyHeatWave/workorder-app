################ IMPORT DECLARATIONS ########################################################################
#pylint: skip-file

from tkinter import *
from tkinter import ttk, messagebox
from openpyxl import load_workbook          #type:ignore
from openpyxl.styles import Alignment       #type:ignore

from lib.forms.advancedoptions import AdvancedOptionsForm                                   #type:ignore
from lib.workorder import WorkOrder                                                         #type:ignore
from lib.global_resources import *                                                          #type:ignore
from lib.outlook_utils import generate_new_twois_request_email                              #type:ignore
from lib.forms.tkform_wrappers import Toplevel_Adapter                                      #type:ignore
from lib.custom_tkwidgets import EntryWithDefaultText, TextboxWithDefaultText, DateEntry    #type:ignore



################ CLASS DEFINITION AND INITIALIZER ###########################################################
class WorkOrderForm(Toplevel_Adapter):
    """This class generates a tkinter form intended to create a new TWOIS form or to edit an existing one.\n
    Note: Most of the work is done here, but this class is meant to be inherited by two other classes:\n
    the NewWorkOrderForm and the EditWorkOrderForm class. This class isn't meant to be used on its own."""
    _WOTITLE_SAMPLE_STRING: str = "Enter a description of your task here"
    _TASKLIST_SAMPLE_STRING: str = "This is an example task; this is an example document\n14-Day AV Updates Ops GMM;D743-26217-23 revP sec0030-20"
    _DESCRIPTION_SAMPLE_STRING: str = "(OPTIONAL) Enter a detailed description of the task"

    def __init__(this, master) -> None:
        Toplevel_Adapter.__init__(this, master)        
        this._requires_pac: BooleanVar = BooleanVar(value=False)
        this.geometry("900x550")
        this.title("OVERWRITE THIS TITLE STRING")
        this.resizable(False, False)
        this._pack_top_frame()
        this._pack_second_frame()
        this._pack_task_list_frame()
        this._pack_description_frame()
        this._generate_submit_button(this)
        this.grab_set()



    ############ FORM LAYOUT METHODS ########################################################################
    def _pack_top_frame(this) -> None:
        """Form Layout Method: Defines form layout at the top of the form."""
        this._top_frame: Frame = Frame(this, height=1)
        this._generate_workorder_title_input(this._top_frame)        
        this._generate_workorder_type_input(this._top_frame)
        this._set_tabkey_focus_control(this._top_frame)
        this._top_frame.pack(side='top', pady=5, anchor='w')


    def _pack_second_frame(this) -> None:
        """Form Layout Method: Defines form layout at the second level of the form."""
        this._second_frame: Frame = Frame(this, height=1)
        this._generate_start_date_input(this._second_frame)
        this._generate_priority_input(this._second_frame)
        this._generate_location_input(this._second_frame)
        this._generate_pac_required_checkbox(this._second_frame)
        this._generate_advanced_options_button(this._second_frame)
        this._set_tabkey_focus_control(this._second_frame)
        this._second_frame.pack(side='top', pady=5, anchor='w')
    

    def _pack_task_list_frame(this) -> None:
        """Form Layout Method: Defines the task list input box."""
        this._taskListFrame: Frame = Frame(this, height=10, width=900)

        this._tasklist_lbl: Label = Label(this._taskListFrame, text = "    Task List:   ", height = 10, justify='left', anchor='n')
        this._tasklist_lbl.pack(side='left')
        this._tasklist_txt: TextboxWithDefaultText = TextboxWithDefaultText(this._taskListFrame, this._TASKLIST_SAMPLE_STRING, lambda ev: True)
        this._tasklist_txt.configure(height = 10, width=120)
        this._tasklist_txt.pack(side='right')

        this._set_tabkey_focus_control(this._taskListFrame)
        this._taskListFrame.pack(side='top', pady=5, anchor='w')

    
    def _pack_description_frame(this) -> None:
        """Form Layout Method: Defines the task description input box."""
        this._description_frame: Frame = Frame(this, height=10, width=900)

        this._description_lbl: Label = Label(this._description_frame, text = " Description: ", height = 14, justify='left', anchor='n')
        this._description_lbl.pack(side='left')
        this._description_txt: TextboxWithDefaultText = TextboxWithDefaultText(this._description_frame, this._DESCRIPTION_SAMPLE_STRING, lambda ev: True)
        this._description_txt.configure(height = 14, width=120)
        this._description_txt.pack(side='right')
        
        this._set_tabkey_focus_control(this._description_frame)
        this._description_frame.pack(side='top', pady=5, anchor='w')

        
    def _set_tabkey_focus_control(this, master: Frame) -> None:
        """Form Layout Method: Sets every object in a frame to bind the \"<Tab>\" key with the shifting of focus to the next object on the form."""
        for child in master.winfo_children():
            child.bind("<Tab>", this._focus_on_next_object)
        master.pack(side='top', pady=5, anchor='w')


    def _generate_workorder_title_input(this, master: Frame | Tk | Toplevel) -> None:
        """Form Layout Method: Defines the Work Order Title input box."""
        this._workorder_title_lbl: Label = Label(master, text="WO Title: ", height=1, anchor='w')
        this._workorder_title_lbl.pack(padx=10, side='left')
        this._workorder_title_input: EntryWithDefaultText = EntryWithDefaultText(master, this._WOTITLE_SAMPLE_STRING, lambda ev: True)
        this._workorder_title_input.configure(width=68)
        this._workorder_title_input.pack(side='left')


    def _generate_workorder_type_input(this, master: Frame | Tk | Toplevel) -> None:  
        """Form Layout Method: Defines the Work Order Type combo box."""
        this._workorder_type_cmb: ttk.Combobox = ttk.Combobox(master, height=1, width = 24)
        for k in G_WO_TYPE_DICT.keys():#type:ignore
            this._workorder_type_cmb['values'] = (*this._workorder_type_cmb['values'], k)
        this._workorder_type_cmb.current(0)
        this._workorder_type_cmb.pack(side='right')
        this._workorder_type_lbl: Label = Label(master, text="WO Type: ", height=1)
        this._workorder_type_lbl.pack(padx=10, side='right')


    def _generate_start_date_input(this, master: Frame | Tk | Toplevel) -> None:  
        """Form Layout Method: Defines the Work Order Start Date input box."""
        this._start_date_lbl:Label = Label(master, text = "  Start Date:   ")
        this._start_date_lbl.pack(side='left')
        this._start_date_txt: DateEntry = DateEntry(master)
        this._start_date_txt.pack(side='left')


    def _generate_priority_input(this, master: Frame | Tk | Toplevel) -> None:  
        """Form Layout Method: Defines the Work Order Priority combo box."""
        this._priority_lbl: Label = Label(master, text="Priority:")
        this._priority_lbl.pack(side='left', padx=10)
        this._priority_cmb: ttk.Combobox = ttk.Combobox(master, height=1, width=12)
        this._priority_cmb['values'] = ('1 (highest)',
                                '2',
                                '3 (lowest)')
        this._priority_cmb.current(2)
        this._priority_cmb.pack(side='left')


    def _generate_location_input(this, master: Frame | Tk | Toplevel) -> None: 
        """Form Layout Method: Defines the Work Order Location combo box."""
        this._location_lbl: Label = Label(master, text="Location:")
        this._location_lbl.pack(side='left', padx=10)
        this._location_cmb: ttk.Combobox = ttk.Combobox(master, height=1, width=25)
        for k in g_sites_dict.keys():#type:ignore
            this._location_cmb['values'] = (*this._location_cmb['values'], k)
        this._location_cmb.current(0)
        this._location_cmb.pack(side='left')


    def _generate_pac_required_checkbox(this, master: Frame | Tk | Toplevel) -> None:  
        """Form Layout Method: Defines the Work Order PAC Required check box."""
        this._requires_pac_ckbx: Checkbutton = Checkbutton(master, text="PAC Required?", justify='left', variable=this._requires_pac,
                                            onvalue=True, offvalue=False)
        this._requires_pac_ckbx.deselect()
        this._requires_pac_ckbx.pack(side='left', padx=10)

    
    def _generate_advanced_options_button(this, master: Frame | Tk | Toplevel) -> None:  
        """Form Layout Method: Defines the Work Order Advanced Options button."""
        this._advanced_options_btn: Button = Button(master, text="Advanced Options", command=this._launch_advanced_options_form)
        this._advanced_options_btn.pack(side='left', padx=10)


    def _generate_submit_button(this, master: Frame | Toplevel | Tk) -> None:
        """Form Layout Method: Defines the Work Order Submit button."""
        this._submit_button: Button = Button(master, text="OVERWRITE ME")
        this._submit_button.pack(side='left', padx=10)



    ############ EVENT HANDLERS #############################################################################
    # def _launch_calendar_form(this, event: Event) -> None:
    #     """Event Handler: Defines what happens when you click on the Work Order Start Date input box."""
    #     cal_form: DateSelectForm = DateSelectForm(this)
    #     cal_form.bind("<Destroy>", this._update_selected_date)


    def _launch_advanced_options_form(this) -> None:
        """Event Handler: Defines what happens when you click on the Work Order Advanced Options button."""
        AdvancedOptionsForm(this)


    def _focus_on_next_object(this, event: Event) -> None:
        """Event Handler: Defines what happens when you hit the \"<Tab>\" key."""
        event.widget.tk_focusNext().focus()
    
    
    # def _update_selected_date(this, event: Event) -> None:
    #     """Event Handler: Defines what happens when the DateSelectForm child form closes."""
    #     this._start_date_txt.configure(font=('Segoe UI', 9, 'roman'), fg="black")
    #     this._start_date_txt.delete(0, END)
    #     this._start_date_txt.insert(0, this.get_date_string())

    

    ############ INTERNAL METHODS ###########################################################################
    def _generate_workorder(this, is_a_new_workorder: bool, WONumber: str) -> None:
        """Method used for generating a complete TWOIS File package.\n
        This includes generating the Excel file, the .twois data file, and generating an email.\n
        Method takes in a boolean (True if you want to compose an email, false if not) and a work order number (e.g. \"123456VBS\", \"Pending-001\")."""
        if not this._all_inputs_are_valid():
            return
        
        twois_template = load_workbook(TEMPLATE_TWOIS)#type:ignore
        twois_sheet = twois_template.active

        #BCOBB: MAYBE I SHOULD CREATE A DICTIONARY WITH ALL OF THESE CELL VALUES AND A STRING THAT IDENTIFIES THEM OR SOMETHING, SO THE CODE'S A LITTLE MORE SELF DOCUMENTING
        # CONSTANT VALUES
        twois_sheet['B4'] = 'RS'
        twois_sheet['B5'] = 'BC' #BCOBB: DERIVE BASED ON FULL NAME
        twois_sheet['C7'] = 'S'
        twois_sheet['B10'] = 'Brian Cobb' #BCOBB: MAKE_CONFIGURABLE
        twois_sheet['G10'] = 'N/A'

        # TWOIS FORM OPTIONS
        twois_sheet['B3'] = this._start_date_txt.get_var_val()
        twois_sheet['B3'].alignment = Alignment(wrap_text=False, horizontal='center', vertical='center')
        twois_sheet['A7'] = "" if WONumber.startswith("Pending") else WONumber
        twois_sheet['B7'] = this._determine_site(this._location_cmb.get().split(":")[0])
        twois_sheet['D7'] = this._workorder_title_input.get()
        twois_sheet['I7'] = this._determine_workorder_type(this._workorder_type_cmb.get())
        twois_sheet['D8'] = this._determine_location(this._location_cmb.get())
        twois_sheet['A10'] = int(this._priority_cmb.get()[0])
        twois_sheet['I10'] = "PAC - YES" if this._requires_pac.get() else "PAC - NO"

        # ADVANCED SETTINGS
        twois_sheet['A12'] = "Yes" if this._advanced_options['requiresNCR'].get() else "No" 
        twois_sheet['B12'] = this._ncr_number if this._advanced_options['requiresNCR'].get() else "N/A"
        twois_sheet['E12'] = "Yes" if this._advanced_options['requiresTaskLead'].get() else "No" 
        twois_sheet['F12'] = "Yes" if this._advanced_options['techWitnessPoint'].get() else "No" 
        twois_sheet['G12'] = "Yes" if this._advanced_options['requiresPeerReview'].get() else "No" 
        twois_sheet['H12'] = "Yes" if this._advanced_options['peerReviewAttached'].get() else "No" 
        twois_sheet['I12'] = "Yes" if this._advanced_options['requiresEHS'].get() else "No" 
        twois_sheet['J12'] = "Yes" if this._advanced_options['QAMIP'].get() else "No" 
        twois_sheet['K12'] = "Yes" if this._advanced_options['requiresQAReview'].get() else "No" 

        # TASK LIST
        task_number: int = 10
        excel_row: int = 16
        task_item_strings: list[str] = this._tasklist_txt.get(0.0, END).split("\n")

        for task_string in task_item_strings:
            task_items = task_string.split(";")
            ref: str = ""
            reference_was_provided: bool = len(task_items) > 1
            if reference_was_provided:
                ref = task_items[1]
            if len(task_string) > 2:
                twois_sheet['A' + str(excel_row)] = task_number
                twois_sheet['B' + str(excel_row)] = task_items[0]
                twois_sheet['G' + str(excel_row)] = ref
            task_number += 10
            excel_row += 1

        # GENERATE FILES
        title: str = this._workorder_title_input.get().strip()
        short_filename: str =f"{os.getcwd()}/in_progress/VSFB SA - {title}.xlsx"#type:ignore
        long_filename: str = f"{os.getcwd()}/in_progress/{WONumber} VSFB SA - {title}.xlsx"#type:ignore

        if is_a_new_workorder:
            twois_template.save(short_filename)
            generate_new_twois_request_email(title, short_filename, this.get_date_string())
            twois_template.close()
            os.rename(short_filename, long_filename)#type:ignore
        else:
            twois_template.save(long_filename)
            twois_template.close()
            os.remove(f"{IN_PROGRESS_DIR}\\{WONumber}.twois")#type:ignore
            
        description = this._description_txt.get(0.0, END).strip("\n")
        if description == "" or description == this._DESCRIPTION_SAMPLE_STRING:
            description = ""
        
        workorder: WorkOrder = WorkOrder(long_filename, description)
        workorder.save_workorder_as_twois_file()
        this.destroy()


    def _all_inputs_are_valid(this) -> bool:
        """Method used for determining that the form is properly filled out before proceeding with work order generation."""
        workorder_title_text: str = this._workorder_title_input.get()
        if workorder_title_text == this._WOTITLE_SAMPLE_STRING or len(workorder_title_text) < 15 or len(workorder_title_text) > 100:
            messagebox.showerror("Work Order Title Error", "Error: The Work Order Title must be between 15 and 100 characters")
            return False

        start_date: str = this._start_date_txt.get()
        if len(start_date) > 10 or start_date.startswith("Select") or len(start_date.split("/")) != 3:
            messagebox.showerror("Date Select Error", "Error: A scheduled start date must be selected")
            return False

        tasklist_text = this._tasklist_txt.get(0.0, END).strip("\n")
        if tasklist_text == "" or tasklist_text == this._TASKLIST_SAMPLE_STRING or len(tasklist_text.split(";")) < 2:
            messagebox.showerror("Task List Error", "Error: The task list needs to be filled out with at least one list item, including a reference separated by a semicolon")
            return False
        
        return True
    
    
    def _determine_site(this, strval: str) -> str:
        """Method used for determining what to enter into the cell which defines the site at which the work is to be performed.\n 
        Takes in the abbreviated name of a base (e.g. \"VSFB\", \"FGA\")."""
        resp: str = ""
        match strval.strip():
            case "VSFB":
                resp = "VB"
            case "FGA":
                resp = "FG"
        return resp


    def _determine_location(this, strval: str) -> str:
        """Method used for determining what to enter into the cell which defines the building and room at which the work is to be performed.\n 
        Takes in the value at the Location combo box which should be formatted \"VSFB : Bldg 1768 : Rm 21\"."""
        splits = strval.split(":")
        resp: list[str] = list()
        resp.append(splits[1].strip())
        resp.append(splits[2].strip())
        return ", ".join(resp)


    def _determine_workorder_type(this, strval: str) -> str:
        """Method used for determining what to enter into the cell which defines the type of work order.\n
        Takes in the value at the WO Type combo box, which are non-configurable and defined in the global constants file."""
        resp: str = ""
        match strval.strip():
            case "Preventative Maintenance":
                resp = "PM"
            case "Corrective Maintenance":
                resp = "CM"
            case "Other":
                resp = "OTH"
        return resp
        

    
################ END OF FILE ################################################################################