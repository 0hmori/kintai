import datetime
from datetime import timedelta
from datetime import timezone

import schedule


import os
from flask import Flask
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import TextSendMessage
from dotenv import load_dotenv
import time
import locale
import threading

JST = timezone(timedelta(hours=+9), "JST")

load_dotenv()


line_bot_api = LineBotApi(os.environ["ACCESS_TOKEN"])
handler = WebhookHandler(os.environ["CHANNEL_SECRET"])


# locale.setlocale(locale.LC_TIME, "ja_JP.UTF-8")
Today = datetime.datetime.now()
week_num = Today.weekday()
w_list = ["月曜日", "火曜日", "水曜日", "木曜日", "金曜日", "土曜日", "日曜日"]

# print(Today,  week_num,  w_list[week_num]) 実行OK


app = Flask(__name__)


def push_sample():
    """プッシュメッセージを送る"""
    user_id = os.environ["USER_ID"]
    line_bot_api.push_message(user_id, TextSendMessage(text="Hello,world"))
    return "OK"


# rimind_punch_in関数のなかに、LINEに送るコードを入れた。メッセージ送られず


def rimind_punch_in():
    message = ""
    if week_num == 0:
        message = "おはようございます！今日は月曜日です。出勤登録をお願いします"
        # user_id = event.source.user_id
        user_id = os.environ["USER_ID"]
        line_bot_api.push_message(user_id, TextSendMessage(text=message))

    elif week_num == 1:
        message = "おはようございます！今日は火曜日です。出勤登録をお願いします"
        # user_id = event.source.user_id
        user_id = os.environ["USER_ID"]  # 元はこれ
        line_bot_api.push_message(user_id, TextSendMessage(text=message))

    elif week_num == 2:
        message = "おはようございます！今日は水曜日です。出勤登録をお願いします"  # 動作確認用。動作OK！print(rimind_punch_in())ではこのメッセージのみ出せた
        # user_id = event.source.user_id
        user_id = os.environ["USER_ID"]
        line_bot_api.push_message(user_id, TextSendMessage(text=message))

    elif week_num == 3:
        message = "おはようございます！今日は木曜日です。出勤登録をお願いします"
        # user_id = event.source.user_id
        user_id = os.environ["USER_ID"]
        line_bot_api.push_message(user_id, TextSendMessage(text=message))

    elif week_num == 4:
        message = "おはようございます！今日は金曜日です。出勤登録をお願いします"
        # user_id = event.source.user_id
        user_id = os.environ["USER_ID"]
        line_bot_api.push_message(user_id, TextSendMessage(text=message))

    elif week_num == 5:  # テスト用
        message = "おはようございます！今日は土曜日です。出勤登録をお願いします"
        # user_id = event.source.user_id
        user_id = os.environ["USER_ID"]
        line_bot_api.push_message(user_id, TextSendMessage(text=message))
    elif week_num == 6:  # テスト用
        message = "おはようございます！今日は日曜日です。出勤登録をお願いします"
        # user_id = event.source.user_id
        user_id = os.environ["USER_ID"]
        line_bot_api.push_message(user_id, TextSendMessage(text=message))

    else:
        pass

    # print(w_list[week_num], message) 実行OK
    # return message  # なんで赤波線が出るのか…
    print(message)


# rimind_punch_in()  # 動作はOK！


def rimind_punch_out():
    message = ""
    if week_num == 0:
        message = "本日もおつかれさまでした！月曜日の出勤登録をお願いします"
        user_id = os.environ["USER_ID"]
        line_bot_api.push_message(user_id, TextSendMessage(text=message))

    elif week_num == 1:
        message = "本日もおつかれさまでした！火曜日の出勤登録をお願いします"
        # user_id = event.source.user_id
        user_id = os.environ["USER_ID"]
        line_bot_api.push_message(user_id, TextSendMessage(text=message))

    elif week_num == 2:
        message = "本日もおつかれさまでした！水曜日の出勤登録をお願いします"  # 動作確認用。動作OK！print(rimind_punch_in())ではこのメッセージのみ出せた
        user_id = os.environ["USER_ID"]
        line_bot_api.push_message(user_id, TextSendMessage(text=message))

    elif week_num == 3:
        message = "本日もおつかれさまでした！木曜日の出勤登録をお願いします"
        user_id = os.environ["USER_ID"]
        line_bot_api.push_message(user_id, TextSendMessage(text=message))

    elif week_num == 4:
        message = "本日もおつかれさまでした！金曜日の出勤登録をお願いします"
        user_id = os.environ["USER_ID"]
        line_bot_api.push_message(user_id, TextSendMessage(text=message))

    elif week_num == 5:  # テスト用
        message = "本日もおつかれさまでした！土曜日の出勤登録をお願いします"
        user_id = os.environ["USER_ID"]
        line_bot_api.push_message(user_id, TextSendMessage(text=message))
    elif week_num == 6:  # テスト用
        message = "本日もおつかれさまでした！日曜日の出勤登録をお願いします"
        user_id = os.environ["USER_ID"]
        line_bot_api.push_message(user_id, TextSendMessage(text=message))

    else:
        pass

    # print(w_list[week_num], message) 実行OK
    # return message  # message = ""がないと赤波線が出る。return用のmessageがない、ということ
    print(message)


# rimind_punch_out()  # 動作はOK！

if __name__ == "__main__":
    schedule.every().monday.at("08:30").do(rimind_punch_in)
    schedule.every().tuesday.at("08:30").do(rimind_punch_in)
    schedule.every().wednesday.at("08:30").do(rimind_punch_in)
    schedule.every().thursday.at("08:30").do(rimind_punch_in)
    schedule.every().friday.at("08:30").do(rimind_punch_in)
    schedule.every().saturday.at("17:50").do(rimind_punch_in)  # 動作OK！10/14
    schedule.every().sunday.at("11:57").do(rimind_punch_in)

    schedule.every().monday.at("17:30").do(rimind_punch_out)
    schedule.every().tuesday.at("17:30").do(rimind_punch_out)
    schedule.every().wednesday.at("17:30").do(rimind_punch_out)
    schedule.every().thursday.at("17:30").do(rimind_punch_out)
    schedule.every().friday.at("17:30").do(rimind_punch_out)
    schedule.every().saturday.at("17:56").do(rimind_punch_out)  # 動作OK！10/14
    schedule.every().sunday.at("16:44").do(rimind_punch_out)

    while True:
        schedule.run_pending()
        time.sleep(1)
