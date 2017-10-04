from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from apiclient import errors
from apiclient import http

import io
from apiclient.http import MediaIoBaseDownload

import json

import requests
import StringIO




def print_drive_contents(service, pages = 10, print_text = True):
    results = service.files().list(pageSize=15,fields="nextPageToken, files(id, mimeType, name, description)").execute()
    print (json.dumps(results, sort_keys=True, indent=4))
    items = results.get('files', [])
    if(print_text):
        if not items:
            print('No files found.')
        else:
            print('Files:')
            for item in items:
                description = item.get('description', 'NONE')
                downloadURL = item.get('downloadUrl', 'NONE')
                print('Name: {0}\n\tMemeType: {1}\n\tID: {2}\n\tDescription: {3}\n\tDownloadURL: {4}'.format(item['name'], item['mimeType'], item['id'], description, downloadURL))
    return items

def find_file(service, file_title = "Test Grocier List", pages = 10 ):
    print("***************Find Test********************")
    items = print_drive_contents(service,pages,print_text=False)
    if not items:
        return None

    for item in items:
        if(item['name'] == file_title):
            print('Found')
            return item

    return None

def print_file_data(drive_file):
    description = drive_file.get('description', 'NONE')
    downloadURL = drive_file.get('downloadUrl', 'NONE')
    print('Name: {0}\n\tMemeType: {1}\n\tID: {2}\n\tDescription: {3}\n\tDownloadURL: {4}'.format(drive_file['name'], drive_file['mimeType'], drive_file['id'], description, downloadURL))

def download_file2(file_id, mimeType, filename, drive_service):
    u = requests.get("https://www.googleapis.com/drive/v3/files/{0}alt=media".format(file_id))
    print (u.content)
def download_file3(file_id, mimeType, filename, service):
    result = service.spreadsheets().values().get(
        spreadsheetId=file_id, range="Item Name").execute()
    print (json.dumps(result, sort_keys=True, indent=4))
def download_file(file_id, mimeType, filename, drive_service):
    mimeTypeConversion = {'application/vnd.google-apps.document' : "text/html"}
    DownloadMimeType = mimeTypeConversion[mimeType]
    print("Attempting to download file:\n\tID: {0}\n\tName: {1}\n\tmimeTpye: {2}\n\tDownload Type:{3}".format(file_id,filename,mimeType,DownloadMimeType))
    '''
    request = drive_service.files().get_media(fileId=file_id)
    stream = io.BytesIO()
    downloader = MediaIoBaseDownload(stream, request)
    done = False
    '''

    #New Attempt
    try:
        drive_service.files().export_media(fileId = file_id,
                    mimeType = DownloadMimeType).execute()
    except Exception as e:
        print(e)
    '''
    while done is False:
        status, done = downloader.next_chunk()
        print ("Download %d%%." % int(status.progress() * 100))


    # Retry if we received HttpError
    for retry in range(0, 5):
        try:
            while done is False:
                status, done = downloader.next_chunk()
                print ("Download %d%%." % int(status.progress() * 100))
            print(stream.getvalue())
        except Exception as error:
            print ('There was an API error: {}. Try # {} failed.'.format(
                error.response,
                retry,
            ))
    '''

def detect_changes(drive_service):
    response = drive_service.changes().getStartPageToken().execute()
    print ('Start token: %s' % response.get('startPageToken'))

    # Begin with our last saved start token for this user or the
    # current token from getStartPageToken()
    page_token = response.get('startPageToken');
    while page_token is not None:
        response = drive_service.changes().list(pageToken=page_token,
                                                spaces='drive', pageSize = 200, includeRemoved = True ).execute()
        for change in response.get('changes'):
            print("entered")
            print(response.get('changes'))
            # Process change
            print ('Change found for file: %s' % change.get('fileId'))
        if 'newStartPageToken' in response:
            # Last page, save this token for the next polling interval
            saved_start_page_token = response.get('newStartPageToken')
        page_token = response.get('nextPageToken')

def delete_file(service, file_id):
  """Permanently delete a file, skipping the trash.

  Args:
    service: Drive API service instance.
    file_id: ID of the file to delete.
  """
  try:
    service.files().delete(fileId=file_id).execute()
    print('Deleted')
  except errors.HttpError, error:
    print ('An error occurred: %s' % error)
