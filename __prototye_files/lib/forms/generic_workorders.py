from lib.forms.tkform_wrappers import Toplevel_Adapter
from lib.custom_tkwidgets import DateEntry

from tkinter import *
from typing import Callable

class GenericWorkordersForm(Toplevel_Adapter):
    def __init__(this, master: Toplevel | Tk):
        Toplevel_Adapter.__init__(this, master)
        this.LIST_OF_SYSTEMS: list[str] = ["OSB GMM", "GMDE GMM", "OSB BSAT", "AV Laptops", "CVA Laptops", "MSE Package"]
        this.avdat_bools: list[BooleanVar] = []
        this.avdat_dates: list[StringVar] = []
        this.avscan_bools: list[BooleanVar] = []
        this.avscan_dates: list[StringVar] = []

        boxesframe: Frame = Frame(this)

        avdat_frame: Frame = Frame(boxesframe)
        avdat_label: Label = Label(avdat_frame, text="AV .DAT Updates", justify='center', font=('Segoe UI', 12, 'roman'), fg="black")
        avdat_label.pack(side='top')
        this.__pack_frame(avdat_frame, this.avdat_bools, this.avdat_dates)
        avdat_frame.pack(side='left', padx=30, pady=20)

        avscan_frame: Frame = Frame(boxesframe)
        avscan_label: Label = Label(avscan_frame, text="AV Scans", justify='center', font=('Segoe UI', 12, 'roman'), fg="black")
        avscan_label.pack(side='top')
        this.__pack_frame(avscan_frame, this.avscan_bools, this.avscan_dates)
        avscan_frame.pack(side='right', padx=30, pady=20)

        boxesframe.pack(side='top')

        buttonframe: Frame = Frame(this)
        submit_btn: Button = Button(buttonframe, text="Submit", command=this.submit_all_workorders)
        submit_btn.pack(side='left', padx=10)
        cancel_btn: Button = Button(buttonframe, text="Cancel", command=this.destroy)
        cancel_btn.pack(side='left', padx=10)
        buttonframe.pack(side='bottom', pady=10)
        

    def __pack_frame(this, frame: Frame, bools: list[BooleanVar], dates: list[StringVar]) -> None:
        for system in this.LIST_OF_SYSTEMS:
            item_frame: Frame = Frame(frame, width=100)
            boolvar: BooleanVar = BooleanVar(this)

            dateselect: DateEntry = DateEntry(item_frame)
            dateselect.configure(state='disabled')

            ckbox: Checkbutton = Checkbutton(item_frame, variable=boolvar, text=system, width=20)
            ckbox.bind("<Button-1>", this.__check_associated_bool_status_with_lambda(boolvar, dateselect))
            
            bools.append(boolvar)
            dates.append(dateselect.get_StringVar_object())

            ckbox.pack(side='left', anchor='w', padx='10')
            dateselect.pack(side='right', anchor='e', padx=10)
            item_frame.pack(side='top')


    def __check_associated_bool_status_with_lambda(this, boolvar: BooleanVar, dateselect: DateEntry, *args) -> Callable:
        return lambda ev:this.__check_associated_bool_status(boolvar, dateselect)
    
    def __check_associated_bool_status(this, boolvar: BooleanVar, dateselect: DateEntry) -> None:
        newbool: bool = not boolvar.get()
        boolvar.set(not newbool)
        if newbool:
            dateselect.configure(state='normal')
        else:
            dateselect.configure(state='disabled')

    def submit_all_workorders(this) -> None:
        #BCOBB: Don't just print the values: actually post them up
        for i in range(len(this.LIST_OF_SYSTEMS)):
            if this.avdat_bools[i].get():
                print(f"{this.LIST_OF_SYSTEMS[i]}  \tAV Dat Required:\t{this.avdat_dates[i].get()}")
            if this.avscan_bools[i].get():
                print(f"{this.LIST_OF_SYSTEMS[i]}  \tAV Scan Required:\t{this.avscan_dates[i].get()}")
        print("\n=================================================\n\n")