"""Yo!"""

from dataclasses import dataclass
from datetime import date

class WorkorderCompletionData():
    """Yo!"""
    def __init__(self, startdate: date, enddate: date, restoredate: date, repairtime: str) -> None:
        self.startdate: date = startdate
        self.enddate: date = enddate
        self.restoredate: date = restoredate

        rtlist: list[str] = repairtime.split(":")

        for i, item in enumerate(rtlist):
            if not item.isdigit():
                rtlist[i] = '0'

        self.minutes: int = int(rtlist[len(rtlist) - 1])
        self.hours: int = int(rtlist[len(rtlist) - 2])
        self.days: int = 0 if len(rtlist) < 3 else int(rtlist[0])

    def __str__(self) -> str:
        resp: str = ""
        if self.days > 0:
            resp += str(self.days) + "d, "
        if self.hours > 0:
            resp += str(self.hours) + "h, "
        if self.minutes > 0:
            resp += str(self.minutes) + "m"
        return resp

@dataclass
class TaskCompletionData():
    """Yo!"""
    def __init__(self, cdate: date, tech: str, qty_techs: int, hours: float):
        self.cdate = cdate
        self.tech = tech
        self.qty_techs = qty_techs
        self.hours = hours
    