from enum import Enum
from typing import Self

class Site(Enum):
    """A class which represents all of the available Site options, as well as a special
    static method called parse(), which receives a string and returns an enum member.

    Members
    --------
        FG = 0 (Fort Greely Army Base)\n
        VB = 1 (Vandenberg Space Force Base)\n
        CS = 2 (Colorado Springs sites)\n
        EA = 3 (Eareckson Air Station)\n
        FD = 4 (Fort Drum)\n
        SX = 5 (Sea-Based X-Band)\n
        FY = 6 (Royal Air Force, UK)\n
        CL = 7 (Clear Space Force Station)\n
        BL = 8 (Beale Air Force Base)\n
        TH = 9 (Thule Air Station, Greenland)
    """
    FG = 0
    VB = 1
    CS = 2
    EA = 3
    FD = 4
    SX = 5
    FY = 6
    CL = 7
    BL = 8
    TH = 9

    @staticmethod
    def parse(string: str) -> Self: #type:ignore
        """
        Method takes in a case-insensitive string and returns the appropriate Enum
        member as a response. If the string is not a member, it will return a
        user-defined default member.
        
        Examples
        ----------------
        >>> Site.parse('VB')
        Site.VB
        >>> Site.parse('fy')
        Site.FY
        >>> Site.parse('Willy Wonka')
        {default site}
        """
        s = string.upper()
        if s in Site.__members__:
            return Site[s] #type:ignore
        return default_site #type:ignore
    
default_site: Site = Site.VB