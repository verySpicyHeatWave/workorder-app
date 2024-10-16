"""General use utility functions"""

from datetime import date, timedelta
import os
import re

def name_to_initials(chars: str) -> str:
    """Takes a string and converts it into initials. Should receive a first and last name."""
    resp: list[str] = []
    for i, char in enumerate(chars):
        if i == 0 and char != " ":
            resp.append(char)
        if char == ' ' and chars[i+1].isalpha():
            resp.append(chars[i+1].upper())
        if not char.isalpha() and not char.isnumeric() and not char == ' ':
            break
    return "".join(resp)


def make_string_filepath_friendly(value: str) -> str:
    """Takes a string and removes characters that are not filepath-friendly, then returns it."""
    illegal_chars: list[str] = ['#', '%', '{', '}', '\\', '<', '>', '*', '?', '/',""
                                '$', '!', '\'', '\"', ':', '@', '+', '`', '|', '=', '^']
    return "".join(x for x in value if x not in illegal_chars)


def clamp(val: int, minval: int, maxval: int) -> int:
    """Limits the range of input 'val' to stay between 'minval' and 'maxval', inclusive."""
    return max(min(val, maxval), minval)


def is_within_bounds(val: int, minval: int, maxval: int) -> bool:
    """Returns true if 'val' is in between 'minval' and 'maxval', includive."""
    return minval <= val <= maxval


def bool_to_yes_no_string(val: bool) -> str:
    """Takes in a boolean and returns a 'Yes' or 'No' string."""
    return 'Yes' if val else 'No'


def yes_no_string_to_bool(val: str) -> bool:
    """Takes in a 'Yes' or 'No' string and returns a boolean."""
    return val.lower() == 'yes'


def create_dated_directories(base_dir: str, c_date: date) -> str:
    """Takes in a base directory as a string as well as a date object and creates
    a year directory within the base directory and a numbered 'Week of' directory within
    the year directory"""
    if not os.path.isdir(base_dir):
        os.mkdir(base_dir)

    MONDAY: int = 0                     #pylint: disable=invalid-name
    dirdate: date = c_date
    one_day: timedelta = timedelta(days=1)

    new_dir: str = os.path.join(base_dir, str(dirdate.year))
    if not os.path.isdir(new_dir):
        os.mkdir(new_dir)

    while dirdate.weekday() != MONDAY:
        dirdate -= one_day


    new_dir = os.path.join(new_dir, f'Week of {date_to_string(dirdate, "%m-%d")}')
    if not os.path.isdir(new_dir):
        os.mkdir(new_dir)

    return new_dir


def safe_rename(src: str, dest: str) -> None:
    """A method which takes in a source and destination file and determines whether or not a
    rename operation is safe, and then performs that operation if it is. Returns true if
    successful and false if not.
    """
    if os.path.exists(src) and not os.path.exists(dest):
        os.rename(src, dest)


def date_to_string(d: date, strformat: str = "%#m/%#d/%Y") -> str:
    """A method which takes in a date object and returns a formatted string."""
    return d.strftime(strformat)


def string_to_date(s: str) -> date:
    """A method which takes in a date object and returns a formatted string."""
    resp: date = date.today()    
    date_re = re.compile(r"\d{1,2}(/|\\)\d{1,2}(/|\\)\d{4}")
    reg = date_re.search(s)
    if reg is not None:
        ds: list[str] = str(reg.group()).split('/')
        resp = date(int(ds[2]), int(ds[0]), int(ds[1]))
    return resp


def is_a_valid_date_string(s: str, regex: str = r"\d{1,2}(/|\\)\d{1,2}(/|\\)\d{4}"):
    """A method which takes in a formatted date string and an optional regex pattern and returns
    a boolean describing whether the string matches the regular expresion."""
    date_re = re.compile(regex)
    reg = date_re.match(s)
    if reg is None:
        return False
    return True
