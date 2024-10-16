from tkinter import Tk, Toplevel, BooleanVar, StringVar
from datetime import date
from typing import Callable

class Toplevel_Adapter(Toplevel):
    
    _ADVANCED_OPTION_NAMES: list[str] = ["requiresNCR",  "requiresTaskLead", "techWitnessPoint", "requiresPeerReview", 
                          "peerReviewAttached", "requiresEHS", "QAMIP", "requiresQAReview"]
    def __init__(this, master: Toplevel | Tk) -> None:
        Toplevel.__init__(this, master)
        this._date: date = date.today()
        this._ncr_number: str = ""
        this._advanced_options: dict = dict(
            requiresNCR = BooleanVar(value=False),
            requiresTaskLead = BooleanVar(value=False),
            techWitnessPoint = BooleanVar(value=False),
            requiresPeerReview = BooleanVar(value=False),
            peerReviewAttached = BooleanVar(value=False),
            requiresEHS = BooleanVar(value=False),
            QAMIP = BooleanVar(value=False),
            requiresQAReview = BooleanVar(value=False))      

    def set_date(this, d: date) -> None:
        this._date = d

    def get_date(this) -> date:
        return this._date

    def get_date_string(this) -> str:
        return this._date.strftime("%#m/%#d/%Y")
    
    def get_ncr_number(this) -> str:
        return this._ncr_number
    
    def set_ncr_number(this, NCR: str) -> None:
        this._ncr_number = NCR
    

class Tk_Adapter(Tk):
    def __init__(this) -> None:
        Tk.__init__(this)
        this._date: date = date.today()

    def set_date(this, d: date) -> None:
        this._date = d

    def get_date(this) -> date:
        return this._date

    def get_date_string(this) -> str:
        return this._date.strftime("%#m/%#d/%Y")
    
