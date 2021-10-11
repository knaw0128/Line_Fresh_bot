import os

from linebot.models.flex_message import FlexSendMessage

if os.getenv('DEVELOPMENT') is not None:
    from dotenv import load_dotenv

    load_dotenv(dotenv_path='../.env')

import sys
import random, csv

from flask import Flask, request, abort
from linebot import *
from linebot.exceptions import *
from linebot.models import *

app = Flask(__name__)

# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv('LINE_CHANNEL_SECRET') or 'YOUR_SECRET'
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN') or 'YOUR_ACCESS_TOKEN'

if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    # app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def message_text(event):
    action = event.message.text
    if action=="start":
        output = TemplateSendMessage(
            alt_text='Buttons template',
            template=ButtonsTemplate(
                thumbnail_image_url='https://tour.taitung.gov.tw/image/827/1024x768',
                title='鐵花村嚮導',
                text='臺東夜不寂寞，來到鐵花村音樂聚落\n享受山海文化孕育出澎湃的歌聲\n來喝上一杯鐵花吧的臺東特調吧！',
                actions=[
                    PostbackAction(
                        label='美食'
                        data='$$美食$$'
                    ),
                    PostbackAction(
                        label='飲品',
                        data='$$飲品$$'
                    ),
                    PostbackAction(
                        label='原創商品',
                        data='$$原創商品$$'
                    ),
                    PostbackAction(
                        label='旅館',
                        data='$$旅館$$'
                    ),
                    PostbackAction(
                        label='音樂聚落',
                        data='$$音樂聚落$$'
                    )],
                default_action=URIAction(
                    uri="https://www.facebook.com/tiehua/"
                )
            )
        )
    elif action == '優惠券':
        output = TemplateSendMessage(
            alt_text='TemplateSendMessage template',
            template = CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url='https://tour.taitung.gov.tw/image/827/1024x768',
                        title = '好食券',
                        text = '您還有        點',
                        actions=[
                            PostbackAction(
                                label='Eating',
                                data='$$Eating$$'
                            ),
                            PostbackAction(
                                label='Eating',
                                data='$$Eating$$'
                            ),
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://tour.taitung.gov.tw/image/827/1024x768',
                        title = '國旅券',
                        text = '您還有        點',
                        actions=[
                            PostbackAction(
                                label='Eating',
                                data='$$Eating$$'
                            ),
                            PostbackAction(
                                label='Eating',
                                data='$$Eating$$'
                            ),
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://tour.taitung.gov.tw/image/827/1024x768',
                        title = '動滋券',
                        text = '您還有        點',
                        actions=[
                            PostbackAction(
                                label='Eating',
                                data='$$Eating$$'
                            ),
                            PostbackAction(
                                label='Eating',
                                data='$$Eating$$'
                            ),
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://tour.taitung.gov.tw/image/827/1024x768',
                        title = '藝fun券',
                        text = '您還有        點',
                        actions=[
                            PostbackAction(
                                label='Eating',
                                data='$$Eating$$'
                            ),
                            PostbackAction(
                                label='Eating',
                                data='$$Eating$$'
                            ),
                        ]
                    ),
                ]
            )
        )
    
    line_bot_api.reply_message(
        event.reply_token,
        output
    )

@handler.add(PostbackEvent)
def handle_postback(event):
    action = event.postback.data
    if action == "$$美食$$":
        rows_list = []
        with open(os.path.abspath("food.csv"), newline='') as csvfile:
            rows = csv.reader(csvfile, delimiter=',')
            for row in rows:
                rows_list.append(row)

        rand = random.randint(0,4)
        line_bot_api.reply_message(
            event.reply_token,
            output = TextSendMessage(text=str(rows_list[rand]))
        )

        # replyContent = "今天我推薦來點" + repo[now] +"\n" +links[repo[now]]
        # output = TextSendMessage(text=replyContent)

    elif action == "$$飲品$$":
        output = TextSendMessage(text="賣喝的")
    elif action == "$$原創商品$$":
        output = TextSendMessage(text="賣穿的")
    elif action == "$$旅館$$":
        output = TextSendMessage(text="賣住的")
    elif action == "$$音樂聚落$$":
        replyContent = "由此查看演出時間" + "\n" + "http://www.tiehua.com.tw/calendar.php?p=5"
        output = TextSendMessage(text=replyContent)
    
    line_bot_api.reply_message(
        event.reply_token,
        output
    )

# @handler.add(PostbackEvent)
# def handle_postback(event):
#     action = event.postback.data
#     if action == "$$Eating$$":
#         links = {
#             "炒上鮮平價熱炒" : "https://spot.line.me/detail/486251123917723842",
#             "何家寨土雞城" : "https://spot.line.me/detail/486257421489019364",
#             "圓圓小吃店" : "https://spot.line.me/detail/486257089434360139",
#         }
#         repo = [
#             "炒上鮮平價熱炒",
#             "何家寨土雞城",
#             "圓圓小吃店",
#         ]
#         now = random.randint(0,2)
#         replyContent = "今天我推薦來點" + repo[now] +"\n" +links[repo[now]]
#         output = TextSendMessage(text=replyContent)
#     elif action == "$$Drinking$$":
#         output = TextSendMessage(text="賣喝的")
#     elif action == "$$Dressing$$":
#         output = TextSendMessage(text="賣穿的")
#     elif action == "$$Hotels$$":
#         output = TextSendMessage(text="賣住的")
    
#     line_bot_api.reply_message(
#         event.reply_token,
#         output
#     )



# # CSV Example
# import csv
# @handler.add(MessageEvent, message=TextMessage)
# def message_text(event):
#     action = event.message.text
#     if action=="showdata":
#         rows_list = []
#         with open(os.path.abspath("guide-data.csv"), newline='') as csvfile:
#             rows = csv.reader(csvfile, delimiter=',')
#             for row in rows:
#                 rows_list.append(row)

#         line_bot_api.reply_message(
#             event.reply_token,
#             TextSendMessage(text=str(rows_list[1]))
#         )


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
