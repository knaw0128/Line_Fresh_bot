
import sys
from linebot.models import RichMenu, RichMenuSize, RichMenuArea, RichMenuBounds, URIAction
import sys
from linebot import LineBotApi
from linebot.models.actions import *

channel_access_token = 'cdASOk5uENL6iWSacwmtAwkHjEGuAE//SgTFTjF4+Hole2CBOFH2bCkOWYgoRLmyfoI+ZjCrYfMHgFXnaVnIRFMXjw1G3zEjY+hokaYRIh4U19UNnNNKczN3Q+s+AGoaHA8ZgyTmJh7mfbK8TEU9AgdB04t89/1O/w1cDnyilFU='

if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)

# Create rich menu
rich_menu_to_create = RichMenu(
    size=RichMenuSize(width=2500, height=1686),
    selected=True,
    name="Nice richmenu",
    chat_bar_text="Tap here",
    areas=[RichMenuArea(
        bounds=RichMenuBounds(x=0, y=0, width=2500, height=1686),
        action=MessageAction(label='開始導覽', text='嚮導')
        )]
)
rich_menu_id = line_bot_api.create_rich_menu(rich_menu=rich_menu_to_create)

#upload rich menu
content_type = 'image/png'

with open('./template.png', 'rb') as f:
    line_bot_api.set_rich_menu_image(rich_menu_id, content_type, f)

#set default rich menu
line_bot_api.set_default_rich_menu(rich_menu_id)

print('Set default success.')