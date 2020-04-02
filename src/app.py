from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, StickerSendMessage
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

    if event.message.type == "text":
        text = event.message.text

        if text == "search for code":
            content = "請輸入想查詢的銀行"
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=content))
            return 0

        elif text == "let's chat" or text == "send me emoticon":
            content = "不行喔！"
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=content))
            return 0
        
        else:
            matched_banks = [(key + " " + val) for key, val in bank_dist.items() if text in key]
            content = "找不到啦～"
            if len(matched_banks):
                content = "\n".join(matched_banks)
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=content))
            return 0
    
    elif event.message.type == "sticker":
        line_bot_api.reply_message(event.reply_token, StickerSendMessage(package_id=11538, sticker_id=51626512))
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
