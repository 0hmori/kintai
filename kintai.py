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

    df1 = pd.DataFrame(worksheet.get_all_records())  # get_all_values()だと動作できず
    # print(df1)

    timestamp = datetime.now(JST)

    date = timestamp.strftime("%Y/%m/%d")
    # print(date)
    # punch_in = timestamp.strftime("%H:%M")
    # print(punch_in)

    df2 = pd.DataFrame(data=[{"日付": date, "出勤時間": "8:30", "退勤時間": "00:00"}])
    # print(df2)

    # print(pd.concat([df1, df2]))
    df = pd.concat([df1, df2], ignore_index=True)

    worksheet.update([df.columns.values.tolist()] + df.values.tolist())
    # ここまででスプレッドシートに追加部分
    print("出勤登録完了しました")


# punch_in()  # 動作確認OK！


def late():  # 遅刻
    worksheet = auth()

    df1 = pd.DataFrame(worksheet.get_all_records())  # get_all_values()だと動作できず
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
    print("おつかれさまです。出勤登録完了しました。")


# late()  # 動作確認OK！


def punch_out():  # 退勤時間
    worksheet = auth()
    df1 = pd.DataFrame(worksheet.get_all_records())

    # timestamp = datetime.now(JST)

    # punch_out = timestamp.strftime("%H:%M")

    # print(punch_out)
    df1.iloc[-1, 2] = "17:30"
    worksheet.update([df1.columns.values.tolist()] + df1.values.tolist())

    print("退勤登録完了しました")


# punch_out()  # 動作確認OK！


def leave_early():  # 早退
    worksheet = auth()
    df1 = pd.DataFrame(worksheet.get_all_records())

    timestamp = datetime.now(JST)

    punch_out = timestamp.strftime("%H:%M")

    # print(punch_out)
    df1.iloc[-1, 2] = punch_out
    worksheet.update([df1.columns.values.tolist()] + df1.values.tolist())

    print("早退登録完了しました")


# leave_early()  # 動作確認OK！


def rest():  # 休暇
    worksheet = auth()
    df1 = pd.DataFrame(worksheet.get_all_records())
    # print(df1)

    timestamp = datetime.now(JST)

    date = timestamp.strftime("%Y/%m/%d")
    # print(date)

    df2 = pd.DataFrame(data=[{"日付": date, "出勤時間": "00:00", "退勤時間": "00:00"}])
    # print(df2)

    # print(pd.concat([df1, df2]))
    df = pd.concat([df1, df2], ignore_index=True)

    worksheet.update([df.columns.values.tolist()] + df.values.tolist())
    # ここまででスプレッドシートに追加部分
    print("休暇登録完了しました")


# rest() #動作確認OK！


def delete():  # 修正として最終行を削除。出勤時間ミス、休暇ミス時に使う。退勤時間は勝手に更新されるので使わない
    worksheet = auth()

    row_count = len(worksheet.get_all_values())
    # print("最終行番号:", row_count)

    worksheet.delete_rows(row_count)

    print("修正登録完了しました。入力し直してください")


# delete() #動作確認OK！
