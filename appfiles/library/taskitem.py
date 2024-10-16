from dataclasses import dataclass
from datetime import date

from appfiles.library.completiondata import TaskCompletionData
from appfiles.utils.utils import clamp

ARBITRARY_DATE: date = date(1989,5,30)

@dataclass
class TaskItem:
    """A data class which stores the basic information of a task item on a Work Order.
    Initially it only takes in a task number, summary, reference, and row number.
    It also holds completion data, including date, technician name, number of techs, and hours.
    Those won't get updated until 
    
    Fields
    ----------------
        number: int
            This is the task number, almost always a multiple of ten.

        summary: str
            This is a brief description of the task item.

        reference: str
            This is the number for the procedural document being referenced.

        planned_row: int
            This is the excel row that the entry goes on. Will be clamped between 15 and 29.
            
        actuals_row: int (not configurable)
            This is where the completion entry will be. Always 17 more than the planned row.
            
        completion_date: date
            This is the date that the task was actually completed. Defaults to an arbitrary
            date in the past.

        technician: str
            This is the name of the technician who is responsible for doing the work. Defaults
            to an empty string.

        qty_techs: int
            this is the number of technicians who actually did the work. Defaults to -1.

        self.hours: float
            This is the number of hours that the work took to complete. Needs to be in increments of
            0.1, Defaults to -1.0.
    """
    def __init__(self, task_number: int, summary: str, ref: str, row: int) -> None:
        self.number: int = task_number
        self.summary: str = summary
        self.reference: str = ref
        self.planned_row: int = clamp(row, 15, 29)
        self.actuals_row: int = row + 17
        self.completion_date: date = ARBITRARY_DATE
        self.technician: str = ""
        self.qty_techs: int = -1
        self.hours: float = -1.0

    def __str__(self) -> str:
        return self.summary

    def complete(self, data: TaskCompletionData) -> bool:
        """Applies completion data to the task item object."""
        if self.is_complete():
            return False
        self.completion_date = data.cdate
        self.technician = data.tech
        self.qty_techs = data.qty_techs
        self.hours = data.hours
        return True

    def is_complete(self) -> bool:
        """Checks if the workorder is complete by checking some completion values"""
        return self.qty_techs > 0 and self.hours > 0
