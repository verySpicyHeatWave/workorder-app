# pylint: skip-file

import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from appfiles.library.site import Site, default_site
from appfiles.library.special import Special, default_special
from appfiles.library.workorder_type import WorkOrderType, default_wotype

class SiteEnumTests(unittest.TestCase):
    def test_parse_function_default1(self) -> None:
        s: Site = Site.parse("Vn")
        self.assertEqual(s, default_site)
    
    def test_parse_function_default2(self) -> None:
        s: Site = Site.parse("boom")
        self.assertEqual(s, default_site)
    
    def test_parse_function_default3(self) -> None:
        s: Site = Site.parse("Fort Greely")
        self.assertEqual(s, default_site)
    
    def test_parse_function_FG(self) -> None:
        s: Site = Site.parse("FG")
        self.assertEqual(s, Site.FG)
    
    def test_parse_function_VB(self) -> None:
        s: Site = Site.parse("VB")
        self.assertEqual(s, Site.VB)
    
    def test_parse_function_CS(self) -> None:
        s: Site = Site.parse("CS")
        self.assertEqual(s, Site.CS)
    
    def test_parse_function_EA(self) -> None:
        s: Site = Site.parse("EA")
        self.assertEqual(s, Site.EA)
    
    def test_parse_function_FD(self) -> None:
        s: Site = Site.parse("FD")
        self.assertEqual(s, Site.FD)
    
    def test_parse_function_SX(self) -> None:
        s: Site = Site.parse("SX")
        self.assertEqual(s, Site.SX)
    
    def test_parse_function_FY(self) -> None:
        s: Site = Site.parse("FY")
        self.assertEqual(s, Site.FY)
    
    def test_parse_function_CL(self) -> None:
        s: Site = Site.parse("CL")
        self.assertEqual(s, Site.CL)
    
    def test_parse_function_BL(self) -> None:
        s: Site = Site.parse("BL")
        self.assertEqual(s, Site.BL)
    
    def test_parse_function_TH(self) -> None:
        s: Site = Site.parse("TH")
        self.assertEqual(s, Site.TH)

    def test_parse_function_lowercase(self) -> None:
        s: Site = Site.parse("fg")
        self.assertEqual(s, Site.FG)



class SpecialEnumTests(unittest.TestCase):
    def test_parse_function_default1(self) -> None:
        s: Special = Special.parse("A")
        self.assertEqual(s, default_special)
    
    def test_parse_function_default2(self) -> None:
        s: Special = Special.parse("boom")
        self.assertEqual(s, default_special)
    
    def test_parse_function_default3(self) -> None:
        s: Special = Special.parse("ISSO")
        self.assertEqual(s, default_special)
    
    def test_parse_function_S(self) -> None:
        s: Special = Special.parse("S")
        self.assertEqual(s, Special.S)
    
    def test_parse_function_I(self) -> None:
        s: Special = Special.parse("I")
        self.assertEqual(s, Special.I)
    
    def test_parse_function_N(self) -> None:
        s: Special = Special.parse("N")
        self.assertEqual(s, Special.N)

    def test_parse_function_lowercase(self) -> None:
        s: Special = Special.parse("i")
        self.assertEqual(s, Special.I)



class WorkOrderTypeEnumTests(unittest.TestCase):
    def test_parse_function_default1(self) -> None:
        s: WorkOrderType = WorkOrderType.parse("CN")
        self.assertEqual(s, default_wotype)
    
    def test_parse_function_default2(self) -> None:
        s: WorkOrderType = WorkOrderType.parse("boom")
        self.assertEqual(s, default_wotype)
    
    def test_parse_function_default3(self) -> None:
        s: WorkOrderType = WorkOrderType.parse("Preventative Maintenance")
        self.assertEqual(s, default_wotype)
    
    def test_parse_function_PM(self) -> None:
        s: WorkOrderType = WorkOrderType.parse("PM")
        self.assertEqual(s, WorkOrderType.PM)
    
    def test_parse_function_CM(self) -> None:
        s: WorkOrderType = WorkOrderType.parse("CM")
        self.assertEqual(s, WorkOrderType.CM)
    
    def test_parse_function_OTH(self) -> None:
        s: WorkOrderType = WorkOrderType.parse("OTH")
        self.assertEqual(s, WorkOrderType.OTH)

    def test_parse_function_lowercase(self) -> None:
        s: WorkOrderType = WorkOrderType.parse("cm")
        self.assertEqual(s, WorkOrderType.CM)

if __name__ == '__main__':
    unittest.main()