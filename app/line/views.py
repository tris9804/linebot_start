from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from linebot.exceptions import InvalidSignatureError

from .handlers import handler

@require_POST
@csrf_exempt
def webhook(request):
    signature = request.META.get('HTTP_X_LINE_SIGNATURE') #分辨LINEserver request Django要使用META
    body = request.body.decode('utf-8') #用文字的型態拿到http body


    try:
        handler.handle(body, signature) #判斷非法簽章

    except InvalidSignatureError:
        return HttpResponseBadRequest()

    return HttpResponse('OK')