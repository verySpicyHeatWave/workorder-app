"""Yo!"""

from functools import partial
import os
import random as rng
from datetime import date
from tkinter import Event, messagebox
import customtkinter as ctk #type: ignore

from appfiles.forms.complete_form import CompletionForm
from appfiles.forms.workorder_form import WorkOrderForm, WorkOrderFormMode
from appfiles.library.logcomment import LogComment
from appfiles.widgets.twois_detail import TWOISDetailButton, TWOISDetailFrame, TWOISLogCommentFrame
from appfiles.library.workorder import WorkOrder
from appfiles.library.taskitem import TaskItem
from appfiles.library.excelfilestatus import ExcelFileStatus

class TWOISStatusFrame(ctk.CTkFrame):
    """Yo!"""
    def __init__(self, master: ctk.CTk | ctk.CTkToplevel | ctk.CTkFrame):
        super().__init__(master=master)

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.button_scrframe: ctk.CTkScrollableFrame = ctk.CTkScrollableFrame(self, width=360)
        self.button_scrframe.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')
        self.detail_frame: ctk.CTkFrame = TWOISDetailFrame(self, WorkOrder())

        self.workorders: list[WorkOrder] = self.load_workorders()
        self.buttons: list[TWOISDetailButton] = self.__create_twois_buttons()
        self.active_workorder: WorkOrder = WorkOrder()
        self.__hide_workorder_details()


    def refresh_contents(self) -> None:
        """A method which clears out all of the workorder buttons, reloads the workorders,
        and then repopulates the buttons."""
        self.__hide_workorder_details()
        for btn in self.buttons:
            btn.grid_forget()
        self.buttons.clear()
        self.workorders = self.load_workorders()
        self.buttons = self.__create_twois_buttons()
        self.active_workorder = WorkOrder()


    def load_workorders(self) -> list[WorkOrder]:
        """A method which looks in the 'in progress' directory and loads all of the serialized
        WorkOrder files stores in .twois files into memory and returns them as a single list."""
        #BCOBB: Implement--make it load from the real workorders directory
        return self.__DELETE_THIS__generate_fake_workorders()


    def complete_workorder(self) -> None:
        """A method which produces a dialog window used for completing an existing workorder."""
        print("BCOBB: TODO! - Complete method")
        cmpform: CompletionForm = CompletionForm(self, self.active_workorder)
        cmpform.bind("<Destroy>", self.__refresh_contents_event_handler)


    def approve_workorder(self) -> None:
        """A method which produces an openfiledialog used for finding an approved workorder."""
        desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
        file: str = ctk.filedialog.askopenfilename(initialdir=desktop,
                                                   filetypes=(("Excel files", ["*.xlsx", "*.xls"]),
                                                              ("All files", "*.*")))
        badfile: str = "File Selection Error"
        fstat = self.active_workorder.approve(filename=file)

        # fstat = approved_file_status(file)
        if fstat == ExcelFileStatus.NOT_XLSX:
            messagebox.showerror(badfile, "This file is not a Microsoft Excel file!")
            return
        elif fstat == ExcelFileStatus.NOT_TWOIS:
            messagebox.showerror(badfile, "This file is not a TWOIS file!")
            return
        elif fstat == ExcelFileStatus.NOT_COMPLETE:
            messagebox.showerror(badfile, "This file is not completely filled out!")
            return
        elif fstat == ExcelFileStatus.NOT_APPROVED:
            messagebox.showerror(badfile, "This file is not actually approved!")
            return
        elif fstat == ExcelFileStatus.FILES_UNMATCHED:
            msg: str = ("This file doesn't seem to match the selected workorder. "
            "Approve it anyway?\n"
            "Note: This will erase the existing workorder data ."
            "It will be replaced by the data in the Excel file.")
            approve = messagebox.askyesno(badfile, msg)
            if approve:
                self.active_workorder.approve(filename=file, override=True)
        self.refresh_contents()


    def edit_workorder(self) -> None:
        """A method which produces a dialog window used for editing/creating a workorder."""
        woform: WorkOrderForm = WorkOrderForm(self, WorkOrderFormMode.EDIT, self.active_workorder)
        woform.bind("<Destroy>", self.__refresh_contents_event_handler)
        # self.refresh_contents()


    def delete_workorder(self) -> None:
        """A method which produces a message dialog window to ask whether a user wants to
        delete a workorder or not."""
        msg: str = ("Are you sure you want to delete this workorder? "
                    "Once it's deleted, it will be unretrievable.\n"
                    "If you want to retain the file but remove it from tracking, "
                    "an alternate solution is to go into the in_progress "
                    "directory and move the .twois and .xlsx files elsewhere.")
        user_is_absolutely_fucking_sure = messagebox.askyesno("Delete File", msg)
        if user_is_absolutely_fucking_sure:
            self.active_workorder.delete()
        self.refresh_contents()


    # def __show_workorder_details_getlambda(self, wo: WorkOrder) -> Callable:
    #     return lambda ev:self.__show_workorder_details(wo)


    def __refresh_contents_event_handler(self, e: Event):
        if isinstance(e.widget, WorkOrderForm) or isinstance(e.widget, CompletionForm):
            self.refresh_contents()



    def __hide_workorder_details(self) -> None:
        self.detail_frame.grid_forget()
        self.detail_frame = ctk.CTkFrame(self, width=200)
        self.detail_frame.grid_rowconfigure((0,2), weight=1)
        self.detail_frame.grid_columnconfigure((0,2), weight=1)
        ctk.CTkLabel(self.detail_frame, text="Click a workorder to show the details here.",
                     font=ctk.CTkFont(size=20, weight='bold'),
                     wraplength=200).grid(row=1, column=1, sticky='ew')
        self.detail_frame.grid(row=0, column=1, padx=10, pady=10, sticky='nsew')


    def __show_workorder_details(self, wo: WorkOrder) -> None:
        self.detail_frame.grid_forget()
        self.active_workorder = wo
        self.detail_frame = TWOISDetailFrame(self, self.active_workorder)
        self.detail_frame.grid(row=0, column=1, padx=10, pady=10, sticky='nsew')

        if self.active_workorder.is_approved(False):
            self.detail_frame.actn_btn.configure(command=self.complete_workorder)
        else:
            self.detail_frame.actn_btn.configure(command=self.approve_workorder)
        self.detail_frame.hide_btn.configure(command=self.__hide_workorder_details)
        self.detail_frame.del_btn.configure(command=self.delete_workorder)
        self.detail_frame.edit_btn.configure(command=self.edit_workorder)
        self.detail_frame.logs_btn.configure(command=self.show_log_comments)


    def show_log_comments(self) -> None:
        """Yo!"""
        self.detail_frame.grid_forget()
        self.detail_frame = TWOISLogCommentFrame(self, self.active_workorder)
        self.detail_frame.grid(row=0, column=1, padx=10, pady=10, sticky='nsew')
        # self.detail_frame.return_btn.configure(
        #     command=self.__show_workorder_details(self.active_workorder))
        self.detail_frame.return_btn.configure(
            command=partial(self.__show_workorder_details, self.active_workorder))


    def __create_twois_buttons(self) -> list[TWOISDetailButton]:
        for i, wo in enumerate(self.workorders):
            resp: list[TWOISDetailButton] = []
            btn: TWOISDetailButton = TWOISDetailButton(self.button_scrframe, wo)
            btn.configure(command=partial(self.__show_workorder_details, wo))
            # btn.bind("<Button-1>", self.__show_workorder_details_getlambda(wo))
            btn.grid(row=i, column=0, padx=20, pady=10, sticky="ew")
            resp.append(btn)
        return resp


    def __DELETE_THIS__generate_fake_workorders(self) -> list[WorkOrder]: #pylint: disable=invalid-name
        resp: list[WorkOrder] = []
        desc_str: str = ""
        with open('lorem_ipsum.txt', mode='r', encoding='utf-8') as file:
            desc_str = file.read()

        for i in range(1, 11):
            month: int = date.today().month + rng.randint(-1,2)
            ddd = date(2024,month,(rng.randint(1,28)))
            wo: WorkOrder = WorkOrder(
                wo_number=f"{543000 + i}",
                title=f"{str(i).rjust(2, '0')}-Day Antivirus (AV) Update{'t'*(i-1)*5}",
                due_date=ddd, room=rng.randint(1,3),
                description=f"{str(i).rjust(2,'0')} - {desc_str}",
                task_list=[TaskItem((i+0)*10, f"Task number {i+0} ttt",
                                    f"Ref number {i+0}", i+16),
                           TaskItem((i+1)*10, f"Task number {i+1} tttttt",
                                    f"Ref number {i+1}", i+17),
                           TaskItem((i+2)*10, f"Task number {i+2} ttttttttt",
                                    f"Ref number {i+2}", i+18)],
                comments=[LogComment(f"This is log comment number {i+0}",
                                     "Brian Cobb", ddd, 0),
                          LogComment(f"This is log comment number {i+1}",
                                     "Brian Cobb", ddd, 1),
                          LogComment("This is a really really fucking long and detailed log comment",
                                     "Brian Cobb", ddd, 2)])
            resp.append(wo)
        resp.sort(key=lambda twois: twois.due_date)
        return resp
