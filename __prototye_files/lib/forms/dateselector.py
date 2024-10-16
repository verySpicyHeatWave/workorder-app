from datetime import date, datetime
from tkcalendar import Calendar #type: ignore
from tkinter import *



class DateSelectForm(Toplevel):    
    return_date: date = date.today()

    def __init__(this, string_var: StringVar) -> None:
        Toplevel.__init__(this, None)
        this.geometry("250x220")
        this.title('Choose date')
        this.resizable(False, False)
        this._string_var = string_var
        
        this._cal: Calendar = Calendar(this, selectmode = 'day',
                    year = this.return_date.year, month = this.return_date.month, 
                    day = this.return_date.day, date_pattern='mm/dd/yyyy')
        this._cal.pack()
    
        this._submit_btn: Button = Button(this, text="Confirm Selection", command=this._pick_date)
        this._submit_btn.pack()
        this.grab_set()

    
    def _pick_date(this) -> None:
        intermediary_datetime: datetime = datetime.strptime(this._cal.get_date(), "%m/%d/%Y")
        resp_str: str = intermediary_datetime.strftime('%#m/%#d/%Y')
        this._string_var.set(resp_str)
        this.destroy()

        

