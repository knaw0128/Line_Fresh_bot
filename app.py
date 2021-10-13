import os
from types import BuiltinMethodType

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

food_list = []
with open("food.csv", encoding='UTF-8') as csvfile:
    rows = csv.reader(csvfile)
    for food in rows:
        food_list.append(food)

origin_list = []
with open("origin.csv", encoding='UTF-8') as csvfile:
    rows = csv.reader(csvfile)
    for origin in rows:
        origin_list.append(origin)

hotel_list = []
with open("hotel.csv", encoding='UTF-8') as csvfile:
    rows = csv.reader(csvfile)
    for hotel in rows:
        hotel_list.append(hotel)


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
    if action=="Start" or action=="start":
        output = TemplateSendMessage(
            alt_text="hello",
            template=ButtonsTemplate(
                thumbnail_image_url='https://tour.taitung.gov.tw/image/827/1024x768',
                title='鐵花村嚮導',
                text='臺東夜不寂寞，來到鐵花村音樂聚落\n享受山海文化孕育出澎湃的歌聲\n來喝上一杯鐵花吧的臺東特調吧！',
                actions=[
                    PostbackAction(
                        label='美食&飲品',
                        data='$$美食&飲品$$'
                    ),
                    PostbackAction(
                        label='原創商品',
                        data='$$原創商品$$'
                    ),
                    PostbackAction(
                        label='旅館',
                        data='$$旅館$$'
                    ),
                    URIAction(
                        label = '表演時程表',
                        uri="http://www.tiehua.com.tw/calendar.php?p="
                    )
                ],
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
                                label='使用',
                                data='$$Eating$$'
                            ),
                            PostbackAction(
                                label='儲存',
                                data='$$Eating$$'
                            ),
                        ]),
                    CarouselColumn(
                        thumbnail_image_url='https://tour.taitung.gov.tw/image/827/1024x768',
                        title = '國旅券',
                        text = '您還有        點',
                        actions=[
                            PostbackAction(
                                label='使用',
                                data='$$Eating$$'
                            ),
                            PostbackAction(
                                label='儲存',
                                data='$$Eating$$'
                            ),
                        ]),
                    CarouselColumn(
                        thumbnail_image_url='https://tour.taitung.gov.tw/image/827/1024x768',
                        title = '動滋券',
                        text = '您還有        點',
                        actions=[
                            PostbackAction(
                                label='使用',
                                data='$$Eating$$'
                            ),
                            PostbackAction(
                                label='儲存',
                                data='$$Eating$$'
                            ),
                        ]),
                    CarouselColumn(
                        thumbnail_image_url='https://tour.taitung.gov.tw/image/827/1024x768',
                        title = '藝fun券',
                        text = '您還有        點',
                        actions=[
                            PostbackAction(
                                label='使用',
                                data='$$Eating$$'
                            ),
                            PostbackAction(
                                label='儲存',
                                data='$$Eating$$'
                            ),
                        ]),
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
    if action == "$$美食&飲品$$":
        rand = random.randint(1, len(food_list))
        replyContent = "今天我推薦來點" + food_list[rand][0] +"\n" +food_list[rand][1]
        output = TextSendMessage(text=replyContent)
    elif action == "$$原創商品$$":
        rand = random.randint(1, len(origin_list))
        replyContent = "今天我推薦來點" + origin_list[rand][0] +"\n" +origin_list[rand][1]
        output = TextSendMessage(text=replyContent)
    elif action == "$$旅館$$":
        rand = random.randint(1, len(hotel_list))
        replyContent = "今天我推薦住在" + hotel_list[rand][0] +"\n" +hotel_list[rand][1]
        output = TextSendMessage(text=replyContent)

    
    line_bot_api.reply_message(
        event.reply_token,
        output
    )

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)