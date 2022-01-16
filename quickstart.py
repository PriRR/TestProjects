from __future__ import print_function
import os.path
import time
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload
import io
import shutil


class DriveAPI:
    global SCOPES
    SCOPES = ['https://www.googleapis.com/auth/drive']

    def connectDriveAPI(self):
        self.creds = None

        if os.path.exists('token.json'):
            self.creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        # If credentials are not valid, Log in. 
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                self.creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(self.creds.to_json())

        try:
            self.service = build('drive', 'v3', credentials=self.creds)
            # Call the Drive v3 API
            results = self.service.files().list(
                pageSize=30, fields="nextPageToken, files(id, name)").execute()
            items = results.get('files', [])

            if not items:
                print('No files found.')
                return
            print('Listing Files Present on the Google Drive: \n')
            time.sleep(2)
            for item in items:
                print(u'{0} ({1})'.format(item['name'], item['id']))
        except HttpError as error:
            print(f'An error occurred: {error}')


    def DownloadFile(self, file_id, file_name):
        request = self.service.files().get_media(fileId=file_id)
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        # Download the data in chunks
        while not done:
            status, done = downloader.next_chunk()
  
        fh.seek(0)          
        # Write the received data to the file
        with open(file_name, 'wb') as f:
            shutil.copyfileobj(fh, f)
  
        print("File Downloaded")
        return True


if __name__ == '__main__':
    print("This Program will download files from Google Drive.. \n")
    objDriveAPI = DriveAPI() 
    objDriveAPI.connectDriveAPI()
    ## Read File ID and Name from User to Download a file.
    file_id = input("\nEnter File ID : ")
    file_name = input("Enter File Name : ")
    print("Downloading File in current directory..")
    objDriveAPI.DownloadFile(file_id, file_name)

