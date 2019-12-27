from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

from linebot import LineBotApi, WebhookParser, WebhookHandler
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, ImageMessage, TextMessage, PostbackEvent, TextSendMessage, ImageSendMessage

# import line funtion
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
                    if mtext == '@傳送文字':
                        linebot_func.sendText(event)
                        return HttpResponse()
                    elif mtext == '@傳送圖片':
                        linebot_func.sendImage(event)
                        return HttpResponse()
                    elif mtext == '@按鈕樣板':
                        linebot_func.sendButton(event)
                        return HttpResponse()
                    elif mtext == '@確認樣板':
                        linebot_func.sendQuickreply(event)
                        return HttpResponse()
                    elif mtext == '@轉盤位置':
                        linebot_func.sendConfirm(event)
                        return HttpResponse()
                    elif mtext == '@快速選單':
                        linebot_func.sendCarousel(event)
                        return HttpResponse()

                elif isinstance(event.message,ImageMessage):
                    #########################################  這邊判斷到是照片 ###########################################
                    line_bot_api.reply_message(event.reply_token, TextSendMessage(text='你傳送到照片了'))
                    return HttpResponse()

                else:
                    ################################   這邊判斷到 文字 或 圖片外的東西 #########################################
                    line_bot_api.reply_message(event.reply_token, TextSendMessage(text='你傳了到圖片了'))
                    return HttpResponse()
                
            print("到文字、圖片或不三不四的表情區塊後，會跑到這，如果拿掉下面那行，會跑到 下面的 第三禁區 ")
            return HttpResponse()
        
        print("第三禁區")
        return HttpResponse()
    
    else:
        print("第四禁區")
        return HttpResponseBadRequest()
