# Globally Defined String Functions

body_new_wo_single: str
body_new_wo_mult: str
body_complete_wo_single: str
body_complete_wo_mult: str
signature: str = """Thank you!<br>
                            <br>
                            <b>Brian Cobb</b><br>
                            Systems Administration<br>
                            SITR Readiness<br>
                            805-606-8599 / 8562"""

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
            {signature}
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
            {signature}
            </p>
        </body>
    </html>
"""
    return body


def convert_body_to_html(body: str) -> str:
    return ""
