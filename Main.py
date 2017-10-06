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
from gDrive_notification import *
from List_Processor import *

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

SCOPES = 'https://www.googleapis.com/auth/drive'
TARGET_FILE_NAME = "Test Grocier List"
EXPORT_FILE_NAME = "GroceryList.txt"
RECOMMENDATIONS_FILE_NAME = "neededItems.txt"
NEEDED_ITEMS_JSON = "Common_Items.json"

Contacts = {
    "Email_Contacts" : ['cutinoj@mail.gvsu.edu','joseph.cutino@psware.com'],
    "Phone_Contacts" : ['5863821908']
    }

debug = False
perform_notify = False

def main():
    #service = create_Gdrive_service()
    #Working code. Taken out for additional testing

    #Establish GDrive service
    service, flags = init(argv = '', name = 'drive', version = 'v3', doc = '__doc__', filename = '__file__', scope = SCOPES)

    #Locate the needed grocery list
    target_file = find_file(service, file_title = TARGET_FILE_NAME, debugging = debug)

    #For debugging (shows file metadata)
    if debug:
        print_file_data(target_file)

    #Retrive file content. Saved to GroceryList.txt
    resp, content = download_file(target_file, service, debugging = debug, exportFile = EXPORT_FILE_NAME)

    #Perform list processing with the most up to date list
    list_explorer = ListProcessor(target_list = EXPORT_FILE_NAME, commone_items_obj = NEEDED_ITEMS_JSON)
    list_explorer.process_list(debug = debug)

    #used to limmit email and text during debugging and development
    if perform_notify:
        #Notify individuals that the list should be looked at.
        contact_eng = EmployeeNotification()
        contact_eng.notify_Employee(text_file = RECOMMENDATIONS_FILE_NAME, contacts = Contacts, debugging=debug)

if __name__ == '__main__':
    main()
