from __future__ import print_function
import httplib2
import os
import json
import webbrowser

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

from file_info import *
from gDrive_auth import *
from gDrive_info import *
import smtplib
from PSgrocer_phone import *
from PSgrocer_email import *

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

def main():
    service = create_Gdrive_service()
    #Working code. Taken out for additional testing
    '''
    print_drive_contents(service,10)

    file_test = find_file(service)
    print_file_data(file_test)

    print("##########################Changes#############################")
    detect_changes(service)

    '''
    print("##########################Open/download#############################")
    file_test = find_file(service)
    download_file(file_test['id'], file_test['mimeType'], file_test['name'],service)


if __name__ == '__main__':
    main()

    ##This works, commented out for google drive debugging
    #email = PS_Shopper_Email()
    #email.email_textfile(file_name = 'email_test.txt', SUBJECT = 'email text doc test')

    ##This works, commented out for email debugging
    '''
    phone = PS_Shopper_Phone()
    phone.sendText("5863821908", "Wow this python stuff is cool.")
    '''
