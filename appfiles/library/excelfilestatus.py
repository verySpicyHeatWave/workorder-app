from enum import Enum

class ExcelFileStatus(Enum):
    """A class which represents the result of attempting to analyze a potential TWOIS excel file.

    Members
    --------
    IS_VALID = 0\n
    NOT_FOUND = 1\n
    NOT_XLSX = 2\n
    NOT_TWOIS = 3\n
    NOT_COMPLETE = 4\n
    NOT_APPROVED = 5\n
    FILES_UNMATCHED = 6\n
    WO_ALREADY_APPROVED = 7
    """
    IS_VALID = 0
    NOT_FOUND = 1
    NOT_XLSX = 2
    NOT_TWOIS = 3
    NOT_COMPLETE = 4
    NOT_APPROVED = 5
    FILES_UNMATCHED = 6
    WO_ALREADY_APPROVED = 7
