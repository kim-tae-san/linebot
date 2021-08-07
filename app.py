
from __future__ import unicode_literals

import os
import sys
from argparse import ArgumentParser

from flask import jsonify

from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookParser
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

from papago import translate

app = Flask(__name__)

# get channel_secret and channel_access_token from your environment variable
channel_secret = '0c537bb765d08bd12c8f213655e50fb7'
channel_access_token = 'Pe+d4QE6/6cr+eHAKjyZhuv81UsgYyhd41MTZirgM242zPOGrEGMDGHsLCjoZAlSfS6SJ5FFm5KoDgUAjx/JlwOy9g9YZVfG3CciB/jXF+bCQwoEubbG0bNP6rRnZRMWC5m300ZRaxlNbdR97ToxyQdB04t89/1O/w1cDnyilFU='

line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)


@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue

        # Translate
        translated = translate(event.message.text)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=translated)
        )

    return 'OK'


if __name__ == "__main__":
    arg_parser = ArgumentParser(
        usage='Usage: python ' + __file__ + ' [--port <port>] [--help]'
    )
    arg_parser.add_argument('-p', '--port', default=8000, help='port')
    arg_parser.add_argument('-d', '--debug', default=False, help='debug')
    options = arg_parser.parse_args()

    app.run(debug=options.debug, port=options.port)
