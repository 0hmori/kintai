# import pandas as pd
import datetime
from datetime import timedelta
from datetime import timezone

# from oauth2client.service_account import ServiceAccountCredentials
import schedule


import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from dotenv import load_dotenv
import time
import locale

JST = timezone(timedelta(hours=+9), "JST")

load_dotenv()

app = Flask(__name__)


line_bot_api = LineBotApi(os.environ["ACCESS_TOKEN"])
handler = WebhookHandler(os.environ["CHANNEL_SECRET"])


# @app.route("/push_sample")
# def push_sample():
#    """プッシュメッセージを送る"""
#    user_id = os.environ["USER_ID"]
#    line_bot_api.push_message(user_id, TextSendMessage(text="Hello,world"))
#
#    return "OK"

@app.route("/callback", methods=["GET", "POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:  # as e:を消した！
        abort(400)

    return "OK"


locale.setlocale(locale.LC_TIME, "ja_JP.UTF-8")
Today = datetime.datetime.now()
week_num = Today.weekday()
w_list = ["月曜日", "火曜日", "水曜日", "木曜日", "金曜日", "土曜日", "日曜日"]

# print(Today,  week_num,  w_list[week_num]) 実行OK


@app.route("/rimind_punch_in")
def rimind_punch_in():
    if week_num == 0:
        message = "おはようございます！今日は月曜日です。出勤登録をお願いします"
        # LINE_Notify.Sent_Message(message)
        user_id = os.environ["USER_ID"]
        line_bot_api.push_message(user_id, TextSendMessage(text=message))

    elif week_num == 1:
        message = "おはようございます！今日は火曜日です。出勤登録をお願いします"
        user_id = os.environ["USER_ID"]
        line_bot_api.push_message(user_id, TextSendMessage(text=message))

    elif week_num == 2:
        message = "おはようございます！今日は水曜日です。出勤登録をお願いします"  # 動作確認用。動作OK！print(rimind_punch_in())ではこのメッセージのみ出せた
        user_id = os.environ["USER_ID"]
        line_bot_api.push_message(user_id, TextSendMessage(text=message))

    elif week_num == 3:
        message = "おはようございます！今日は木曜日です。出勤登録をお願いします"
        user_id = os.environ["USER_ID"]
        line_bot_api.push_message(user_id, TextSendMessage(text=message))

    elif week_num == 4:
        message = "おはようございます！今日は金曜日です。出勤登録をお願いします"
        user_id = os.environ["USER_ID"]
        line_bot_api.push_message(user_id, TextSendMessage(text=message))

    else:
        pass

    # print(w_list[week_num], message) 実行OK
    return message  # なんで赤波線が出るのか…


#rimind_punch_in()  # 動作確認OK！


if __name__ == "__main__":
    schedule.every().monday.at("08:30").do(rimind_punch_in)
    schedule.every().tuesday.at("08:30").do(rimind_punch_in)
    schedule.every().wednesday.at("08:30").do(rimind_punch_in)
    schedule.every().thursday.at("08:30").do(rimind_punch_in)
    schedule.every().friday.at("06:27").do(rimind_punch_in)

    while True:
        schedule.run_pending()
        time.sleep(1)