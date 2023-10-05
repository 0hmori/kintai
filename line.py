from flask import Flask, request, abort

from linebot.v3 import (
    WebhookHandler
)
from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent
)

app = Flask(__name__)

YOUR_CHANNEL_ACCESS_TOKEN = "OoB9ut4VSSLf3KdTqtQB2Ipw56UR3b/2Fs1HpdsonnSsW6eUDnLohABExT++Z8KsEP+xXHrCwPgRr/pAFeeSMWc/k5qD2sTxqd1sPHOyvRGYXzXoTbZgzjC27ka5c95hytOobbTcYgUrLUPeaG9LwwdB04t89/1O/w1cDnyilFU="
YOUR_CHANNEL_SECRET = "c873c48a14dcbb1633f938da547b5c48"

configuration = Configuration(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)


@app.route("/")
def hello_world():
    return "hello きんたい"


@app.route("/callback", methods=["POST"])
def callback():
    # get X-Line-Signature header value
    signature = request.headers["X-Line-Signature"]

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        app.logger.info("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return "OK"


@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token, messages=[TextMessage(text=event.message.text)]
            )
        )


if __name__ == "__main__":
    app.run()
