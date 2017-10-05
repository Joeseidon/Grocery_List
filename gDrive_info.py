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


def print_drive_contents(service, pages = 10, print_text = True, json = False):
    results = service.files().list(pageSize=15,fields="nextPageToken, files(id, mimeType, name, description)").execute()
    if json:
        print (json.dumps(results, sort_keys=True, indent=4))
    items = results.get('files', [])
    if(print_text):
        if not items:
            print('No files found.')
        else:
            print('Files:')
            for item in items:
                print_file_data(item,tofile=True)
    return items

def find_file(service, file_title = "document.txt", pages = 10, debugging = False ):
    if debugging:
        print("***************Find Test********************")
    items = print_drive_contents(service,pages,print_text=False)
    if not items:
        return None

    for item in items:
        if(item['name'] == file_title):
            if debugging:
                print('Found')
                print_file_data(item,tofile=True)
            return item
    return None

def print_file_data(drive_file,tofile=False,filename = 'fileids.txt'):
    description = drive_file.get('description', 'NONE')
    downloadURL = drive_file.get('downloadUrl', 'NONE')
    if tofile:
            file = open(filename,'w')
            file.write('Name: {0}\n\tMemeType: {1}\n\tID: {2}\n\tDescription: {3}\n\tDownloadURL: {4}'.format(drive_file['name'], drive_file['mimeType'], drive_file['id'], description, downloadURL))
            file.close()
    print('Name: {0}\n\tMemeType: {1}\n\tID: {2}\n\tDescription: {3}\n\tDownloadURL: {4}'.format(drive_file['name'], drive_file['mimeType'], drive_file['id'], description, downloadURL))

def download_http(file_id, mimeType, filename, drive_service,filet):
    mimeTypeConversion = {'application/vnd.google-apps.document' : "text/plain",
                            'text/plain' : 'text/plain'}
    exportMemeType = mimeTypeConversion[mimeType]
        #GET https://www.googleapis.com/drive/v2/files/fileId/export
    print("Attempting to download file:\n\tID: {0}\n\tName: {1}\n\tmimeTpye: {2}\n\tDownload Type:{3}".format(file_id,filename,mimeType,exportMemeType))

    #resp, content = drive_service._http.requests("https://www.googleapis.com/drive/v2/files/{0}/{1}".format(file_id,exportMemeType))
    #print (resp)
    r = requests.get('https://api.github.com/user', auth=('user', 'pass'))
    r.raise_for_status()
    print(r)

def download_file2(file_id, mimeType, filename, drive_service,filet):
    mimeTypeConversion = {'application/vnd.google-apps.document' : "text/plain",
                            'text/plain' : 'text/plain'}
    exportMemeType = mimeTypeConversion[mimeType]
        #GET https://www.googleapis.com/drive/v2/files/fileId/export
    print("Attempting to download file:\n\tID: {0}\n\tName: {1}\n\tmimeTpye: {2}\n\tDownload Type:{3}".format(file_id,filename,mimeType,exportMemeType))

    #https://www.googleapis.com/drive/v3/files/1BDiJ0Dzjdd-Tvdo69KMjAjbEpL4j6fLPSsuhRrzgrZ0/export?mimeType=text%2Fplain&key={YOUR_API_KEY}
    #u = requests.get("https://www.googleapis.com/drive/v2/files/{0}/export?mimeType={1}".format(file_id,exportMemeType))
    resp, content = httplib2.Http().request("https://www.googleapis.com/drive/v3/files/1BDiJ0Dzjdd-Tvdo69KMjAjbEpL4j6fLPSsuhRrzgrZ0/export?mimeType=text%2Fplain&key=AIzaSyBQHJRYRZKK1QovxtStf_QujyW8n_MJ8m4")
    print("Status: "+str(resp.status))
    return(resp, content)
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
        print("Attempt successful!?")
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


def print_file_metadata(service, file_id):
  """Print a file's metadata.

  Args:
    service: Drive API service instance.
    file_id: ID of the file to print metadata for.
  """
  try:
    file = service.files().get(fileId=file_id).execute()

    print( 'Title: %s' % file['title'])
    print ('MIME type: %s' % file['mimeType'])
  except errors.HttpError, error:
    print ('An error occurred: %s' % error)

##Only useable for files with binary content
'''
def Nprint_file_content(service, file_id):
  """Print a file's content.

  Args:
    service: Drive API service instance.
    file_id: ID of the file.

  Returns:
    File's content if successful, None otherwise.
  """
  try:
    print( service.files().get_media(fileId=file_id).execute())
  except errors.HttpError, error:
    print ('An error occurred: %s' % error)
def Ndownload(service, file_id, local_fd):
  """Download a Drive file's content to the local filesystem.

  Args:
    service: Drive API Service instance.
    file_id: ID of the Drive file that will downloaded.
    local_fd: io.Base or file object, the stream that the Drive file's
        contents will be written to.
  """
  request = service.files().get_media(fileId=file_id)
  media_request = http.MediaIoBaseDownload(local_fd, request)

  while True:
    try:
      download_progress, done = media_request.next_chunk()
    except errors.HttpError, error:
      print ('An error occurred: %s' % error)
      return
    if download_progress:
      print ('Download Progress: %d%%' % int(download_progress.progress() * 100))
    if done:
      print ('Download Complete')
      return
'''
