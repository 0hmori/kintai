# LINEBot
import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from dotenv import load_dotenv

from kintai import punch_in, punch_out, late, leave_early, delete, rest


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
def handle_message(event):
    print(event.message.text)
    # print(event.source)  # {"type": "user", "userId": "U3457ef080344dc6ce7d0bf86a240108d"}
    # print(event.source.user_id)  # U3457ef080344dc6ce7d0bf86a240108d

    if event.message.text == "出勤":
        userid = event.source.user_id
        punch_in(userid)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="おはようございます！出勤登録完了しました！"))

    elif event.message.text == "退勤":
        userid = event.source.user_id
        punch_out(userid)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="退勤登録完了しました！今日も一日おつかれさまでした"))

    elif event.message.text == "遅刻":
        userid = event.source.user_id
        late(userid)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="おつかれさまです！出勤登録完了しました！"))

    elif event.message.text == "早退":
        userid = event.source.user_id
        leave_early(userid)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="退勤登録完了しました！おつかれさまでした"))

    elif event.message.text == "お休みします":
        userid = event.source.user_id
        rest(userid)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="お休みの登録が完了しました！よいリフレッシュを"))

    elif event.message.text == "修正":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(
                text="出勤時間を修正したいときは「出勤を修正」、"
                "退勤時間を修正したいときは「退勤を修正」、"
                "間違えてお休みを押してしまったときは「お休みを修正」、"
                "と入力して送信をおねがいします！"
            ),
        )

    elif event.message.text == "出勤を修正":
        userid = event.source.user_id
        delete(userid)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="もう一度、正しい勤怠の登録をおねがいします！"))

    elif event.message.text == "退勤を修正":
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="退勤時にもう一度退勤の登録をおねがいします！"))

    elif event.message.text == "お休みを修正":
        userid = event.source.user_id
        delete(userid)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="もう一度、正しい勤怠の登録をおねがいします！"))

    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="こちらは出退勤を管理するBotです。"))


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", debug=True, port=port)  # これももとは()内がなかった
