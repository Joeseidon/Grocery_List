from __future__ import print_function
import httplib2
import os
import json
import webbrowser

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

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

def import_settings():
    with open("settings.json", "r") as f:
        data = json.load(f)

        global SCOPES
        global TARGET_FILE_NAME
        global EXPORT_FILE_NAME
        global RECOMMENDATIONS_FILE_NAME
        global NEEDED_ITEMS_JSON
        global Contacts
        SCOPES = data['Scope']
        TARGET_FILE_NAME = data['GDrive_Target']
        EXPORT_FILE_NAME = data['Grocery_List_Export']
        RECOMMENDATIONS_FILE_NAME = data['Item_Recommendations']
        NEEDED_ITEMS_JSON = data['Common_Items_JSON']
        Contacts = data['Contacts']

        global debug
        global perform_notify
        global detail_modification_test
        global testing_upload
        debug = data["script_permissions"]["debug"]
        perform_notify = data["script_permissions"]["perform_notify"]
        detail_modification_test = data["script_permissions"]["mod_testing"]
        testing_upload = data["script_permissions"]["upload_testing"]

def main():
    import_settings()
    #Used to confirm connections have been established before actions are taken
    connection_status = {"gDrive": False, "email": False, "phone": False}
    #Establish GDrive service
    try:
        connection_status["gDrive"] = True
        service, flags = init(argv = '', name = 'drive', version = 'v3',
                                    doc = '__doc__', filename = '__file__',
                                    scope = SCOPES)
    except:
        connection_status["gDrive"] = False

    #Establish email and phone server connections
    contact_eng = EmployeeNotification()
    connection_status["email"] = contact_eng.establish_email_connection()
    connection_status["phone"] = contact_eng.establish_phone_connection()


    if connection_status["gDrive"]:
        #Locate the needed grocery list
        target_file = find_file(service, file_title = TARGET_FILE_NAME, debugging = debug)

    #For debugging (shows file metadata)
    if debug and connection_status["gDrive"]:
        print_file_data(target_file)

    if connection_status["gDrive"]:
        #Retrive file content. Saved to GroceryList.txt
        resp, content = download_file(target_file, service, debugging = debug,
                                        exportFile = EXPORT_FILE_NAME)

    #Perform list processing with the most up to date list
    try:
        list_explorer = ListProcessor(target_list = EXPORT_FILE_NAME,
                                        commone_items_obj = NEEDED_ITEMS_JSON)
    except:
        if perform_notify and connection_status["email"]:
            contact_eng.send_error_msg(Contacts, e.msg, connections= connection_status)
        else:
            print(e.message)

    try:
        success = list_explorer.process_list(debug = debug)
    except Exception as e:
        success = False
        if perform_notify and connection_status["email"]:
            contact_eng.send_error_msg(Contacts, e.msg, connections= connection_status)

    #used to limmit email and text during debugging and development
    if perform_notify and success:
        subject_text = """Time to review next weeks shopping list.\nCheck your email for recommendations."""
        #Notify individuals that the list should be looked at.
        contact_eng.notify_Employee(text_file = RECOMMENDATIONS_FILE_NAME,
                                        contacts = Contacts,
                                        connection_status = connection_status,
                                        subject = subject_text, debugging=debug)
    if testing_upload:
        content = upload_file(target_file,service,"Common_Items.json",debugging=True)
        print(content)

    if detail_modification_test:
        print("Connection Status: ")
        print(connection_status)
        print("\n\n")
        print("File Download (success): ")
        print(resp)
        print("\n\n")
        print("List processing (success): "+str(success))

if __name__ == '__main__':
    main()
