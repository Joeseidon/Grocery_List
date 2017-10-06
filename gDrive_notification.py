from PSgrocer_phone import *
from PSgrocer_email import *

class EmployeeNotification:
    def __init__(self):
        pass
    def establish_phone_connection(self):
        try:
            self.phone = PS_Shopper_Phone()
            return True
        except:
            return False
    def establish_email_connection(self):
        try:
            self.email = PS_Shopper_Email()
            return True
        except:
            return False
    def notify_Employee(self, text_file, contacts,
                            connection_status, debugging = False):
        subject = """Time to review next weeks shopping list.
                        Check your eamil for recommendations."""
        if connection_status["phone"]:
            self.phone.sendText(recipient_list = contacts["Phone_Contacts"],
                                    msg=subject, debug = debugging)
        if connection_status["email"]:
            self.email.email_textfile(file_name=text_file,
                                        email_list=contacts["Email_Contacts"],
                                        SUBJECT=subject, debugging=debugging)

    def send_error_msg(self, contacts, msg, connections):
        if connection_status["email"]:
            self.email.sendMail(msg, TO=contacts, SUBJECT = "Script Error")
