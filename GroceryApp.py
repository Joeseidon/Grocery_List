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
from Tkinter import *

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
def connect():
    global connection_status
    connection_status = {"gDrive": False, "email": False, "phone": False}
    try:
        connection_status["gDrive"] = True
        global service
        service, flags = init(argv = '', name = 'drive', version = 'v3',
                                    doc = '__doc__', filename = '__file__',
                                    scope = SCOPES)
    except:
        connection_status["gDrive"] = False

    #Establish email and phone server connections
    contact_eng = EmployeeNotification()
    connection_status["email"] = contact_eng.establish_email_connection()
    connection_status["phone"] = contact_eng.establish_phone_connection()

def download():
    if connection_status["gDrive"]:
        #Locate the needed grocery list
        target_file = find_file(service, file_title = TARGET_FILE_NAME, debugging = debug)
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

def main():
    import_settings()

    root = Tk()

    mainframe = Frame(root)
    mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
    mainframe.columnconfigure(0, weight=1)
    mainframe.rowconfigure(0, weight=1)
    mainframe.pack()

    root.title("Grocery List Manager")

    connectBtn = Button(root, text = "Connect", command = connect)
    connectBtn.pack()

    downloadBtn = Button(root, text = "Download", command = download)
    downloadBtn.pack()

    text = Text(root)
    with open(RECOMMENDATIONS_FILE_NAME, 'r') as f:
        for line in f.readlines():
            text.insert(INSERT,line)
        text.pack()
    root.mainloop()

if __name__ == '__main__':
    main()
