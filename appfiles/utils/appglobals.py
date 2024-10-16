"""BCOBB: placeholder docstring"""

import os
from appfiles.library.person import Person, Group
from appfiles.library.site import Site
from appfiles.library.special import Special
from appfiles.library.workorder_type import WorkOrderType

# Global Constants
USERHOME: str = "\\Users\\" + os.getlogin() + "\\Desktop"
IN_PROGRESS_DIR: str = os.getcwd() + "\\data\\in_progress"
COMPLETE_DIR: str = os.getcwd() + "\\data\\complete"
TEMPLATE_DIR: str = os.getcwd() + "\\data\\templates"
TEMPLATE_TWOIS: str = os.getcwd() + "\\appfiles\\res\\TWOIS_template-3-20.xlsx"
TESTFILE: str = os.getcwd() + "\\appfiles\\res\\testfile.xlsx"
FONTSIZE: int = 9
NUMROWS: int = 1



# Configuration Information
#BCOBB: Make everything in this section configurable
#BCOBB: Add the list of recurring tasks
primary_user: Person = Person("Brian Cobb", "brian.n.cobb@boeing.com",
                               Group.SA, True, 3677837)

default_building: int = 1768
default_room: int = 6
default_site: Site = Site.VB
default_special: Special = Special.S
default_wotype: WorkOrderType = WorkOrderType.OTH



people: list[Person] = [primary_user,
                        Person("Joel DeLeon", "joel.deleon@boeing.com",
                               Group.SA, True, 3667293),
                        Person("Jose Lopez", "jose.m.lopez8@boeing.com",
                               Group.SA, True, 3421099),
                        Person("Michael Mora", "michael.a.mora@boeing.com",
                               Group.ISSO, False),
                        Person("Fiorela Silva-Hurst", "fiorela.c.silvahurst@boeing.com",
                               Group.PC, False)]



