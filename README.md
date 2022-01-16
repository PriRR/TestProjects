# TestProject : Download Files from Google Drive using Drive API

Instructions to run the script:

This script uses Drive API to download files from Google drive. Below are the prerequisites to run this script:

    1. Python3 with Google client library installed:
        pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib

    2. Enable Drive API for your Google Drive. 
       Detailed instructions are given here: https://developers.google.com/workspace/guides/create-project.

Run the script in your command prompt as:
    python downloadFilesFromGoogleDrive.py

This program uses a simple mechanism to ask user to enter File_ID (and File name with which downloaded file will be stored) and download it in current directory.
    
# Test Cases:

This script provides support for below test scenarios:
1. Download a File by providing File ID as input to the program.
2. Download a File by providing File ID and directory to save the doenloaded file as input to program. 
     - Provide a directory that exists 
     - Provide a directory that doesn't exist.
3. Download a file when file with same name already exists in current or user specified directory.
4. Download all files present in Google drive.

Below are the scenarios where program is most likely to break. Scenarios that a program should provide support for:

1. Enter Invalid/Non existent file ID.
    - Observed behaviour: This program will throw an "http error 404: File not found" and terminate if invalid File ID is provided.
    - Expected Results: Program should display correct messgage if invalid File Id is provided and should not terminate abruptly.


2. Enter a folder name instead of file name.
    - Observed behaviour: Drive API lists everything in your Google drive: files, folders, trashed files/folders. Program will break if user enters folder ID. Program is terminatating with "http error 404: File not found" same as test case 1.
    - Expected Results : Program should display correct messgage if invalid File Id is provided and should not terminate abruptly.


3. Specify File name same as existing file in current directory
    - Observed behaviour: Here program is overriding the existing file but this will lead to data loss.
    - Expected Results: Script should notify user that file with same name already exists in the directory and provide an option to user whether or not to override a file.


4. Spcify different folder to save the downloaded file.
   - Observed behaviour: This script saves the file in current directory. User cannot provide different directory to store the file in.
   - Expected : Script should have support to provide another directory to download the file in and handle use cases like what if user specified directory doesn't exist or directory doesn't have enough space or ran out of space while copying the file from drive.


5. Specify multiple File IDs when program prompts for the File IDs and try to download multiple Files.
   - Observed behaviour: This scipt considers provided multiple File Ids as one single File ID and terminates the program with invalid File ID error.
   - Expected : Script should have support to download multiple Files at a time. For ex. Specify space separated list of File IDs and script will download all those files.
 
6. Provide support for downloading all Google drive files at once.


## Improvements that can be done in Program:

1. Provide support for advance search queries like when use wants to download all txt files or all pdf files stored on drive.

2. Show Download progress. This will help while downloading larger files.

