from app.message_bot.models import BotUser

from linebot.models import (
    TemplateSendMessage, ButtonsTemplate,
    PostbackTemplateAction,
    TextSendMessage,
)



def state_no(event, user):
    
    # return TextSendMessage(f'HI, {line_user.display_name}')

    return TemplateSendMessage(
        alt_text='請選擇要進入的模式',
        template = ButtonsTemplate(
            title='模式選擇',
            text='請選擇模式',
            actions=[
                PostbackTemplateAction(
                    label='應聲蟲',
                    data=BotUser.STATE_ECHO,
                ),
                PostbackTemplateAction(
                    label='訊息反轉',
                    data=BotUser.STATE_REVERSED,
                ),
            ]
        )
    )


def state_echo(event, user):
    return TextSendMessage(event.message.text)


def state_reversed(event, user):
    return TextSendMessage(event.message.text[::-1])