#pylint: skip-file

from typing import TypedDict
from customtkinter import StringVar, IntVar, BooleanVar #type: ignore

from appfiles.library.taskitem import TaskItem

class WorkOrderFormDict(TypedDict):
    """A typed dictionary used as a var holder for the CTk "Var" objects that will store
      all of the WorkOrder data held in the associated widgets.
      """

    #BCOBB: Load default values into these
    site: StringVar
    special: StringVar
    type: StringVar
    priority: IntVar
    creator: StringVar
    building: StringVar
    room: StringVar
    related_wo: StringVar
    pac_required: BooleanVar
    ncr_required: BooleanVar
    ncr_number: StringVar
    task_lead_required: BooleanVar
    tech_witness_point: BooleanVar
    peer_review_required: BooleanVar
    peer_review_attached: BooleanVar
    ehs_required: BooleanVar
    qamip: BooleanVar
    qa_review_required: BooleanVar
    task_list: list[TaskItem]
    