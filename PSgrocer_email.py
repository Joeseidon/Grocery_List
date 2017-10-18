import smtplib
import sys
import traceback
import os

class PS_Shopper_Email:
    server = None
    PyEmail = 'jcPyTest@gmail.com'
    PyPass = 'PyTest77'
    PORT = 587
    set_up_complete = False
    def __init__(self):
        try:
            self.set_up()
        except:
            print("Email Setup Error")
            traceback.print_exc()

    def get_setup_complete(self):
        return self.set_up_complete

    def set_up(self):
        if not self.get_setup_complete():
            self.set_up_complete = True
            try:
                self.server = smtplib.SMTP('smtp.gmail.com', self.PORT)
            except:
                PORT = 465
                self.server = smtplib.SMTP_SSL('smtp.gmail.com', self.PORT)

            #create connection with SMTP server
            result = self.server.ehlo()
            if(not result[0] == 250):
                print("SMTP Connection Error")
                self.set_up_complete = False

            if(self.PORT == 587):
                result = self.server.starttls()
                if(not result[0] == 220):
                    print("Failed to start TLS Encyrption")
                    self.set_up_complete = False

            result = self.server.login(self.PyEmail,self.PyPass)
            if(not result[0] == 235):
                print("Email Login Failed")
                self.set_up_complet = False

    def email_textfile(self,file_name,
                FROM= PyEmail,
                email_list= ['cutinoj@mail.gvsu.edu'],
                SUBJECT="Weekly Shopping List", SERVER = None, debugging = False):

        f = open(file_name)
        text = f.readlines()
        msg = "\n".join(text)

        if SERVER == None:
            SERVER = self.server

        message = """From: %s\nTo: %s\nSubject: %s\n\n%s
        """ % (FROM, ", ".join(email_list), SUBJECT, msg)

        if self.get_setup_complete():
            if debugging:
                print("sendMail: setup completed")
            try:
                SERVER.sendmail(FROM, email_list, message)
                if debugging:
                    print("Email Sent...(Maybe: There were atleast no exceptions thrown.)")
                    print("Message Data: " + message)
            except:
                traceback.print_exc()

        else:
            if debugging:
                print("sendMail: setup no complete")
            try:
                self.set_up()
            except:
                print("Email Setup Error")

    def sendMail(self,TEXT,
                FROM= PyEmail,
                TO= ['cutinoj@mail.gvsu.edu'],
                SUBJECT="Weekly Shopping List", SERVER = None, debugging = False):

        if SERVER == None:
            SERVER = self.server

        message = """From: %s\nTo: %s\nSubject: %s\n\n%s
        """ % (FROM, ", ".join(TO), SUBJECT, TEXT)

        if self.get_setup_complete():
            print("sendMail: setup completed")
            try:
                SERVER.sendmail(FROM, TO, message)
                if debugging:
                    print("Email Sent...(Maybe: There were atleast no exceptions thrown.)")
                    print("Message Data: " + message)
            except:
                traceback.print_exc()

        else:
            if debugging:
                print("sendMail: setup no complete")
            try:
                self.set_up()
            except:
                print("Email Setup Error")
