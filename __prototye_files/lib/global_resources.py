import os

# Global Constants
USERHOME: str = "\\Users\\" + os.getlogin() + "\\Desktop"
IN_PROGRESS_DIR: str = os.getcwd() + "\\in_progress"
COMPLETE_DIR: str = os.getcwd() + "\\complete"
TEMPLATE_TWOIS: str = "res/TWOIS_template-3-20.xlsx"
FONTSIZE: int = 9
NUMROWS: int = 1


# Configuration Information
__email_signature: str = "Thank you!<br><br><b>Brian Cobb</b><br>Systems Administration<br>SITR Readiness<br>805-606-8599 / 8562"


# Globally Defined String Functions
def get_html_email_body__new_workorder(title:str, datestring:str) -> str:
    """This method generates the HTML-formatted text body for a new TWOIS email. It is located in the global constants file."""

    
    body = rf"""
    <html>
        <body>
            <p>Hey Fiorela!<br>
            <br>
            Please see the attached TWOIS request for the following task scheduled to be performed on {datestring}: {title}<br>
            Let me know if everything looks alright.<br>
            <br>
            {__email_signature}
            </p>
        </body>
    </html>
"""
    return body

def get_html_email_body__complete_workorder(wonumber: str):

    body = rf"""
    <html>
        <body>
            <p>Hey Fiorela!<br>
            <br>
            Please see the attached TWOIS # {wonumber}. The work is complete and the work order can be closed.<br>
            Let me know if everything looks alright.<br>
            <br>
            {__email_signature}
            </p>
        </body>
    </html>
"""
    return body


def get_next_pending_workorder_number() -> str:
    """Method which determines what the Pending work order number should be based on how many other pending work orders are in the in_progress directory."""
    nums: set[int] = set()
    for name in os.listdir(IN_PROGRESS_DIR):
        if name.endswith(".twois") and name.startswith("Pending"):
            num: int = int(name.split(".")[0].split("-")[1])
            nums.add(num)
    resp: str = f"Pending-001"
    for i in range(len(nums)):
        ind: int = i + 1
        if ind not in nums:
            n: str = str(ind).rjust(max(3, len(str(ind))), '0') #leading zeroes
            return f"Pending-{n}"
        nexti = ind + 1
        resp = f"Pending-{str(nexti).rjust(max(3, len(str(nexti))), '0')}"
    return resp


g_sites_dict: dict[str, int] = {'VSFB : B1768 : Rm 21': 0,
                                'VSFB : B1768 : Rm 6/7/8' : 1,
                                'VSFB : B1768 : Rm 2' : 2}          #Maybe these could be loaded from a config file at some point


G_WO_TYPE_DICT: dict[str, int] = {'Preventative Maintenance': 0,
                                'Corrective Maintenance' : 1,
                                'Other' : 2}                        #These are constants


G_WO_TYPE_DICT_ABBR: dict[str, int] = {'PM': 0,
                                'CM' : 1,
                                'OTH' : 2}                          #These are constants

g_admin_dict: dict[int, str] = {3677837: "Brian Cobb",
                                3667293 : "Joel DeLeon",
                                3421099 : "Jose Lopez"}             #Should be loaded from a config file!