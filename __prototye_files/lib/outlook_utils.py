from lib.global_resources import *
from lib.workorder import WorkOrder
import win32com.client  #type: ignore
from win32com.client import gencache
from datetime import datetime

def generate_new_twois_request_email(title: str, file: str, datestring: str) -> None:
    """Method intended to generate an email to request a new TWOIS"""
    outlook = win32com.client.Dispatch('Outlook.Application')
    mailitem = 0x0

    newmail = outlook.CreateItem(mailitem)
    newmail.Subject = f"TWOIS Request: {title}"
    # newmail.To = "fiorela.c.silvahurst@boeing.com; ryan.c.reyes2@boeing.com"                                      #MAKE_CONFIGURABLE
    # newmail.CC = "joel.deleon@boeing.com; jose.m.lopez8@boeing.com; dl-grpvafbgmdisso@exchange.boeing.com"        #MAKE_CONFIGURABLE
    newmail.To = ""
    newmail.CC = ""
    newmail.HTMLBody = get_html_email_body__new_workorder(title, datestring)
    newmail.Attachments.Add(file)
    newmail.Display()


def generate_work_order_completion_email(workorder: WorkOrder, file: str) -> None:
    """Method intended to generate an email to request a new TWOIS"""
    outlook = win32com.client.Dispatch('Outlook.Application')
    mailitem = 0x0

    newmail = outlook.CreateItem(mailitem)
    newmail.Subject = f"{workorder.title}"
    # newmail.To = "fiorela.c.silvahurst@boeing.com; ryan.c.reyes2@boeing.com"                                      #MAKE_CONFIGURABLE
    # newmail.CC = "joel.deleon@boeing.com; jose.m.lopez8@boeing.com; dl-grpvafbgmdisso@exchange.boeing.com"        #MAKE_CONFIGURABLE
    newmail.To = ""
    newmail.CC = ""
    newmail.HTMLBody = get_html_email_body__complete_workorder(workorder.number)
    newmail.Attachments.Add(file)
    newmail.Display()


def generate_calendar_event_for_approved_work(workorder: WorkOrder, file: str) -> None:
    gencache.EnsureModule('{00062FFF-0000-0000-C000-000000000046}', 0, 9, 4)

    outlook = win32com.client.gencache.EnsureDispatch("Outlook.Application")
    mapi    = outlook.GetNamespace("MAPI")
    folder  = mapi.GetDefaultFolder(win32com.client.constants.olFolderCalendar)
    
    meeting = folder.Items.Add()
    strbits: list[str] = workorder.get_date_string().split('/')
    meeting.Start = datetime(int(strbits[2]),int(strbits[0]),int(strbits[1]))
    meeting.AllDayEvent = True
    meeting.Subject = workorder.title
    meeting.ResponseRequested = False
    meeting.Attachments.Add(file)
    meeting.ReminderSet = True
    meeting.ReminderMinutesBeforeStart = 1800
    meeting.MeetingStatus = 1
    meeting.RequiredAttendees = "joel.deleon@boeing.com; jose.m.lopez8@boeing.com"
    meeting.OptionalAttendees = "bncobb1989@gmail.com"
    meeting.Display()