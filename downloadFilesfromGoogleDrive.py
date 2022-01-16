import os
import time
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload
import io


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
            print('\nListing Files Present on the Google Drive: \n')
            time.sleep(2)
            for item in items:
                print(u'File ID: {1}  File Name: {0}'.format(item['name'], item['id']))
        except HttpError as error:
            print(f'An error occurred: {error}')


    def DownloadFile(self, file_id, file_loc):
        request = self.service.files().get_media(fileId=file_id)
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        # Download the data in chunks
        try:
            while not done:
                status, done = downloader.next_chunk()
                #print("Download %d%%." % int(status.progress() * 100))
        except:
            print("\nSomething went wrong. File ID is not valid. ")

        if os.path.exists(file_loc):
            print("%s already present"%file_loc)
            print("Do you want to override the existing file? This program will terminate if you entered no.")
            response = input("Enter your choice (yes/no): ")
            if response == "yes":
                with io.open(file_loc,'wb') as f:
                    fh.seek(0)
                    f.write(fh.read())
                    print("File Downloaded.")
            elif response == "no":
                print("Exiting..")
                return
        else:
            with io.open(file_loc,'wb') as f:
                fh.seek(0)
                f.write(fh.read())
                print("File Downloaded.")

    def DownloadAllFiles(self):
        results = self.service.files().list(pageSize=30, fields="nextPageToken, files(id, name)").execute()
        items = results.get('files', [])
        print("\nDownloading all Files in Google Drive..\n")
        for item in items:
            print(u'Downloading File : {0}'.format(item['name']))
            self.DownloadFile(item['id'], str(os.getcwd() + "\\" + str(item['name'])))


if __name__ == '__main__':
    print("This Program will download files from Google Drive.. \n")

    print("\n1. Download a File using File ID \n2. Download all Files in Google Drive \n3. Run a search query")
    choice = input("\nEnter your choice : ")

    objDriveAPI = DriveAPI() 
    objDriveAPI.connectDriveAPI()

    if choice == "1":
        ## Read File ID, Name and location to save Downloaded file from user.
        file_id = input("\nEnter ID of the File to be downloaded : ")
        file_name = input("Enter File name to save the file : ")
        response = input("Downloading File in current folder.. Do you want to save the file in other folder (yes/no) : ")
        if response == "yes":
            file_path = input("\nEnter Local folder path to save the file : ")
            if os.path.exists(file_path):
                if not file_path.endswith('\\'):
                    file_loc = str(file_path + "\\"+ file_name)
            else:
                print("Local Folder %s doesn't exist. Saving File in current folder..\n"%file_path)
                file_loc = str(os.getcwd() + "\\" + file_name)
        elif response == "no":
            file_loc = str(os.getcwd() + "\\" + file_name)
            print("\nSaving File in current folder %s..\n"%file_loc)
        else:
            print("Invalid Response.")
        objDriveAPI.DownloadFile(file_id, file_loc)
    elif choice == "2":
        objDriveAPI.DownloadAllFiles()
    elif choice == "3":
        print("This is not implemented yet. Exiting..")

    







