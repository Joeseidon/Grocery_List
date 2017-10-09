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
    '''
    Description: Uses google's python client libraries to access the files
    stored in the root directory of the associated servie. It then prints
    the contents of that directory with some important metadata.
    Parameters:
        service: Google Drive service used to access drive data
        pages: Number of results to expect
        print_text: Enables terminal print statements for dubugging
    	json: print out json formated results from get request
    Returns:
        file list: all of the files stored on the provided google drive
    '''

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
    '''
    Description: Uses google's python client libraries to access the files
    stored in the root directory of the associated servie. It then searches
    through the results to find the requested file.
    Parameters:
        service: Google Drive service used to access drive data
        pages: Number of results to expect
        file_title: title of the file to search for on google drive
		debugging: prevents/permits printing of useful text.
    Returns:
        file: the desired file or a NoneType if not found
    '''

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
    '''
    Description: Prints some of the metadata associated with the provided file.
    Parameters:
        drive_file: file from google drive
		tofile: determins if the file data should be written to a file or
			straigt to the terminal.
		filename: file used for output if tofile==True
    '''

    #Confirm that these data points have value for the given file
    description = drive_file.get('description', 'NONE')
    downloadURL = drive_file.get('downloadUrl', 'NONE')
    if tofile:
            file = open(filename,'w')
            file.write('Name: {0}\n\tMemeType: {1}\n\tID: {2}\n\tDescription: {3}\n\tDownloadURL: {4}'.format(drive_file['name'], drive_file['mimeType'], drive_file['id'], description, downloadURL))
            file.close()
    print('Name: {0}\n\tMemeType: {1}\n\tID: {2}\n\tDescription: {3}\n\tDownloadURL: {4}'.format(drive_file['name'], drive_file['mimeType'], drive_file['id'], description, downloadURL))

def download_file(fileObj,drive_service,exportFile='GroceryList.txt',debugging = False):
    '''
    Description: This function uses an HTTP request to pull the
		target files content from google drive.
    Parameters:
        fileObj: Target file
		exportFile: File to which the target files content will be
			printed
		debugging: Parameter used to control print statements
    '''

    mimeTypeConversion = {'application/vnd.google-apps.document' : "text/plain",
                            'text/plain' : 'text/plain'}
    exportMemeType = mimeTypeConversion[fileObj['mimeType']]
    if debugging:
        print("Attempting to download file:\n\tID: {0}\n\tName: {1}\n\tmimeTpye: {2}\n\tDownload Type:{3}".format(fileObj['id'],fileObj['name'],fileObj['mimeType'],exportMemeType))

    resp, content = httplib2.Http().request("https://www.googleapis.com/drive/v3/files/{0}/export?mimeType=text%2Fplain&key=AIzaSyBQHJRYRZKK1QovxtStf_QujyW8n_MJ8m4".format(fileObj['id']))

    if debugging:
        print("Status: " + str(resp.status))

    if not resp.status == '400':
        file = open(exportFile,'wb')
        file.write(content)

    return(resp, content)

def detect_changes(drive_service):
    '''
    Description: Establishes a monitor of the target google drive to
		register changes to the stored files.
    Parameters:
        drive_service: Google drive service used by google's python client to
			register changes.
    '''

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
