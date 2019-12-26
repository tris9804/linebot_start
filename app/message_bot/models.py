from django.db import models


class BotUser(models.Model):
    PLATFORM_LINE = 'line' #被資料庫儲存的
    PLATFORM_CHOICES = (
        (PLATFORM_LINE, 'Line') ,
    ) #顯示給使用者的


    STATE_NO = 'no'
    STATE_ECHO = 'echo'
    STATE_REVERSED = 'reversed'
    STATE_CHOICES = (
        (STATE_NO, '無'),
        (STATE_ECHO , '應聲蟲'),
        (STATE_REVERSED, '訊息反轉'),
    )

    platform =models.CharField(max_length=255, choices=PLATFORM_CHOICES)
    user_id = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    state = models.CharField(max_length=255, choices=STATE_CHOICES)

    def __str__(self):
        return f'{self.get_platform_display()} - {self.user_id}'
        #get_platform_display 是顯示使用者的platform name