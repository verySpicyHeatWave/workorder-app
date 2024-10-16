from datetime import date
from typing import TypedDict

from .logcomment import LogComment
from .site import Site
from .special import Special
from .taskitem import TaskItem
from .workorder_type import WorkOrderType

class WorkOrderDict(TypedDict):
    """A typed dictionary used as a kwargs interface for the WorkOrder class constructor
      and edit methods. Used to provide options for users to configure a workorder
      object while allowing for default values.
      """
    description: str
    due_date: date
    wo_number: str
    site: Site
    special: Special
    title: str
    type: WorkOrderType
    priority: int
    creator: str
    building: int
    room: int
    related_wo: str
    pac_required: bool
    ncr_required: bool
    ncr_number: str
    task_lead_required: bool
    tech_witness_point: bool
    peer_review_required: bool
    peer_review_attached: bool
    ehs_required: bool
    qamip: bool
    qa_review_required: bool
    task_list: list[TaskItem]
    comments: list[LogComment]
    