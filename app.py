# LINEBot
import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from dotenv import load_dotenv

from kintai import punch_in, punch_out


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
    # line_bot_api.reply_message(event.reply_token, TextSendMessage(text=event.message.text))


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
