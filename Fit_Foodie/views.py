from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

from linebot import LineBotApi, WebhookParser,WebhookHandler
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, ImageMessage ,TextMessage, PostbackEvent,TextSendMessage ,ImageSendMessage
from urllib.parse import parse_qsl

from linebot_func import linebot_func

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(settings.LINE_CHANNEL_SECRET)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)



def error_cb(err):
    print('Error: %s' % err)


@csrf_exempt
def callback(request):
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')
        try:
            events = parser.parse(body, signature)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()

        for event in events:
            if isinstance(event, MessageEvent):
                if isinstance(event.message, TextMessage):
                    mtext = event.message.text
                    if mtext == '@食譜查詢':
                        linebot_func.sendText(event)
                        return HttpResponse()
                    elif mtext == '@個人化推薦':
                        linebot_func.sendFlex(event)
                        return HttpResponse()
                    elif mtext == '@熱門推薦':
                        linebot_func.sendFlex(event)
                        return HttpResponse()
                    elif mtext == '@問卷':
                        linebot_func.sendCarousel(event)
                        return HttpResponse()
                    elif mtext == '@yes':
                        linebot_func.sendYes(event)
                        return HttpResponse()
                    elif mtext == '@no':
                        linebot_func.sendNo(event)
                        return HttpResponse()
                    elif mtext[:3] == '###' and len(mtext) > 3:
                        linebot_func.manageForm(event, mtext)
                        return HttpResponse()
                    
            # PostbackTemplateAction觸發此事件
            if isinstance(event, PostbackEvent):
                # 取得Postback資料
                backdata = dict(parse_qsl(event.postback.data))
                if backdata.get('action') == 'buy':
                    linebot_func.sendBack_buy(event, backdata)
                elif backdata.get('action') == 'sell':
                    linebot_func.sendBack_sell(event, backdata)


            print("到文字、圖片或不三不四的表情區塊後，會跑到這，如果拿掉下面那行，會跑到 下面的 第三禁區 ")
            return HttpResponse()

        print("第三禁區")
        return HttpResponse()

    else:
        print("第四禁區")
        return HttpResponseBadRequest()

