from tkinter import *
from typing import Callable, Any
from lib.forms.dateselector import DateSelectForm
from datetime import date, datetime

class TextboxWithDefaultText(Text):
    def __init__(this, master: Tk | Toplevel | Frame, defaultStr: str, valid_contents_fnc: Callable[[Any], bool]) -> None:
        Text.__init__(this, master=master)

        this.default_string: str = defaultStr
        this.contents_are_valid_fnc: Callable[[Any], bool] = valid_contents_fnc
        this.bind("<FocusIn>", this.focus_in_function)
        this.bind("<FocusOut>", this.focus_out_function)
        this.configure(font=('Segoe UI', 9, 'italic'), fg="gray", height=1)
        this.insert(0.0, this.default_string)

    def focus_in_function(this, *args) -> None:
        if this.get(0.0, END).strip("\n") == this.default_string:
            this.delete(0.0, END)
            this.configure(font=('Segoe UI', 9, 'roman'), fg="black")
        
    def focus_out_function(this, *args) -> None:
        if this.get(0.0,END).strip("\n") == "" or not this.contents_are_valid_fnc(None):
            this.delete(0.0, END)
            this.insert(0.0, this.default_string)
            this.configure(font=('Segoe UI', 9, 'italic'), fg="gray")

    
    def get_text(this) -> str:
        return this.get(0.0, END).strip('\n')


class EntryWithDefaultText(Entry):
    def __init__(this, master: Tk | Toplevel | Frame, defaultStr: str, valid_contents_fnc: Callable[[str], bool]) -> None:
        Entry.__init__(this, master=master)

        this.default_string: str = defaultStr
        this.string_var: StringVar = StringVar(this, value=defaultStr)
        this.contents_are_valid_fnc: Callable[[str], bool] = valid_contents_fnc
        this.bind("<FocusIn>", this.focus_in_function)
        this.bind("<FocusOut>", this.focus_out_function)
        this.configure(font=('Segoe UI', 9, 'italic'), fg="gray", textvariable=this.string_var)

    def focus_in_function(this, *args) -> None:
        if this.string_var.get() == this.default_string:
            this.string_var.set("")
            this.configure(font=('Segoe UI', 9, 'roman'), fg="black")
        
    def focus_out_function(this, *args) -> None:
        if this.string_var.get() == "" or not this.contents_are_valid_fnc(this.string_var.get()):
            this.string_var.set(this.default_string)
            this.configure(font=('Segoe UI', 9, 'italic'), fg="gray")
    
    def get_text(this) -> str:
        return this.get()


class DateEntry(Entry):    
    def __init__(this, master: Tk | Toplevel | Frame) -> None:
        Entry.__init__(this, master=master)
        this.string_var: StringVar = StringVar(this, value="Select")
        this.configure(width=12, font=('Segoe UI', 9, 'italic'), fg="gray",textvariable=this.string_var)
        this.bind("<FocusIn>", this._launch_calendar_form)

    
    def _launch_calendar_form(this, event: Event) -> None:
        """Event Handler: Defines what happens when you click on the Work Order Start Date input box."""
        cal_form: DateSelectForm = DateSelectForm(this.string_var)
        cal_form.bind("<Destroy>", this._update_format)


    def _update_format(this, event: Event) -> None:
        """Event Handler: Defines what happens when the DateSelectForm child form closes."""
        if event.widget != event.widget.winfo_toplevel():
            return
        
        if this.string_var.get() != "Select":
            this.configure(font=('Segoe UI', 9, 'roman'), fg="black")        
        this.tk_focusNext().focus() #type:ignore

    def get_var_val(this) -> str:
        return this.string_var.get()
    
    def get_StringVar_object(this) -> StringVar:
        return this.string_var
    

class CheckBoxWithDateEntry(Frame):
    def __init__(this, master: Tk | Toplevel | Frame, text_string: str):
        Frame.__init__(this, master)        
        dateselect: DateEntry = DateEntry(this)
        dateselect.configure(state='disabled')
        dateselect.pack(side='right', anchor='e', padx=10)        
        this.boolvar: BooleanVar = BooleanVar(this)
        this.strvar: StringVar = dateselect.get_StringVar_object()
        ckbox: Checkbutton = Checkbutton(this, variable=this.boolvar, text=text_string)
        ckbox.pack(side='left', anchor='w', padx='10')

    
    def get_bool(this) -> bool:
        return this.boolvar.get()
    

    def get_date_string(this) -> str:
        return this.strvar.get()
    

