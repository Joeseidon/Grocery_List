from __future__ import print_function
import httplib2
import os
import json
import webbrowser

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

#from file_info import *
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

SCOPES = 'https://www.googleapis.com/auth/drive'
TARGET_FILE_NAME = "Test Grocier List"
EXPORT_FILE_NAME = "GroceryList.txt"

debug = True

def main():
    #service = create_Gdrive_service()
    #Working code. Taken out for additional testing
    service, flags = init(argv = '', name = 'drive', version = 'v3', doc = '__doc__', filename = '__file__', scope = SCOPES)

    '''
    if debug:
        print_drive_contents(service,10)
    '''

    target_file = find_file(service, file_title = TARGET_FILE_NAME, debugging = debug)
    print_file_data(target_file)

    resp, content = download_file(target_file, service, debugging = debug, exportFile = EXPORT_FILE_NAME)



if __name__ == '__main__':
    main()

    ##This works, commented out for google drive debugging
    '''
    email = PS_Shopper_Email()
    email.sendMail(TEXT="Sending python test.",
                    TO=['cutinoj@mail.gvsu.edu'],
                    SUBJECT = 'Python Test')
    '''
    ##This works, commented out for email debugging
    '''
    phone = PS_Shopper_Phone()
    phone.sendText("+15863821908", "Test from script")
    '''
