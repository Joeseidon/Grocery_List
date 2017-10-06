from PSgrocer_phone import *
from PSgrocer_email import *

class EmployeeNotification:
    def __init__(self):
        self.phone = PS_Shopper_Phone()
        self.email = PS_Shopper_Email()

    def notify_Employee(self, text_file, contacts,debugging = False):
        subject = "Time to review next weeks shopping list. Check your eamil for recommendations."
        self.phone.sendText(recipient_list = contacts["Phone_Contacts"], msg=subject, debug = debugging)
        self.email.email_textfile(file_name=text_file, email_list=contacts["Email_Contacts"], SUBJECT=subject, debugging=debugging)
