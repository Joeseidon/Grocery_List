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

SCOPES = 'https://www.googleapis.com/auth/drive'

def main():
    #service = create_Gdrive_service()
    #Working code. Taken out for additional testing
    service, flags = init(argv = '', name = 'drive', version = 'v3', doc = '__doc__', filename = '__file__', scope = SCOPES)
    print_drive_contents(service,10)

    file_test = find_file(service,debugging=True)
    print_file_data(file_test)

    '''
    print("##########################Changes#############################")
    detect_changes(service)
    '''

    print("##########################Open/download#############################")
    file_test = find_file(service)
    resp, content = download_file2(file_test['id'], file_test['mimeType'], file_test['name'],service,filet=file_test)


    if not resp.status == '400':
        file = open('testingdownload.txt','wb')
        file.write(content)

    '''
    print("##########################Http Attempt#############################")
    content = download_http(file_test['id'], file_test['mimeType'], file_test['name'],service,filet=file_test)

    #Only works for files with binary content

    print("##########################NEwTest#############################")
    Nprint_file_content(service,file_test['id'])
    file = open('downTest.txt','w')
    Ndownload(service,file_test['id'],file)
    file.close()
    '''

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
