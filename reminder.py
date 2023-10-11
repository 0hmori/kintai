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

JST = timezone(timedelta(hours=+9), "JST")

load_dotenv()

app = Flask(__name__)


line_bot_api = LineBotApi(os.environ["ACCESS_TOKEN"])
handler = WebhookHandler(os.environ["CHANNEL_SECRET"])


@app.route("/")
def index():
    return "You call index()"


# def hello_world():
#    return "hello きんたい"


@app.route("/push_sample")
def push_sample():
    """プッシュメッセージを送る"""
    user_id = os.environ["USER_ID"]
    line_bot_api.push_message(user_id, TextSendMessage(text="Hello World!"))

    return "OK"


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


@handler.add(MessageEvent, message=TextMessage)
def rimind_punch_in():
    Today = datetime.datetime.today()
    # print(Today)

    weekday_number = Today.weekday()
    week_list = ["月曜日", "火曜日", "水曜日", "木曜日", "金曜日", "土曜日", "日曜日"]
    # print(Today, weekday_number, week_list[weekday_number])

    if weekday_number == 0:
        message = "おはようございます！今日は月曜日です。出勤登録をお願いします"

    elif weekday_number == 1:
        message = "おはようございます！今日は火曜日です。出勤登録をお願いします"  # 動作確認用。動作OK！print(rimind_punch_in())ではこのメッセージのみ出せた

    elif weekday_number == 2:
        message = "おはようございます！今日は水曜日です。出勤登録をお願いします"  # 動作確認用。動作OK！print(rimind_punch_in())ではこのメッセージのみ出せた

    elif weekday_number == 3:
        message = "おはようございます！今日は木曜日です。出勤登録をお願いします"  # 動作確認用。動作OK！print(rimind_punch_in())ではこのメッセージのみ出せた

    elif weekday_number == 4:
        message = "おはようございます！今日は金曜日です。出勤登録をお願いします"  # 動作確認用。動作OK！print(rimind_punch_in())ではこのメッセージのみ出せた

    else:
        pass

    return message  # week_list[weekday_number]を入れないでみた
    # print(message)  # week_list[weekday_number]を入れないと上のリストにエラー。でも出力はできる。


# print(rimind_punch_in())  # このコードでメッセージのみ表示できてるから大丈夫そう？

if __name__ == "__main__":
    schedule.every().monday.at("08:30").do(rimind_punch_in)
    schedule.every().tuesday.at("08:30").do(rimind_punch_in)
    schedule.every().wednesday.at("08:30").do(rimind_punch_in)
    schedule.every().thursday.at("06:15").do(rimind_punch_in)
    schedule.every().friday.at("08:30").do(rimind_punch_in)

    while True:
        schedule.run_pending()
        time.sleep(1)


def rimind_punch_out():
    Today = datetime.datetime.today()
    # print(Today)

    weekday_number = Today.weekday()
    week_list = ["月曜日", "火曜日", "水曜日", "木曜日", "金曜日", "土曜日", "日曜日"]
    # print(Today, weekday_number, week_list[weekday_number])

    if weekday_number == 0:
        message = "退勤時間になりました！退勤登録をお願いします。月曜日、おつかれさまでした"

    elif weekday_number == 1:
        message = "退勤時間になりました！退勤登録をお願いします。火曜日、おつかれさまでした"  # 動作確認用。動作OK！print(rimind_punch_in())ではこのメッセージのみ出せた

    elif weekday_number == 2:
        message = "退勤時間になりました！退勤登録をお願いします。水曜日、おつかれさまでした"  # 動作確認用。動作OK！print(rimind_punch_in())ではこのメッセージのみ出せた

    elif weekday_number == 3:
        message = "退勤時間になりました！退勤登録をお願いします。木曜日、おつかれさまでした"  # 動作確認用。動作OK！print(rimind_punch_in())ではこのメッセージのみ出せた

    elif weekday_number == 4:
        message = "退勤時間になりました！退勤登録をお願いします。金曜日、おつかれさまでした"  # 動作確認用。動作OK！print(rimind_punch_in())ではこのメッセージのみ出せた

    else:
        pass

    return message  # week_list[weekday_number]を入れないでみた
    # print(message)  # week_list[weekday_number]を入れないと上のリストにエラー。でも出力はできる。


# print(rimind_punch_out())  # 動作確認OK


if __name__ == "__main__":
    schedule.every().monday.at("17:30").do(rimind_punch_out)
    schedule.every().tuesday.at("17:30").do(rimind_punch_out)
    schedule.every().wednesday.at("17:30").do(rimind_punch_out)
    schedule.every().thursday.at("06:16").do(rimind_punch_out)
    schedule.every().friday.at("17:30").do(rimind_punch_out)

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
