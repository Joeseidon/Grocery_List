import PSgrocer_email
import PSgrocer_phone

def set_up():
    phone = PSgrocer_phone()
    email = PSgrocer_email()

def notify_Employee(Name,need_items_file):
    subject = "Time to review next weeks shopping list."
    phone.sendText(recipient="5863821908", msg=subject)
    email.email_textfile(file_name=need_items_file, SUBJECT=subject)
