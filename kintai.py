import pandas as pd
from datetime import datetime
from datetime import timedelta
from datetime import timezone
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os

JST = timezone(timedelta(hours=+9), "JST")


# 認証の流れ
def auth():
    SP_CREDENTIAL_FILE = "secret.json"
    SP_SCOPE = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

    SP_SHEET_KEY = "1yrOkKh-vKTkRagXXGdHtFKG0TCfsOsrPTEssGVCVTFc"
    SP_SHEET = "timesheet"

    credentials = ServiceAccountCredentials.from_json_keyfile_name(SP_CREDENTIAL_FILE, SP_SCOPE)
    gc = gspread.authorize(credentials)

    worksheet = gc.open_by_key(SP_SHEET_KEY).worksheet(SP_SHEET)
    return worksheet


def punch_in():  # 出勤時間
    worksheet = auth()
    # df1 = pd.DataFrame(worksheet.get_all_values())
    df1 = pd.DataFrame(worksheet.get_all_records())
    # print(df1)

    timestamp = datetime.now(JST)

    date = timestamp.strftime("%Y/%m/%d")
    # print(date)
    punch_in = timestamp.strftime("%H:%M")
    # print(punch_in)

    df2 = pd.DataFrame(data=[{"日付": date, "出勤時間": punch_in, "退勤時間": "00:00"}])
    # print(df2)

    # print(pd.concat([df1, df2]))
    df = pd.concat([df1, df2], ignore_index=True)

    worksheet.update([df.columns.values.tolist()] + df.values.tolist())
    # ここまででスプレッドシートに追加部分
    print("出勤登録完了しました")


def punch_out():  # 退勤時間
    worksheet = auth()
    df1 = pd.DataFrame(worksheet.get_all_records())

    timestamp = datetime.now(JST)

    punch_out = timestamp.strftime("%H:%M")

    # print(punch_out)
    df1.iloc[-1, 2] = punch_out
    worksheet.update([df1.columns.values.tolist()] + df1.values.tolist())

    print("退勤登録完了しました")


# punch_in() #動作確認OK！
# punch_out() #動作確認OK！
