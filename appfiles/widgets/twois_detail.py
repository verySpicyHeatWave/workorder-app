"""Yo!"""

from datetime import date
from functools import partial
from tkinter import END, messagebox

import customtkinter as ctk #type: ignore

from appfiles.library.logcomment import LogComment
from appfiles.library.workorder import WorkOrder
from appfiles.utils.workorder import format_room_number
from appfiles.utils.appglobals import primary_user

WRAP_LEN = 365
BTN_W = 100


class TWOISDetailFrame(ctk.CTkFrame):
    """Yo!"""
    def __init__(self, master: ctk.CTk | ctk.CTkToplevel | ctk.CTkFrame |
                 ctk.CTkScrollableFrame, workorder: WorkOrder):
        super().__init__(master=master)
        self.workorder = workorder
        self.grid_columnconfigure(0, weight=1)

        num_label: ctk.CTkLabel = ctk.CTkLabel(self,
                                               text=self.workorder.get_full_workorder_number(),
                                               font=ctk.CTkFont(size=20, weight="bold"))

        title_label: ctk.CTkLabel = ctk.CTkLabel(self, text=self.workorder.title)

        due_str: str = f"Scheduled date:\t{self.workorder.due_date.strftime('%a, %b %d, %Y')}"
        due_label: ctk.CTkLabel = ctk.CTkLabel(self, anchor='w', text=due_str)
        if self.workorder.due_date < date.today():
            due_label.configure(text_color=("#A33331", "#BF3C3A"))

        rm_str: str = format_room_number(self.workorder.room, self.workorder.building)
        loc_str: str = f"Location:\t\tBldg. {self.workorder.building}, {rm_str}"
        loc_label: ctk.CTkLabel = ctk.CTkLabel(self, anchor='w', text=loc_str)

        pac_str: str = f"PAC Required:\t{self.workorder.pac_required}"
        pac_label: ctk.CTkLabel = ctk.CTkLabel(self, anchor='w', text=pac_str)

        task_str: str = "Tasks:\t\t"
        for i, task in enumerate(self.workorder.task_list):
            task_str += str(task)
            if i < len(self.workorder.task_list) - 1:
                task_str += "\n\t\t"

        thead_label: ctk.CTkLabel = ctk.CTkLabel(self, anchor='w', text=task_str, justify='left')

        desc_label: ctk.CTkLabel = ctk.CTkLabel(self, anchor='w', text=self.workorder.description,
                                                wraplength=WRAP_LEN, justify='left')

        btnframe: ctk.CTkFrame = ctk.CTkFrame(self)
        btnframe.grid_columnconfigure(1, weight=1)

        actn_txt: str = "Complete" if self.workorder.is_approved(False) else "Approve"
        self.actn_btn: ctk.CTkButton = ctk.CTkButton(btnframe, text=actn_txt, width=BTN_W,)
        self.edit_btn: ctk.CTkButton = ctk.CTkButton(btnframe, text="Edit", width=BTN_W)
        self.del_btn: ctk.CTkButton = ctk.CTkButton(btnframe, text="Delete", width=BTN_W)
        self.hide_btn: ctk.CTkButton = ctk.CTkButton(btnframe, text="Hide", width=BTN_W)
        self.logs_btn: ctk.CTkButton = ctk.CTkButton(btnframe, text="View Log Comments")

        num_label.grid(     row=0, column=0, padx=20, pady=(10,2), sticky='ew')
        title_label.grid(   row=1, column=0, padx=20, pady=(0,20), sticky='ew')
        due_label.grid(     row=2, column=0, padx=20, pady=0, sticky='ew')
        loc_label.grid(     row=3, column=0, padx=20, pady=0, sticky='ew')
        pac_label.grid(     row=4, column=0, padx=20, pady=0, sticky='ew')
        thead_label.grid(   row=5, column=0, padx=20, pady=5, sticky='ew')
        desc_label.grid(    row=6, column=0, padx=20, pady=0, sticky='ew')
        self.grid_rowconfigure( 7, weight=1)

        btnframe.grid(      row=8, column=0, padx=20, pady=10, sticky='ew')
        self.actn_btn.grid( row=0, column=0, padx=(50,5), pady=(10,5), sticky='w')
        self.edit_btn.grid( row=0, column=2, padx=(5,50), pady=(10,5), sticky='e')
        self.del_btn.grid(  row=1, column=0, padx=(50,5), pady=5, sticky='w')
        self.hide_btn.grid( row=1, column=2, padx=(5,50), pady=5, sticky='e')
        self.logs_btn.grid( row=2, column=0, columnspan=3, padx=50, pady=(5,10), sticky='ew')




