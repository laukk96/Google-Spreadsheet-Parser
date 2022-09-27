# Test for the automated Google Calender Scheduler for Google ExcelSheet Links

from __future__ import print_function

from datetime import datetime, timedelta

# https://stackoverflow.com/questions/45501082/set-google-application-credentials-in-python-project-to-use-google-api
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "resources\\keys.json"


from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# These lines generate all the necessary credentials for accessing a spreadsheet
from google.oauth2 import service_account

# For unpacking credentials information from Google Auth 2.0
# @ 11:30, https://www.youtube.com/watch?v=j1mh0or2CX8
import pickle 

# from apiclient.discovery import build

# Helper Python Files
from helper_functions import write_json, cls
from helper_classes import Workday

values = None

def SPREADSHEET_get_values(link):
    global values
    # SCOPES = ['https://www.googleapis.com/auth/sqlservice.admin']
    SERVICE_ACCOUNT_FILE = 'resources\\keys.json'
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

    credentials = None
    credentials = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)

    # The ID and range of a sample spreadsheet.
    # SAMPLE_SPREADSHEET_ID = '1N9DbFu2NmmpLcNBQGcUNaRfY1QobsGdb35s-vsZJzwg'
    # link = https://docs.google.com/spreadsheets/d/1AfCd8G-ogkbQPUe5SPBvbNUHUILDIned-JK7ssRSjMk/edit#gid=0
    link = link[link.find('/d/')+3:]
    SAMPLE_SPREADSHEET_ID = link[:link.find('/')]
    print(f'{link} \n: {SAMPLE_SPREADSHEET_ID}')
    SAMPLE_RANGE_NAME = 'B3:J55'

    # creds = None
    creds = credentials

    service = build('sheets', 'v4', credentials=creds)  

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=SAMPLE_RANGE_NAME).execute()

    values = result.get('values', [])
    # return values

# write_json(result, 'resources\\schedule.json')

workdays = {}

def get_date_info(row_index):
    the_date = values[0][row_index]
    the_day = values[1][row_index]
    date_key = f'{the_date} {the_day}'
    return date_key, the_date, the_day

def convert_values_to_workdays(target_name):
    for i in range(2, len(values)):
        for row_index in range(0, len(values[i])):
            # Change to uppercase
            values[i][row_index] = values[i][row_index].upper()
            if target_name in values[i][row_index]:
                print(values[i])
                
                date_key, the_date, the_day = get_date_info(row_index)  
                
                if not date_key in workdays.keys():
                    workdays[date_key] = []
                
                new_day = Workday(
                    date = the_date,
                    day = the_day,
                    time = values[i][0],
                    position = values[i][1]
                )
                workdays[date_key].append(new_day)

def print_workdays():
    print(f'\nTop Row: Dates = {values[0]}')
    print(f'Row 2: Days = {values[1]} \n')
    
    print('\n====================')
    
    # Loop through the first row of dates (values[0])
    for row_index in range(2, len(values[0])):
        # Get date info (Returns an array of 3 string variables)
        # Change the array to be a single string variable containing the date_key
        date_key = get_date_info(row_index)
        date_key = date_key[0]
        
        if date_key in workdays.keys():
            for entry in workdays[date_key]:
                if isinstance(entry, Workday):
                    entry.print()
            print('====================')


# ============================================================

def CALENDAR_setup():
    calendar_scopes = ['https://www.googleapis.com/auth/calendar']
    flow = InstalledAppFlow.from_client_secrets_file('resources\\client_secret.json', scopes=calendar_scopes)
    credentials = flow.run_console()
    
    pickle.dump(credentials, open("token.pkl", "wb"))
    credentials = pickle.load(open("token.pkl", "rb"))
    service = build("calendar", "v3", credentials=credentials)
    account_info = service.calendarList().list(maxResults=15).execute()
    print(account_info)
    
    # write_json(account_info['items'][2], 'account_info.json')
    
    calendarId = account_info['items'][2]['id']
    result = service.events().list(calendarId=calendarId).execute()
    print(result)
    # Store the returned events of the calendar inside a json
    # write_json(result, 'event_result.json')
    
    
    
    


# ====================================
# Main Area

cls()
# CALENDAR_setup()

# cls()
print("Enter the link for the spreadsheet schedule: ")
schedule_link = input()
print("Enter the name of the person you're looking for: ")
target_name = input().upper()

SPREADSHEET_get_values(schedule_link)
convert_values_to_workdays(target_name)
print_workdays() 