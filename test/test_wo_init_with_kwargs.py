"""This test file is meant to ensure that a workorder object being generated from an Excel
spreadsheet will correctly parse and populate its fields based on the contents of that
spreadsheet.
"""

# pylint: skip-file

# import os
import unittest
# from datetime import date

# from openpyxl import Workbook, load_workbook
# from openpyxl.worksheet.worksheet import Worksheet

from appfiles.library.site import Site
from appfiles.library.special import Special
# from app.lib.workorder_type import WorkOrderType
from appfiles.library.workorder import WorkOrder
from appfiles.utils.appglobals import IN_PROGRESS_DIR
from appfiles.utils.utils_for_testing import clear_dir


class WorkOrderKWArgsTests(unittest.TestCase):
    """For testing the description field of the work order class"""
    def test_description__clamps_to_max_len(self) -> None:
        """Make sure the description string caps at the max length."""
        desc_str: str = ""
        with open('lorem_ipsum.txt', mode='r', encoding='utf-8') as file:
            desc_str = file.read()
        desc_limit = desc_str[:WorkOrder.MAX_DESCRIPTION]
        test_wo: WorkOrder = WorkOrder(description=desc_str)
        self.assertEqual(desc_limit, test_wo.description)
        self.assertEqual(len(test_wo.description), WorkOrder.MAX_DESCRIPTION)


    def test_description__is_default_if_left_blank(self) -> None:
        """Make sure the description defaults if not provided."""
        test_wo: WorkOrder = WorkOrder()
        self.assertEqual(test_wo.description, WorkOrder.DEFAULT_DESCRIPTION)


    def test_wo_number__accepts_valid_wo_number1(self) -> None:
        """Make sure a work order number is properly accepted if valid."""
        num: str = "053089"
        test_wo: WorkOrder = WorkOrder(wo_number=num)
        self.assertEqual(test_wo.get_full_workorder_number(), f"{num}VBS")


    def test_wo_number__accepts_valid_wo_number2(self) -> None:
        """Make sure a work order number is properly accepted if valid."""
        num: str = "415269FDI"
        test_wo: WorkOrder = WorkOrder(wo_number=num, site=Site.FD, special=Special.I)
        self.assertEqual(test_wo.get_full_workorder_number(), num)


    def test_wo_number__properly_uses_site_and_special_attributes1(self) -> None:
        """Make sure a work order number appropriately uses the site and special attributes."""
        num: str = "415269VBS"
        test_wo: WorkOrder = WorkOrder(wo_number=num, site=Site.FD, special=Special.I)
        self.assertEqual(test_wo.get_full_workorder_number(), "415269FDI")


    def test_wo_number__properly_uses_site_and_special_attributes2(self) -> None:
        """Make sure a work order number appropriately uses the site and special attributes."""
        num: str = "415269"
        test_wo: WorkOrder = WorkOrder(wo_number=num, site=Site.FD, special=Special.I)
        self.assertEqual(test_wo.get_full_workorder_number(), "415269FDI", )


    def test_wo_number__defaults_to_pending_if_blank(self) -> None:
        """Make sure a work order number is Pending if left blank."""
        clear_dir(IN_PROGRESS_DIR)
        num: str = ""
        test_wo: WorkOrder = WorkOrder(wo_number=num, site=Site.FD, special=Special.I)
        self.assertEqual(test_wo.get_full_workorder_number(), "Pending-001")


    def test_wo_number__defaults_to_pending_multiple_times_if_blank(self) -> None:
        """Make sure a work order number is  if left blank or not provided."""
        clear_dir(IN_PROGRESS_DIR)
        num: str = ""
        for i in range(4):
            WorkOrder(priority=i).save()
        test_wo: WorkOrder = WorkOrder(wo_number=num, site=Site.FD, special=Special.I)
        self.assertEqual(test_wo.get_full_workorder_number(), "Pending-005")


    def test_wo_number__defaults_to_pending_if_bad_string(self) -> None:
        """Make sure a work order number is Pending if the string doesn't make sense."""
        clear_dir(IN_PROGRESS_DIR)
        num: str = "WHAT?!?!"
        test_wo: WorkOrder = WorkOrder(wo_number=num, site=Site.FD, special=Special.I)
        self.assertEqual(test_wo.get_full_workorder_number(), "Pending-001")


    def test_title__populates_correctly(self) -> None:
        """Checks to see if the title value populates correctly"""
        t: str = "14 Day AV Updates (OPS GMM)"
        test_wo: WorkOrder = WorkOrder(title=t)
        self.assertEqual(test_wo.title, t)


    def test_title__truncates_if_too_long(self) -> None:
        """Checks to see if the title will be truncated to max characters if the string contents
        are too long."""
        t: str = "Lorem ipsum dolor sit amet consectetur adipiscing elit "
        t += "sed do eiusmod tempor incididunt ut labore et dolore magna aliqua"
        title_limit: str = t[:WorkOrder.MAX_TITLE]
        test_wo: WorkOrder = WorkOrder(title=t)
        self.assertEqual(test_wo.title, title_limit)
        self.assertEqual(len(test_wo.title), WorkOrder.MAX_TITLE)


    def test_title__cleans_up_for_file_path(self) -> None:
        """Checks to see if the object will modify the title and remove characters that shouldn't
        be in a system filepath."""
        t: str = "This is a f%$#@<>! crazy string wow"
        t_fixed: str = "This is a f crazy string wow"
        test_wo: WorkOrder = WorkOrder(title=t)
        self.assertEqual(test_wo.title, t_fixed)


    def test_title__is_default_if_left_blank(self) -> None:
        test_wo: WorkOrder = WorkOrder()
        self.assertEqual(test_wo.title, WorkOrder.DEFAULT_TITLE)


    def test_priority__populates_correctly(self) -> None:
        test_wo: WorkOrder = WorkOrder(priority=2)
        self.assertEqual(test_wo.priority, 2)


    def test_priority__is_default_if_left_blank(self) -> None:
        test_wo: WorkOrder = WorkOrder()
        self.assertEqual(test_wo.priority, 3)


    def test_priority__is_default_if_too_low(self) -> None:
        test_wo: WorkOrder = WorkOrder(priority=0)
        self.assertEqual(test_wo.priority, 3)


    def test_priority__is_default_if_too_high(self) -> None:
        test_wo: WorkOrder = WorkOrder(priority=4)
        self.assertEqual(test_wo.priority, 3)


    def test_building__populates_correctly(self) -> None:
        test_wo: WorkOrder = WorkOrder(building=1000)
        self.assertEqual(test_wo.building, 1000)


    def test_building__is_default_if_left_blank(self) -> None:
        test_wo: WorkOrder = WorkOrder()
        self.assertEqual(test_wo.building, 1768)


    def test_building__is_default_if_too_low(self) -> None:
        test_wo: WorkOrder = WorkOrder(building=9)
        self.assertEqual(test_wo.building, 1768)


    def test_building__is_default_if_too_high(self) -> None:
        test_wo: WorkOrder = WorkOrder(building=100_000)
        self.assertEqual(test_wo.building, 1768)


    def test_room__populates_correctly(self) -> None:
        test_wo: WorkOrder = WorkOrder(room=21)
        self.assertEqual(test_wo.room, 21)


    def test_room__is_default_if_left_blank(self) -> None:
        test_wo: WorkOrder = WorkOrder()
        self.assertEqual(test_wo.room, 6)


    def test_room__is_default_if_too_low(self) -> None:
        test_wo: WorkOrder = WorkOrder(room=0)
        self.assertEqual(test_wo.room, 6)


    def test_room__is_default_if_too_high(self) -> None:
        test_wo: WorkOrder = WorkOrder(room=1_000)
        self.assertEqual(test_wo.room, 6)

    
    def test_related_wo__accepts_valid_wo_number1(self) -> None:
        """Make sure a related work order number is properly accepted if valid."""
        num: str = "053089"
        test_wo: WorkOrder = WorkOrder(wo_number=num)
        self.assertEqual(test_wo.get_full_workorder_number(), f"{num}VBS")


    def test_related_wo__accepts_valid_wo_number2(self) -> None:
        """Make sure a related work order number is properly accepted if valid."""
        num: str = "415269FDI"
        test_wo: WorkOrder = WorkOrder(related_wo=num, site=Site.FD, special=Special.I)
        self.assertEqual(test_wo.related_wo, num)


    def test_related_wo__properly_uses_site_and_special_attributes1(self) -> None:
        """Make sure a related work order number DOES NOT use the site and special attributes."""
        num: str = "415269VBS"
        test_wo: WorkOrder = WorkOrder(related_wo=num, site=Site.FD, special=Special.I)
        self.assertEqual(test_wo.related_wo, num)


    def test_related_wo__properly_uses_site_and_special_attributes2(self) -> None:
        """Make sure a related work order number DOES NOT use the site and special attributes."""
        num: str = "415269"
        test_wo: WorkOrder = WorkOrder(related_wo=num, site=Site.FD, special=Special.I)
        self.assertEqual(test_wo.related_wo, num)


    def test_related_wo__defaults_to_na_if_blank(self) -> None:
        """Make sure a work related order number is 'N/A' if left blank."""
        num: str = ""
        test_wo: WorkOrder = WorkOrder(related_wo=num, site=Site.FD, special=Special.I)
        self.assertEqual(test_wo.related_wo, "N/A")


    def test_related_wo__defaults_to_na_if_not_specified(self) -> None:
        """Make sure a related work order number is 'N/A' if left blank."""
        test_wo: WorkOrder = WorkOrder()
        self.assertEqual(test_wo.related_wo, "N/A")


    def test_related_wo__defaults_to_na_if_bad_string(self) -> None:
        """Make sure a work order number is n/a if the string doesn't make sense."""
        num: str = "WHAT?!?!"
        test_wo: WorkOrder = WorkOrder(related_wo=num, site=Site.FD, special=Special.I)
        self.assertEqual(test_wo.related_wo, "N/A")


    def test_ncr_number__takes_a_valid_number1(self) -> None:
        num: str = 'NCR123456w'
        test_wo: WorkOrder = WorkOrder(ncr_number=num, ncr_required=True)
        self.assertEqual(test_wo.ncr_number, num)


    def test_ncr_number__takes_a_valid_number2(self) -> None:
        num: str = 'ncr123456w'
        test_wo: WorkOrder = WorkOrder(ncr_number=num, ncr_required=True)
        self.assertEqual(test_wo.ncr_number, num)


    def test_ncr_number__defaults_if_not_supplied(self) -> None:
        test_wo: WorkOrder = WorkOrder(ncr_required=True)
        self.assertEqual(test_wo.ncr_number, 'REQUIRED')


    def test_ncr_number__defaults_if_bad_string(self) -> None:
        num: str = 'BITE IT YOU SCUM'
        test_wo: WorkOrder = WorkOrder(ncr_number=num, ncr_required=True)
        self.assertEqual(test_wo.ncr_number, 'REQUIRED')


    def test_ncr_number__defaults_with_valid_number_not_required1(self) -> None:
        num: str = 'NCR123456w'
        test_wo: WorkOrder = WorkOrder(ncr_number=num, ncr_required=False)
        self.assertEqual(test_wo.ncr_number, 'N/A')


    def test_ncr_number__defaults_with_valid_number_not_required2(self) -> None:
        num: str = 'ncr123456w'
        test_wo: WorkOrder = WorkOrder(ncr_number=num, ncr_required=False)
        self.assertEqual(test_wo.ncr_number, 'N/A')


    def test_ncr_number__defaults_if_not_supplied_not_required(self) -> None:
        test_wo: WorkOrder = WorkOrder(ncr_required=False)
        self.assertEqual(test_wo.ncr_number, 'N/A')


    def test_ncr_number__defaults_if_bad_string_not_required(self) -> None:
        num: str = 'BITE IT YOU SCUM'
        test_wo: WorkOrder = WorkOrder(ncr_number=num, ncr_required=False)
        self.assertEqual(test_wo.ncr_number, 'N/A')


if __name__ == '__main__':
    unittest.main()
