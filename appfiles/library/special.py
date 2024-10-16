from enum import Enum
from typing import Self

class Special(Enum):
    """A class which represents all of the available 'Special' or Group options, as well as a
    special static method called parse(), which receives a string and returns an enum member.

    Members
    --------
        N = 0 (Northrop-Grumman)\n
        S = 1 (System Administrator)\n
        I = 2 (ISSO)
    """
    N = 0
    S = 1
    I = 2

    @staticmethod
    def parse(string: str) -> Self: #type:ignore
        """
        Method takes in a case-insensitive string and returns the appropriate Enum
        member as a response. If the string is not a member, it will return a
        user-defined default member.
        
        Examples
        ----------------
        >>> Special.parse('s')
        Special.S
        >>> Special.parse('N')
        Special.N
        >>> Special.parse('Tyler Durden')
        {default special}
        """
        s = string.upper()
        if s in Special.__members__:
            return Special[s] #type:ignore
        return default_special #type:ignore

default_special: Special = Special.S
