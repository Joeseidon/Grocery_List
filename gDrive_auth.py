from __future__ import print_function
import httplib2
import os
import argparse
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from oauth2client import file
from googleapiclient import discovery
from googleapiclient.http import build_http


# If modifying these scopes, delete your previously saved credentials
#SCOPES = 'https://www.googleapis.com/auth/drive'
#CLIENT_SECRET_FILE = 'client_secrets.json'
#APPLICATION_NAME = 'pytest'

def create_Gdrive_service():
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v3', http=http)
    print("Finished GDrive Service")
    return service


def init(argv, name, version, doc, filename, scope=None, parents=[], discovery_filename=None):
  """A common initialization routine for samples.

  Many of the sample applications do the same initialization, which has now
  been consolidated into this function. This function uses common idioms found
  in almost all the samples, i.e. for an API with name 'apiname', the
  credentials are stored in a file named apiname.dat, and the
  client_secrets.json file is stored in the same directory as the application
  main file.

  Args:
    argv: list of string, the command-line parameters of the application.
    name: string, name of the API.
    version: string, version of the API.
    doc: string, description of the application. Usually set to __doc__.
    file: string, filename of the application. Usually set to __file__.
    parents: list of argparse.ArgumentParser, additional command-line flags.
    scope: string, The OAuth scope used.
    discovery_filename: string, name of local discovery file (JSON). Use when discovery doc not available via URL.

  Returns:
    A tuple of (service, flags), where service is the service object and flags
    is the parsed command-line flags.
  """
  if scope is None:
    scope = 'https://www.googleapis.com/auth/' + name

  # Parser command-line arguments.
  parent_parsers = [tools.argparser]
  parent_parsers.extend(parents)
  parser = argparse.ArgumentParser(
      description=doc,
      formatter_class=argparse.RawDescriptionHelpFormatter,
      parents=parent_parsers)
  flags = parser.parse_args(argv[1:])

  # Name of a file containing the OAuth 2.0 information for this
  # application, including client_id and client_secret, which are found
  # on the API Access tab on the Google APIs
  # Console <http://code.google.com/apis/console>.
  client_secrets = os.path.join(os.path.dirname(filename),
                                'client_secrets.json')

  # Set up a Flow object to be used if we need to authenticate.
  flow = client.flow_from_clientsecrets(client_secrets,
      scope=scope,
      message=tools.message_if_missing(client_secrets))

  # Prepare credentials, and authorize HTTP object with them.
  # If the credentials don't exist or are invalid run through the native client
  # flow. The Storage object will ensure that if successful the good
  # credentials will get written back to a file.
  storage = file.Storage(name + '.dat')
  credentials = storage.get()
  if credentials is None or credentials.invalid:
    credentials = tools.run_flow(flow, storage, flags)
  http = credentials.authorize(http=build_http())

  if discovery_filename is None:
    # Construct a service object via the discovery service.
    service = discovery.build(name, version, http=http)
  else:
    # Construct a service object using a local discovery document file.
    with open(discovery_filename) as discovery_file:
      service = discovery.build_from_document(
          discovery_file.read(),
          base='https://www.googleapis.com/',
          http=http)
  return (service, flags)


'''
def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'drive-python-quickstart.json')

    print("Credentials Found")

    store = Storage(credential_path)
    credentials = store.get()

    print("Crednetials Grabbed from Storage")
    if not credentials:
        print ("no credentials")
    if credentials.invalid:
        print ("invalid credentials")

    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        #if flags:
        credentials = tools.run_flow(flow, store)
        #else: # Needed only for compatibility with Python 2.6
            #credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials
'''
