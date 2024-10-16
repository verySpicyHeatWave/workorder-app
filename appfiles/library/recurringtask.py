
from datetime import date, timedelta

from appfiles.library.workorder import WorkOrder

# BCOBB: Create a "routine task" class that will be used for standard scheduling
# (AV updates, scans, password updates, etc.) Description:
# BCOBB: ROUTINE TASK CLASS
#    fields::
#        due_date: date          //for display
#        task: str               //for display and sorting, e.g. "14-Day AV Updates, CVA Scan"
#        system: str             //for display and sorting, e.g. "GMDE GMM"
#        recurrence: int         //number of days between recurrences
#        template: str           //references a .twois object that can be used for quick work order generation.
#        history: list[str]      //stores a list of the work order numbers associated with this task


#     methods::
#         iterate_task(wo: WorkOrder) -> None:
#             (will call the update_due_date() function and add the workorder object's number to the list)

#         update_due_date() -> None:
#             (will increase the due date by 'r' number of days, where 'r' is the integer value of the recurrence field)

#         update_template() -> None:
#             (will update the workorder by passing the workorder some kwargs, maybe?)

#         get_template_workorder() -> WorkOrder:
#             will load the .twois file into a WorkOrder object and return it.

class RecurringTask:
    """A relatively simple class with a few fields which defines WorkOrders which are meant to
    be repeated.\n
    It does not inherit the WorkOrder class: instead, it stores a reference to a .twois file which
    acts as a template from which workorder objects are created.
    """
    def __init__(self, template: WorkOrder, due_date: date, title: str, sys: str, cycle: int):
        self.due_date: date = due_date
        self.title: str = title
        self.system: str = sys
        self.recur: int = cycle
        self.history: list[str] = []
        self.template_file = template.save_as_wo_template(f"{sys} - {cycle}")
        self.active_workorder: WorkOrder

    def __str__(self) -> str:
        resp: str = f"{self.recur}-Day {self.title} ({self.system})"
        return resp

    def iterate(self, wo: WorkOrder) -> None:
        """Signals the completion of the task"""
        self.history.append(wo.wo_number)
        self.update_due_date()

    #BCOBB: Finish this method
    def update_due_date(self) -> None:
        """Increase the due date by 'd' number of days, where 'd' is the integervalue of the
        recurrence field.
        """
        if self.due_date > date.today():
            return
        self.due_date += timedelta(days=self.recur)

    def update_template(self, wo: WorkOrder) -> None: #type:ignore
        """(will update the workorder by passing in a new work order object)"""
        wo.save_as_wo_template(self.template_file)

    #BCOBB: Finish this method (load .twois file into WO object and return the WO object)
    def get_template_workorder(self) -> WorkOrder:
        """will load the .twois file into a WorkOrder object and return it."""
        print("BCOBB: TO-DO! - Get workorder template from the recurring task")
        return WorkOrder()

        #BCOBB: Have enums to support the following:
        # recurring task type (AV scan, AV Update, CVA Scan, Root Password Update)
        # the system itself (GMDE GMM, OSB GMM, CSM, MSE, BSAT, AV Laptops, CVA Laptops, IFAS)
        # Preferably make them configurable and load them up from the global resources.
        #
        # An alternate option to using enums to store these would be to store them as lists of
        # strings which would then be serialized and loaded at runtime. The list would have to
        # populate into a tkinter Text object and then we would save them.
        #
        # The problem with using strings is that, if someone changes the string slightly, like
        # by removing a dash or space or by changing capitalization, parsing could get screwed up.
        # Behind the scenes, naming conventions would be screwed up. So maybe, instead, I would
        # display the list of strings but not allow them to be edited, then provide an entry
        # box which could just be used to add an item. Once an item is on the list, it can't be
        # removed or deleted. That's probably the best way.

        # Either way, I would use the string values to define the description:
        #       self.description = f"{self.recur}-Day {self.task_type.name} ({self.system.name})"
        #       e.g. "14-Day Antivirus Updates (OSB GMM)"

        # These also need to be serialized