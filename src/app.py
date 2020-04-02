from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import os
import random

app = Flask(__name__)

from config import *
from data import *

app = Flask(__name__)

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # line_bot_api.reply_message(
    #     event.reply_token,
    #     TextSendMessage(text=event.message.text))

    text = event.message.text.lower()

    if text == "search for code":
        content = "請輸入"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=content))
        return 0

    if text == "let's chat" or text == "send me emoticon":
        content = "不行喔！"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=content))
        return 0
    
    if text:
        matched_banks = [(key + " " + val) for key, val in bank_dist.items() if text in key]
        content = "\n".join(matched_banks)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=content))
        return 0

    random_set = [
        "嗨嗨嗨",
        "晚餐要吃什麼？",
        "笨蛋笨笨",
        "嚕嚕嚕嗶嚕"
    ]

    secure_random = random.SystemRandom()
    content = secure_random.choice(random_set)
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=content))


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
