import pandas as pd
from datetime import datetime
from datetime import timedelta
from datetime import timezone
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os

JST = timezone(timedelta(hours=+9), "JST")


# 認証の流れ
def auth(userid):
    SP_CREDENTIAL_FILE = "secret.json"
    SP_SCOPE = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

    SP_SHEET_KEY = "1yrOkKh-vKTkRagXXGdHtFKG0TCfsOsrPTEssGVCVTFc"

    credentials = ServiceAccountCredentials.from_json_keyfile_name(SP_CREDENTIAL_FILE, SP_SCOPE)
    gc = gspread.authorize(credentials)
    ss = gc.open_by_key(SP_SHEET_KEY)

    worksheet = find_or_new_sheet(ss, userid)

    return worksheet


def find_or_new_sheet(ss, userid):
    sheettitle = get_title_by_userid(userid)

    for sheet in ss.worksheets():
        if sheet.title == sheettitle:
            return ss.worksheet(sheettitle)
    return ss.add_worksheet(sheettitle, 100, 3)


# スプレッドシートのシート名を変えるには、現状ここに追加していく
def get_title_by_userid(userid):
    "useridからシート名を返す関数"
    sheet_names = {
        "U3457ef080344dc6ce7d0bf86a240108d": "オオモリ",
    }
    sheettitle = sheet_names[userid]
    return sheettitle


def punch_in(userid):  # 出勤
    worksheet = auth(userid)

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


def late(userid):  # 遅刻
    worksheet = auth(userid)

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


def punch_out(userid):  # 退勤時間
    worksheet = auth(userid)
    df1 = pd.DataFrame(worksheet.get_all_records())

    # timestamp = datetime.now(JST)

    # punch_out = timestamp.strftime("%H:%M")

    # print(punch_out)
    df1.iloc[-1, 2] = "17:30"
    worksheet.update([df1.columns.values.tolist()] + df1.values.tolist())

    print("退勤登録完了しました")


# punch_out()  # 動作確認OK！


def leave_early(userid):  # 早退
    worksheet = auth(userid)
    df1 = pd.DataFrame(worksheet.get_all_records())

    timestamp = datetime.now(JST)

    punch_out = timestamp.strftime("%H:%M")

    # print(punch_out)
    df1.iloc[-1, 2] = punch_out
    worksheet.update([df1.columns.values.tolist()] + df1.values.tolist())

    print("早退登録完了しました")


# leave_early()  # 動作確認OK！


def rest(userid):  # 休暇
    worksheet = auth(userid)
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


def delete(userid):  # 修正として最終行を削除。出勤時間ミス、休暇ミス時に使う。退勤時間は勝手に更新されるので使わない
    worksheet = auth(userid)

    row_count = len(worksheet.get_all_values())
    # print("最終行番号:", row_count)

    worksheet.delete_rows(row_count)

    print("修正登録完了しました。入力し直してください")


# delete() #動作確認OK！