class TWOISDetailButton(ctk.CTkButton):
    """Yo!"""
    def __init__(self, master: ctk.CTk | ctk.CTkToplevel | ctk.CTkFrame |
                 ctk.CTkScrollableFrame, workorder: WorkOrder):
        super().__init__(master=master)
        self.workorder = workorder
        btntxt: str = workorder.get_full_workorder_number().ljust(56)
        btntxt += f"Due {str(workorder.due_date).ljust(14)}\n"
        btntxt += workorder.title.ljust(79)
        self.configure(text=btntxt, anchor="w", compound='left',
                       font=ctk.CTkFont("DejaVu Sans Mono", 12, "normal"))
        if self.workorder.due_date < date.today():
            self.configure(fg_color=("#BF3C3A", "#8D211F"), hover_color=("#823332", "#5E1514"))



class TWOISLogCommentFrame(ctk.CTkFrame):
    """Yo!"""
    def __init__(self, master: ctk.CTk | ctk.CTkToplevel | ctk.CTkFrame |
                 ctk.CTkScrollableFrame, workorder: WorkOrder):
        super().__init__(master=master)
        self.workorder = workorder
        self.grid_rowconfigure(4, weight=1)
        num_lbl: ctk.CTkLabel = ctk.CTkLabel(self,
                                               text=self.workorder.get_full_workorder_number(),
                                               font=ctk.CTkFont(size=20, weight="bold"))
        title_lbl: ctk.CTkLabel = ctk.CTkLabel(self, text='Log Comments')


        log_str: str = ""
        for i, log in enumerate(self.workorder.comments):
            log_str += str(log)
            if i < len(self.workorder.comments) - 1:
                log_str += "\n"
        if log_str == "":
            log_str = "No log comments provided."

        self.logcmts: ctk.CTkLabel = ctk.CTkLabel(self, anchor='w', text=log_str, justify='left',
                                             wraplength=WRAP_LEN)

        self.logentry: ctk.CTkEntry = ctk.CTkEntry(self, placeholder_text="Enter a log comment")
        self.logentry.bind("<Return>", partial(self.add_log_comment))


        btnframe: ctk.CTkFrame = ctk.CTkFrame(self)
        btnframe.grid_columnconfigure(1, weight=1)
        self.submit_btn: ctk.CTkButton = ctk.CTkButton(btnframe, text='Add Log', width=BTN_W,
                                                       command=self.add_log_comment)
        self.return_btn: ctk.CTkButton = ctk.CTkButton(btnframe, text='Return', width=BTN_W)

        num_lbl.grid(       row=0, column=0, padx=20, pady=(10,2), sticky='ew')
        title_lbl.grid(     row=1, column=0, padx=20, pady=(0,20), sticky='ew')
        self.logcmts.grid(  row=2, column=0, padx=20, pady=5, sticky='ew')
        self.logentry.grid( row=5, column=0, padx=25, pady=20, sticky='ew')
        btnframe.grid(      row=6, column=0, padx=20, pady=10, sticky='ew')


        self.submit_btn.grid( row=0, column=0, padx=(50,0), pady=10, sticky='w')
        self.return_btn.grid( row=0, column=2, padx=(0,50), pady=10, sticky='e')

    def add_log_comment(self, *args) -> None: #pylint: disable=unused-argument
        """Yo!"""
        if len(self.logentry.get()) < 1:
            return
        new_cmt: LogComment = LogComment(self.logentry.get(), primary_user.name, date.today(),
                                               len(self.workorder.comments))
        if not self.workorder.log_comment([new_cmt]):
            reason: str = ""
            if len(self.workorder.comments) >= 24:
                reason = "The log comment list is full."
            else:
                reason = "There is some sort of discrepancy with the log comment rows."
            messagebox.showerror("Log Failure",
                                 (f"Could not add comment '{new_cmt.text}' to the log comment ",
                                  f"list. {reason}"))
            return

        logstr = self.logcmts.cget('text') + f"\n{new_cmt}"
        self.logcmts.configure(text=logstr)
        self.logentry.delete(0, END)
        self.logcmts.focus()
        self.workorder.save()
