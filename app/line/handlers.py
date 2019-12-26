from app.message_bot.models import BotUser
from core.settings import LINE_ACCESS_TOKEN, LINE_SECRET

from linebot import LineBotApi, WebhookHandler
from linebot.models import (
    FollowEvent, TextSendMessage, 
    MessageEvent, TextMessage,
    PostbackEvent,
)

from . import states

bot = LineBotApi(LINE_ACCESS_TOKEN)
handler = WebhookHandler(LINE_SECRET) #處理不同的狀態

def get_bot_user(user_id):
    name = bot.get_profile(user_id).display_name
    bot_user, created = BotUser.objects.get_or_create(
        platform = BotUser.PLATFORM_LINE,
        user_id = user_id,
        defaults = {
            'state': BotUser.STATE_NO,
            'name': name,
        },
    ) #get or create 判斷資料庫的user 沒有就建立 解除封鎖 #client user_id

    return bot_user


@handler.add(FollowEvent) #加好友的event 使用這個func
def handle_follow(event):
    bot_user = get_bot_user(event.source.user_id)
    message = getattr(states, f'state_{bot_user.state}')(event, bot_user) #呼叫使用者的狀態對應的ㄏㄧ

    bot.reply_message(event.reply_token, message)


@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    bot_user = get_bot_user(event.source.user_id)

    # if event.message.text =='我要進入應聲蟲模式':
    #     bot_user.state = BotUser.STATE_ECHO
    #     bot_user.save()
    #     return
    # elif event.message.text =='我要進入訊息反轉模式':
    #     bot_user.state = BotUser.STATE_REVERSED
    #     bot_user.save()
    #     return  使用POSTBACK

    message = getattr(states, f'state_{bot_user.state}')(event, bot_user) #呼叫使用者的狀態對應的狀態

    if message is None:
        return

    bot.reply_message(event.reply_token, message)

    # bot.reply_message(
    #     event.reply_token,
    #     TextSendMessage(event.message.text),
    # ) #應聲蟲


@handler.add(PostbackEvent)
def handle_image_messgae(event):
    bot_user = get_bot_user(event.source.user_id)
    bot_user.state = event.postback.data
    bot_user.save()

    bot.reply_message(
        event.reply_token, 
        TextSendMessage(f'狀態完成 "{bot_user.get_state_display()}" 模式')
    )   #調整訊息按鈕的回應