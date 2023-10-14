import pandas as pd
from datetime import datetime
from datetime import timedelta
from datetime import timezone
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os


SP_CREDENTIAL_FILE = "secret.json"
SP_SCOPE = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
SP_SHEET_KEY = "1yrOkKh-vKTkRagXXGdHtFKG0TCfsOsrPTEssGVCVTFc"
credentials = ServiceAccountCredentials.from_json_keyfile_name(SP_CREDENTIAL_FILE, SP_SCOPE)
gc = gspread.authorize(credentials)


ss = gc.open_by_key(SP_SHEET_KEY)
worksheet_list = ss.worksheets()
#print(worksheet_list)


worksheet_list[0]._properties['sheetId']
print(worksheet_list[1]._properties['sheetId'])

worksheet_list[0].title
#print(worksheet_list[0].title)

name = input("name > ")

wb = gc.open('kintai')
ws = wb.worksheet(worksheet_list[1].title)
ws.update_title(name)


#members = [0,1,2,3,4]
#for sheet in ss.worksheets():
