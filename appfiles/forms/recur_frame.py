"""Yo!"""

# import random as rng
# from datetime import date
# from typing import Callable
import customtkinter as ctk #type: ignore

from appfiles.widgets.recur_item import RecurringTaskPanel
from appfiles.library.recurringtask import RecurringTask
# from appfiles.library.workorder import WorkOrder
# from appfiles.library.taskitem import TaskItem

class RecurringTaskFrame(ctk.CTkScrollableFrame):
    """Yo!"""
    def __init__(self, master: ctk.CTk | ctk.CTkToplevel | ctk.CTkFrame):
        super().__init__(master=master)
        self.tasks: list[RecurringTask] = self.__DELETE_THIS__generate_fake_recurtasks()
        self.panels: list[RecurringTaskPanel] = []

        for i, task in enumerate(self.tasks):
            panel: RecurringTaskPanel = RecurringTaskPanel(self, task)
            py = 5
            if i == 0:
                py = (20,5)
            if i == len(self.tasks) - 1:
                py = (5,20)
            panel.grid(row=i, column=0, padx=20, pady=py, sticky='ew')
            self.panels.append(panel)



    def __DELETE_THIS__generate_fake_recurtasks(self) -> list[RecurringTask]: #pylint: disable=invalid-name
        resp: list[RecurringTask] = []
        # system: list[str] = ["OSB GMM", "Test GMM", "CVA Laptops", "AV Laptops", "BSAT"]
        # desc_str: str = ""
        # with open('lorem_ipsum.txt', mode='r', encoding='utf-8') as file:
        #     desc_str = file.read()

        # for i in range(1, 11):
        #     month: int = date.today().month + rng.randint(0,1)
        #     day: int = date.today().day + rng.randint(-3,3)
        #     _sys: str = system[rng.randint(0,len(system) - 1)]
        #     wo: WorkOrder = WorkOrder(
        #         wo_number=f"{543000 + i}",
        #         title="Antivirus (AV) Update",
        #         room=i, description=f"{str(i).rjust(2,'0')} - {desc_str}",
        #         task_list=[TaskItem((i+0)*10, f"Task number {i+0} ttt",
        #                             f"Ref number {i+0}", i+16),
        #                    TaskItem((i+1)*10, f"Task number {i+1} tttttt",
        #                             f"Ref number {i+1}", i+17),
        #                    TaskItem((i+2)*10, f"Task number {i+2} ttttttttt",
        #                             f"Ref number {i+2}", i+18)])
        #     resp.append(RecurringTask(template=wo, due_date=date(2024,month,day),
        #                               title=wo.title, sys=_sys, cycle=rng.randint(1,10)))
        # resp.sort(key=lambda task: task.due_date)
        # resp.sort(key=lambda task: task.system)
        return resp
