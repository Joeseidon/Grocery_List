from PSgrocer_phone import *
from PSgrocer_email import *

class EmployeeNotification:
    '''
	Description: Used by other scripts to notify contacts
		via email and/or phone.
	Dependancies: requires the use of PSgrocer email
		and phone scripts
	'''

    def __init__(self):
        pass
    def establish_phone_connection(self):
        '''
		Description: Performs the necessary setup for
			text messages.
		'''
        try:
            self.phone = PS_Shopper_Phone()
            return True
        except:
            return False
    def establish_email_connection(self):
        '''
		Description: Performs the necessary setup for
			emails.
		'''
        try:
            self.email = PS_Shopper_Email()
            return True
        except:
            return False
    def text_Employee(self, contacts,connection_status, text_msg, debugging = False):
        if connection_status["phone"]:
            self.phone.sendText(recipient_list = contacts["Phone_Contacts"],
                                    msg=text_msg, debug = debugging)


    def notify_Employee(self, text_file, contacts,
                            connection_status, subject, debugging = False):
        '''
		Description: Makes use of the imported email module to
			notify the provided contacts with the established
			message.
		Parameters:
			text_file = target data file to be sent via email
			contacts = list of contact numbers and email adresses
			connection_status: tells the function if the email and
				phone server connections have been created succesfully
		'''
        if connection_status["phone"]:
            self.phone.sendText(recipient_list = contacts["Phone_Contacts"],
                                    msg=subject, debug = debugging)
        if connection_status["email"]:
            self.email.email_textfile(file_name=text_file,
                                        email_list=contacts["Email_Contacts"],
                                        SUBJECT=subject, debugging=debugging)

    def send_error_msg(self, contacts, msg, connections):
        '''
		Description: Used to send error messages when the script fails
			via email.
		Parameters:
			contacts: Who will be contacted
			msg: error message
			connections: status of server connections
		'''
        if connections["email"]:
            self.email.sendMail(msg, TO=contacts, SUBJECT = "Script Error")
