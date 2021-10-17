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
with open("./csv_file/food.csv", encoding='UTF-8') as csvfile:
    rows = csv.reader(csvfile)
    for food in rows:
        food_list.append(food)

origin_list = []
with open("./csv_file/origin.csv", encoding='UTF-8') as csvfile:
    rows = csv.reader(csvfile)
    for origin in rows:
        origin_list.append(origin)

hotel_list = []
with open("./csv_file/hotel.csv", encoding='UTF-8') as csvfile:
    rows = csv.reader(csvfile)
    for hotel in rows:
        hotel_list.append(hotel)

singer_list = []
with open("./csv_file/singer.csv", encoding='UTF-8') as csvfile:
    rows = csv.reader(csvfile)
    for singer in rows:
        singer_list.append(singer)


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
            alt_text="開始探索",
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
                        label='優惠券',
                        data='$$優惠券$$'
                    ),
                    PostbackAction(
                        label='音樂聚落',
                        data='$$音樂聚落$$'
                    ),
                ],
                default_action=URIAction(
                    uri="https://www.facebook.com/tiehua/"
                )
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
        rand = random.randint(1, len(food_list)-1)
        replyContent = "今天我推薦來點" + food_list[rand][0] +"\n" +food_list[rand][1]
        output = TextSendMessage(text=replyContent)
    elif action == "$$原創商品$$":
        rand = random.randint(1, len(origin_list)-1)
        replyContent = "今天我推薦來點" + origin_list[rand][0] +"\n" +origin_list[rand][1]
        output = TextSendMessage(text=replyContent)
    elif action == "$$優惠券$$":
        output = TemplateSendMessage(
            alt_text='查看優惠券',
            template = CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url='https://imgur.com/5wPPLxb.png',
                        title = '好食券',
                        text = '您剩餘    張',
                        actions=[
                            PostbackAction(
                                label='使用',
                                data='$$Eating$$'
                            ),
                            PostbackAction(
                                label='更多優惠資訊',
                                data='$$Eating$$'
                            ),
                        ]),
                    CarouselColumn(
                        thumbnail_image_url='https://imgur.com/UusvBQG.png',
                        title = '好喝券',
                        text = '您剩餘    張',
                        actions=[
                            PostbackAction(
                                label='使用',
                                data='$$Eating$$'
                            ),
                            PostbackAction(
                                label='更多優惠資訊',
                                data='$$Eating$$'
                            ),
                        ]),
                    CarouselColumn(
                        thumbnail_image_url='https://imgur.com/0mR3d9i.png',
                        title = '動聽券',
                        text = '您剩餘    張',
                        actions=[
                            PostbackAction(
                                label='使用',
                                data='$$Eating$$'
                            ),
                            PostbackAction(
                                label='更多優惠資訊',
                                data='$$Eating$$'
                            ),
                        ]),
                    CarouselColumn(
                        thumbnail_image_url='https://imgur.com/u0yZEyl.png',
                        title = '好穿券',
                        text = '您剩餘    張',
                        actions=[
                            PostbackAction(
                                label='使用',
                                data='$$Eating$$'
                            ),
                            PostbackAction(
                                label='更多優惠資訊',
                                data='$$Eating$$'
                            ),
                        ]),
                ]
            )
        )
    elif action == "$$音樂人介紹$$":
        rand_list = []
        for i in range(4):
            new = random.randint(1, len(singer_list)-1)
            while new in rand_list:
                new = random.randint(1, len(singer_list)-1)
            rand_list.append(new)
        print(rand_list)
        output = TemplateSendMessage(
            alt_text='音樂人介紹',
            template = ImageCarouselTemplate(
                columns=[
                    ImageCarouselColumn(
                        image_url= singer_list[rand_list[0]][1],
                        action=URIAction(
                            label= singer_list[rand_list[0]][0],
                            uri = singer_list[rand_list[0]][2]
                        )
                    ),
                    ImageCarouselColumn(
                        image_url= singer_list[rand_list[1]][1],
                        action=URIAction(
                            label= singer_list[rand_list[1]][0],
                            uri = singer_list[rand_list[1]][2]
                        )
                    ),
                    ImageCarouselColumn(
                        image_url= singer_list[rand_list[2]][1],
                        action=URIAction(
                            label= singer_list[rand_list[2]][0],
                            uri = singer_list[rand_list[2]][2]
                        )
                    ),
                    ImageCarouselColumn(
                        image_url= singer_list[rand_list[3]][1],
                        action=URIAction(
                            label= singer_list[rand_list[3]][0],
                            uri = singer_list[rand_list[3]][2]
                        )
                    ),
                ]
            )
        )
    elif action == "$$音樂聚落$$":
        output =  TemplateSendMessage(
            alt_text="音樂聚落",
            template=ButtonsTemplate(
                thumbnail_image_url='https://tour.taitung.gov.tw/image/827/1024x768',
                title='音樂聚落',
                text='臺東夜不寂寞，來到鐵花村音樂聚落\n享受山海文化孕育出澎湃的歌聲\n來喝上一杯鐵花吧的臺東特調吧！',
                actions=[
                    URIAction(
                        label='加入社群',
                        uri='https://line.me/ti/g2/5Y44ZfaIkAe33o5P1DLy4NnhzAdDZzlW7MBrKw?utm_source=invitation&utm_medium=link_copy&utm_campaign=default'
                    ),
                    URIAction(
                        label='暢遊音樂',
                        uri='https://music-tw.line.me/playlist/273?playlistId=273'
                    ),
                    PostbackAction(
                        label = '音樂人介紹',
                        data = '$$音樂人介紹$$'
                    ),
                ],
                default_action=URIAction(
                    uri="http://www.tiehua.com.tw/calendar.php?p=5"
                )
            )
        )

    
    line_bot_api.reply_message(
        event.reply_token,
        output
    )

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
