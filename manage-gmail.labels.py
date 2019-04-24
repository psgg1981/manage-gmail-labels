from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from apiclient import errors

import argparse
import logging
import sys

__author__ = "Pedro Gonçalves"
__version__ = "0.3.0"
__license__ = "MIT"


# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/gmail.labels']

def getLabelsList(service):
    """Calls the Gmail API, returning a list of all the label definitions in the user's mailbox.
    """
    try:
        results = service.users().labels().list(userId='me').execute()
        return results

    except errors.HttpError as error:
        print('An error occurred: %s', error)
        return []
    except error:
        print('An unknown error occurred: %s', error)
        return []


def command_list(service):
    """Calls the Gmail API, listing all labels in the user's mailbox.
    """
    try:
        
        labels = getLabelsList(service).get('labels', [])

        if not labels:
            print('No labels found.')
        else:
            print('Listing labels:')
            #labels.sort(key=lambda x: x[0]['name'], reverse=False)
            labels.sort(key = lambda x: x['name'])
            for label in labels:
                print(label['name'])
            print('\nTotal: ',len(labels), ' labels found', sep='')

    except error:
        print('An unknown error occurred: %s', error)


def makeLabel(newLabelName, mlv='hide', llv='labelHide'):
    """Create Label object.

    Args:
    label_name: The name of the Label.
    mlv: Message list visibility, show/hide [hidden by default].
    llv: Label list visibility, labelShow/labelHide [hidden by default]

    Returns:
    Created Label.
    """
    label = {'messageListVisibility': mlv,
           'name': newLabelName,
           'labelListVisibility': llv}
    return label

def command_count(service, labelName):
    """Calls the Gmail API, searches of the specified label and counts how many messages are assigned to it.
    """
    try:
        # search for the label id
        labels = getLabelsList(service).get('labels', [])
        labelId = ''
        for label in labels:
            if label['name'] == labelName:
                labelId = label['id'];
                break;

        # build the label Id list
        labelIds=[]
        labelIds.append(labelId)

        # search for messages with the given label Id
        response = service.users().messages().list(userId='me', labelIds=labelIds).execute()
        messages = []
        if 'messages' in response:
          messages.extend(response['messages'])
          logging.debug(str(len(response['messages'])) + ' messages returned in recent query')

        userInput = ''
        plusSign  = ''
        while 'nextPageToken' in response:
          page_token = response['nextPageToken']
          response = service.users().messages().list(userId='me', labelIds=labelIds, pageToken=page_token).execute()
          messages.extend(response['messages'])
          logging.debug(str(len(response['messages'])) + ' messages returned in recent query (total collected so far: ' + str(len(messages)) + ')')
         
          if len(messages) > 500 :
            userInput = input('There are too many messages to retrieve (' + str(len(messages)) + '+). Do you want to continue (y/N)?')
            if userInput != 'y' :                
                plusSign = '+'
                print('Exiting...')
                break;
            else:
                continue;
        
        print(str(len(messages)) + plusSign + ' messages found with label \'' + labelName + '\'')

    except errors.HttpError as error:
        print('An error occurred: %s', error)

def command_add(service, newLabel):
    """Calls the Gmail API, adding the new label to the user's mailbox.
    """
    try:

        results = service.users().labels().create(userId='me', body=makeLabel(newLabel)).execute()
        msg = newLabel + ' created successfully'
        logging.info(msg)
        print(msg)

    except errors.HttpError as error:
        print('An error occurred: %s', error)

def command_remove(service, labelName):
    """Calls the Gmail API, remove the existing label from the user's mailbox.
    """
    try:
        # search for the label id
        labels = getLabelsList(service).get('labels', [])
        labelId = ''
        for label in labels:
            if label['name'] == labelName:
                labelId = label['id'];
                break;

        if labelId != '':
            results = service.users().labels().delete(userId='me', id=labelId).execute()
            msg = 'Label \'' + labelName + '\' removed successfully'
            logging.info(msg)
            print(msg)
            
        else:
            print('Label \'', labelName, '\' not found', sep='')    

    #except errors.HttpError as error_:
        #print('An error occurred: %s', error_)
    except () as error:
        print('An unknown error occurred: %s', error)

def command_update(service, oldLabelName, newLabelName):
    """Calls the Gmail API, updates the existing label in the user's mailbox to another name
    """
    try:

        # search for the label id
        labels = getLabelsList(service).get('labels', [])
        oldLabelId = ''
        newLabelId = ''
        for label in labels:
            if label['name'] == oldLabelName:
                oldLabelId = label['id'];
                continue;
            elif label['name'] == newLabelName:
                newLabelId = label['id'];

        if oldLabelId != '' and newLabelId == '':
            results = service.users().labels().update(userId='me', id=oldLabelId,
                                                      body=makeLabel(newLabelName)).execute()
            print('Label \'', oldLabelName, '\' renamed to \'', newLabelName, '\' successfully', sep='')
        
        elif oldLabelId == '':
            print('Original label \'', oldLabelName, '\' was not found', sep='')  

        elif newLabelId == '':
            print('New label name \'', newLabelName, '\' already in use', sep='')  

    except errors.HttpError as error:
        print('An error occurred: %s', error)
    except error:
        print('An unknown error occurred: %s', error)

def main(args):
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)

    if args.list:
        command_list(service)

    elif vars(args).get('count') != None:
        label = vars(args)['count'][0]
        command_count(service, label)

    elif vars(args).get('add') != None:
        newLabel = vars(args)['add'][0]
        command_add(service, newLabel)

    elif vars(args).get('remove') != None:
        labelToRemove = vars(args)['remove'][0]
        command_remove(service, labelToRemove)

    elif vars(args).get('rename') != None:
        oldLabelName = vars(args)['rename'][0]
        newLabelName = vars(args)['rename'][1]
        command_update(service, oldLabelName, newLabelName)

    else:
        parser.print_help()

if __name__ == '__main__':

    # Logging format definition
    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', filename=sys.argv[0] + '.log', level=logging.DEBUG)

    parser = argparse.ArgumentParser()

    # Specify output of "--version"
    parser.add_argument(
        "-v", "--version",
        action="version",
        version="%(prog)s (version {version})".format(version=__version__))

    # Required positional argument

    parser.add_argument('-l', '--list',     help='list all labels', action='store_true')
    parser.add_argument('-c', '--count',     help='counts how many message have been assigned a specific label ', nargs=1)
    parser.add_argument('-a', '--add',     help='add a label', nargs=1)
    parser.add_argument('-rm', '--remove',   help='remove an existing label', nargs=1)
    parser.add_argument('-ren', '--rename', help='rename a label', nargs=2)

    args = parser.parse_args()

    main(args)