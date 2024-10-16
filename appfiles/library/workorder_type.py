from enum import Enum
from typing import Self

class WorkOrderType(Enum):
    """A class which represents all of the available work order types, as well as a
    special static method called parse(), which receives a string and returns an enum member.

    Members
    --------
        PM = 0 (Preventative Maintenance)\n
        CM = 1 (Corrective Maintenance)\n
        OTH = 2 (Other)
    """
    PM = 0
    CM = 1
    OTH = 2

    @staticmethod
    def parse(string: str) -> Self: #type:ignore
        """
        Method takes in a case-insensitive string and returns the appropriate Enum
        member as a response. If the string is not a member, it will return a
        user-defined default member.

        Examples
        ----------------
        >>> WorkOrderType.parse('pm')
        WorkOrderType.PM
        >>> WorkOrderType.parse('OTH')
        WorkOrderType.OTH
        >>> WorkOrderType.parse('Dwight Eisenhower')
        {default work order type}
        """
        s = string.upper()
        if s in WorkOrderType.__members__:
            return WorkOrderType[s] #type:ignore
        return default_wotype #type:ignore

default_wotype: WorkOrderType = WorkOrderType.OTH