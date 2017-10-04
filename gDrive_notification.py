import PSgrocer_email
import PSgrocer_phone

def set_up():
    phone = PSgrocer_phone()
    email = PSgrocer_email()

def notify_Employee(Name,Text):
    phone.sendText()
    email.sendEmail()
