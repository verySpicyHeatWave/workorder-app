from dataclasses import dataclass
from datetime import date
from appfiles.utils.utils import clamp, date_to_string

@dataclass
class LogComment:
    """A data class which stores the basic information of a log comment on a Work Order.
    
    Fields
    ----------------
        comment: str
            This is the actual comment.

        person: Person
            This is the identity of the person who left the comment, as a Person object.

        date: date
            This is the date that the comment was left.

        row: int
            This is the excel row that the entry goes on. Will be clamped between 86 and 109.
            Mangled field, should not be used directly.
    """
    def __init__(self, text: str, person: str, c_date: date, listsize: int) -> None:
        self.text: str = text
        self.person: str = person
        self.date: date = c_date
        self.__row: int = clamp(listsize + 86, 86, 109)

    def __str__(self) -> str:
        return f"{date_to_string(self.date)}\t{self.text}"

    def set_row(self, newrow) -> None:
        """A method which will set the private row field to whatever is fed in, clamped between
        86 and 109.
        """
        self.__row = clamp(newrow,86, 109)

    def get_row(self) -> int:
        """A method which return the private row field."""
        return self.__row

