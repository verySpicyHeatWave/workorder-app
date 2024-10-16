from tkinter import *
from lib.forms.tkform_wrappers import Toplevel_Adapter
from tkinter import messagebox
import re

class AdvancedOptionsForm(Toplevel):
    """Child of a NewWorkOrderForm only! Used to set the advanced work order options."""
    def __init__(this, master: Toplevel_Adapter) -> None:
        Toplevel.__init__(this, master)
        this.geometry("250x300")
        this.title("Advanced")
        this.resizable(False, False)
        this._master: Toplevel_Adapter = master
                
        this._populate_controls()

        this.protocol("WM_DELETE_WINDOW", this._close_window_check)
        this.grab_set()




    def _populate_controls(this) -> None:
        this._requires_ncr_ckbx: Checkbutton = Checkbutton(this, text="NCR Required", 
                                                          variable=this._master._advanced_options['requiresNCR'],
                                                          onvalue=True, offvalue=False, command=this._update_ncr_input_box)

        this._requires_task_lead_ckbx: Checkbutton = Checkbutton(this, text="Task Lead Required", 
                                                               variable=this._master._advanced_options['requiresTaskLead'],
                                                               onvalue=True, offvalue=False)

        this._tech_witness_point_ckbx: Checkbutton = Checkbutton(this, text="Tech Witness Point", 
                                                               variable=this._master._advanced_options['techWitnessPoint'],
                                                               onvalue=True, offvalue=False)

        this._requires_peer_review_ckbx: Checkbutton = Checkbutton(this, text="Peer Review Required", 
                                                                 variable=this._master._advanced_options['requiresPeerReview'], 
                                                                 onvalue=True, offvalue=False)

        this._peer_review_attached_ckbx: Checkbutton = Checkbutton(this, text="Peer Review Attached", 
                                                                 variable=this._master._advanced_options['peerReviewAttached'],
                                                                 onvalue=True, offvalue=False)

        this._requires_ehs_ckbx: Checkbutton = Checkbutton(this, text="EHS Required", 
                                                          variable=this._master._advanced_options['requiresEHS'], 
                                                          onvalue=True, offvalue=False)

        this._qamip_ckbx: Checkbutton = Checkbutton(this, text="QAMIP", 
                                                    variable=this._master._advanced_options['QAMIP'], 
                                                    onvalue=True, offvalue=False)

        this._requires_qa_review_ckbx: Checkbutton = Checkbutton(this, text="QA Review Required", 
                                                               variable=this._master._advanced_options['requiresQAReview'], 
                                                               onvalue=True, offvalue=False)
        
        this._ncr_number_lbl: Label = Label(this, height=2, anchor='nw', text="NCR Number: ")
        this._ncr_number_input: Entry = Entry(this, width=15, state='disabled')
        this._confirm_btn: Button = Button(this, text="Confirm Selection", command=this._close_window_check)


        this._requires_ncr_ckbx.pack(side='top', anchor='w', padx=10)
        this._requires_task_lead_ckbx.pack(side='top', anchor='w', padx=10)
        this._tech_witness_point_ckbx.pack(side='top', anchor='w', padx=10)
        this._requires_peer_review_ckbx.pack(side='top', anchor='w', padx=10)
        this._requires_ehs_ckbx.pack(side='top', anchor='w', padx=10)
        this._peer_review_attached_ckbx.pack(side='top', anchor='w', padx=10)
        this._qamip_ckbx.pack(side='top', anchor='w', padx=10)
        this._requires_qa_review_ckbx.pack(side='top', anchor='w', padx=10)
        this._ncr_number_lbl.pack(side='top', anchor='w', padx=10)
        this._ncr_number_input.pack(side='top', anchor='w', padx=10)
        this._confirm_btn.pack(side='top', anchor='w', padx=40)


    def _update_ncr_input_box(this) -> None:
        if this._master._advanced_options['requiresNCR'].get():
            this._ncr_number_input.configure(state='normal')
        else:
            this._ncr_number_input.configure(state='disabled')

    def _close_window_check(this) -> None:
        ncr = None
        okay_to_quit = True
        if this._master._advanced_options['requiresNCR'].get():
            ncr = this._ncr_number_input.get().strip()
            ncrReg = re.compile(r'NCR\d\d\d\d\d\dW')
            resp = ncrReg.search(ncr)
            if len(ncr) > 10 or resp == None:
                messagebox.showerror("NCR Number Required", "You need to supply an NCR number if an NCR is required for this Work Order")
                okay_to_quit = False
        if okay_to_quit:
            this._master.set_ncr_number(str(ncr))
            this.destroy()
