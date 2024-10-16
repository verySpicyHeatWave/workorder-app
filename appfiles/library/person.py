from enum import Enum

from appfiles.utils.utils import name_to_initials

class Group(Enum):
    SA = 0
    ISSO = 1
    PC = 2

class Person:
    def __init__(self, name: str, email: str, group: Group,technician: bool, bems: int = -1):
        self.name: str = name
        self.email: str = email
        self.group: Group = group
        self.is_technician: bool = technician
        self.bems: int = bems

    def __repr__(self) -> str:
        names = self.name.split(" ")
        return f"{name_to_initials(self.name)[0]}. {names[-1]} / {self.bems}"


def get_persons_list_by_group(people: list[Person], grp: Group) -> list[Person]:
    resp: list[Person] = []
    for person in people:
        if person.group == grp: resp.append(person)
    return resp


def get_technicians_list(people: list[Person]) -> list[Person]:
    resp: list[Person] = []
    for person in people:
        if person.is_technician: resp.append(person)
    return resp
