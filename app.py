# LINEBot
import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from dotenv import load_dotenv

# スプレッドシート
import pandas as pd
from datetime import datetime
from datetime import timedelta
from datetime import timezone
import gspread
from oauth2client.service_account import ServiceAccountCredentials

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


# from chat import chat_completion #openaiを使うとき


# from flask import Flask, request, abort
# from linebot.v3 import WebhookHandler
# from linebot.v3.exceptions import InvalidSignatureError
# from linebot.v3.messaging import Configuration, ApiClient, MessagingApi, ReplyMessageRequest, TextMessage
# from linebot.v3.webhooks import MessageEvent, TextMessageContent

# import os

load_dotenv()

app = Flask(__name__)

# YOUR_CHANNEL_ACCESS_TOKEN = "OoB9ut4VSSLf3KdTqtQB2Ipw56UR3b/2Fs1HpdsonnSsW6eUDnLohABExT++Z8KsEP+xXHrCwPgRr/pAFeeSMWc/k5qD2sTxqd1sPHOyvRGYXzXoTbZgzjC27ka5c95hytOobbTcYgUrLUPeaG9LwwdB04t89/1O/w1cDnyilFU="
# YOUR_CHANNEL_SECRET = "c873c48a14dcbb1633f938da547b5c48"

# configuration = Configuration(YOUR_CHANNEL_ACCESS_TOKEN)
# handler = WebhookHandler(YOUR_CHANNEL_SECRET)

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

    # get X-Line-Signature header value
    # signature = request.headers["X-Line-Signature"]

    ## get request body as text
    # body = request.get_data(as_text=True)
    # app.logger.info("Request body: " + body)

    ## handle webhook body
    # try:
    #    handler.handle(body, signature)
    # except InvalidSignatureError:
    #    app.logger.info("Invalid signature. Please check your channel access token/channel secret.")
    #    abort(400)

    # return "OK"


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if event.message.text == "出勤":
        punch_in()
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="出勤登録完了しました！"))

    elif event.message.text == "退勤":
        punch_out()
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="退勤登録完了しました！"))

    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="こちらは出退勤を管理するBotです。"))

    #    reply_message = chat_completion(event.message.text)
    # text = "ぽめらにあん"  TextSendMessage(text=text)) 次にこうした
    # text = event.message.text まずこれをやった。送られたメッセージをそのまま送り返す
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=event.message.text))


# def handle_message(event):
#   #    text = event.message.text
#    reply_message = chat_completion(event.message.text)
#    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_message))


# @handler.add(MessageEvent, message=TextMessageContent)
# def handle_message(event):
#    with ApiClient(configuration) as api_client:
#        line_bot_api = MessagingApi(api_client)
#        line_bot_api.reply_message_with_http_info(
#            ReplyMessageRequest(
#                reply_token=event.reply_token, messages=[TextMessage(text=event.message.text)]
#            )
#        )


if __name__ == "__main__":
    #    port = os.getenv("POST")  # このへんよくわからない、追加したコード
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)  # これももとは()内がなかった
