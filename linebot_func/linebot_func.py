from django.conf import settings

from linebot import LineBotApi
from linebot.models import TextSendMessage, ImageSendMessage, TemplateSendMessage, QuickReplyButton, MessageAction, ButtonsTemplate, MessageTemplateAction, URITemplateAction, PostbackTemplateAction, ConfirmTemplate, CarouselTemplate, CarouselColumn, QuickReply, TextSendMessage, BubbleContainer, ImageComponent, BoxComponent, TextComponent, IconComponent, ButtonComponent, SeparatorComponent, FlexSendMessage, URIAction, ImageCarouselTemplate, ImageCarouselColumn


line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)

#1
def sendText(event):  #傳送文字
    try:
        message = TextSendMessage(
            text = "嗨您好~歡迎使用小助手\n請於下方選擇需要的訊息唷"
        )
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
#2
def sendFlex(event):  #彈性配置
    try:
        bubble = BubbleContainer(
            direction='ltr',  #項目由左向右排列
            header=BoxComponent(  #標題
                layout='vertical',
                contents=[
                    TextComponent(text='冰火飲料', weight='bold', size='xxl'),
                ]
            ),
            hero=ImageComponent(  #主圖片
                url='https://i.imgur.com/3sBRh08.jpg',
                size='full',
                aspect_ratio='792:555',  #長寬比例
                aspect_mode='cover',
            ),
            body=BoxComponent(  #主要內容
                layout='vertical',
                contents=[
                    TextComponent(text='評價', size='md'),
                    BoxComponent(
                        layout='baseline',  #水平排列
                        margin='md',
                        contents=[
                            IconComponent(size='lg', url='https://i.imgur.com/GsWCrIx.png'),
                            TextComponent(text='25   ', size='sm', color='#999999', flex=0),
                            IconComponent(size='lg', url='https://i.imgur.com/sJPhtB3.png'),
                            TextComponent(text='14', size='sm', color='#999999', flex=0),
                        ]
                    ),
                    BoxComponent(
                        layout='vertical',
                        margin='lg',
                        contents=[
                            BoxComponent(
                                layout='baseline',
                                contents=[
                                    TextComponent(text='營業地址:', color='#aaaaaa', size='sm', flex=2),
                                    TextComponent(text='台北市信義路14號', color='#666666', size='sm', flex=5)
                                ],
                            ),
                            SeparatorComponent(color='#0000FF'),
                            BoxComponent(
                                layout='baseline',
                                contents=[
                                    TextComponent(text='營業時間:', color='#aaaaaa', size='sm', flex=2),
                                    TextComponent(text="10:00 - 23:00", color='#666666', size='sm', flex=5),
                                ],
                            ),
                        ],
                    ),
                    BoxComponent(
                        layout='horizontal',
                        margin='xxl',
                        contents=[
                            ButtonComponent(
                                style='primary',
                                height='sm',
                                action=URIAction(label='電話聯絡', uri='tel:0987654321'),
                            ),
                            ButtonComponent(
                                style='secondary',
                                height='sm',
                                action=URIAction(label='查看網頁', uri="http://www.e-happy.com.tw")
                            )
                        ]
                    )
                ],
            ),
            footer=BoxComponent(  #底部版權宣告
                layout='vertical',
                contents=[
                    TextComponent(text='Copyright@ehappy studio 2019', color='#888888', size='sm', align='center'),
                ]
            ),
        )
        message = FlexSendMessage(alt_text="彈性配置範例", contents=bubble)
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))

def manageForm(event, mtext):
    try:
        flist = mtext[3:].split('/')
        text1 = '姓名：' + flist[0] + '\n'
        text1 += '日期：' + flist[1] + '\n'
        text1 += '包廂：' + flist[2]
        message = TextSendMessage(
            text = text1
        )
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
#3
def sendButton(event):  #按鈕樣版
    try:
        message = TemplateSendMessage(
            alt_text='按鈕樣板',
            template=ButtonsTemplate(
                thumbnail_image_url='https://i.imgur.com/4QfKuz1.png',  #顯示的圖片
                title='按鈕樣版示範',  #主標題
                text='請選擇：',  #副標題
                actions=[
                    MessageTemplateAction(  #顯示文字計息
                        label='熱門食譜推薦',
                        text='@熱門食譜推薦'
                    ),
                    URITemplateAction(  #開啟網頁
                        label='連結網頁',
                        uri='http://www.e-happy.com.tw'
                    ),
                    PostbackTemplateAction(  #執行Postback功能,觸發Postback事件
                        label='搜尋中請稍後',  #按鈕文字
                        text='@搜尋中請稍後',  #顯示文字訊息
                        data='action=buy'  #Postback資料
                    ),
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
#5
def sendConfirm(event):  #確認樣板
    try:
        message = TemplateSendMessage(
            alt_text='確認樣板',
            template=ConfirmTemplate(
                text='查詢請依以下格式\n食材1,食材2,食材3',
                actions=[
                    MessageTemplateAction(  #按鈕選項
                        label='是',
                        text='@yes'
                    ),
                    MessageTemplateAction(
                        label='否',
                        text='@no'
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))


def sendCarousel(event):  #轉盤樣板
    try:
        message = TemplateSendMessage(
            alt_text='轉盤樣板',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/4QfKuz1.png',
                        title='這是樣板1',
                        text='第1個轉盤樣板',
                        actions=[
                            URITemplateAction(
                                label='連結文淵閣網頁',
                                uri='http://www.e-happy.com.tw'
                            ),
                            PostbackTemplateAction(
                                label='喜歡',
                                data='action=sell&item=喜歡唷'
                            ),
                            PostbackTemplateAction(
                                label='不太喜歡',
                                data='action=sell&item=不太喜歡耶'
                            ),
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/4QfKuz1.png',
                        title='這是樣板2',
                        text='第2個轉盤樣板',
                        actions=[
                            URITemplateAction(
                                label='連結文淵閣網頁',
                                uri='http://www.e-happy.com.tw'
                            ),
                            PostbackTemplateAction(
                                label='喜歡',
                                data='action=sell&item=喜歡唷'
                            ),
                            PostbackTemplateAction(
                                label='不太喜歡',
                                data='action=sell&item=不太喜歡耶'
                            ),
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/4QfKuz1.png',
                        title='這是樣板3',
                        text='第3個轉盤樣板',
                        actions=[
                            URITemplateAction(
                                label='連結文淵閣網頁',
                                uri='http://www.e-happy.com.tw'
                            ),
                            PostbackTemplateAction(
                                label='喜歡',
                                data='action=sell&item=喜歡唷'
                            ),
                            PostbackTemplateAction(
                                label='不太喜歡',
                                data='action=sell&item=不太喜歡耶'
                            ),
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/4QfKuz1.png',
                        title='這是樣板4',
                        text='第4個轉盤樣板',
                        actions=[
                            URITemplateAction(
                                label='連結文淵閣網頁',
                                uri='http://www.e-happy.com.tw'
                            ),
                            PostbackTemplateAction(
                                label='喜歡',
                                data='action=sell&item=喜歡唷'
                            ),
                            PostbackTemplateAction(
                                label='不太喜歡',
                                data='action=sell&item=不太喜歡耶'
                            ),
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/4QfKuz1.png',
                        title='這是樣板5',
                        text='第5個轉盤樣板',
                        actions=[
                            URITemplateAction(
                                label='連結文淵閣網頁',
                                uri='http://www.e-happy.com.tw'
                            ),
                            PostbackTemplateAction(
                                label='喜歡',
                                data='action=sell&item=喜歡唷'
                            ),
                            PostbackTemplateAction(
                                label='不太喜歡',
                                data='action=sell&item=不太喜歡耶'
                            ),
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/4QfKuz1.png',
                        title='這是樣板6',
                        text='第6個轉盤樣板',
                        actions=[
                            URITemplateAction(
                                label='連結文淵閣網頁',
                                uri='http://www.e-happy.com.tw'
                            ),
                            PostbackTemplateAction(
                                label='喜歡',
                                data='action=sell&item=喜歡唷'
                            ),
                            PostbackTemplateAction(
                                label='不太喜歡',
                                data='action=sell&item=不太喜歡耶'
                            ),
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/4QfKuz1.png',
                        title='這是樣板7',
                        text='第7個轉盤樣板',
                        actions=[
                            URITemplateAction(
                                label='連結文淵閣網頁',
                                uri='http://www.e-happy.com.tw'
                            ),
                            PostbackTemplateAction(
                                label='喜歡',
                                data='action=sell&item=喜歡唷'
                            ),
                            PostbackTemplateAction(
                                label='不太喜歡',
                                data='action=sell&item=不太喜歡耶'
                            ),
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/4QfKuz1.png',
                        title='這是樣板8',
                        text='第8個轉盤樣板',
                        actions=[
                            URITemplateAction(
                                label='連結文淵閣網頁',
                                uri='http://www.e-happy.com.tw'
                            ),
                            PostbackTemplateAction(
                                label='喜歡',
                                data='action=sell&item=喜歡唷'
                            ),
                            PostbackTemplateAction(
                                label='不太喜歡',
                                data='action=sell&item=不太喜歡耶'
                            ),
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/4QfKuz1.png',
                        title='這是樣板9',
                        text='第9個轉盤樣板',
                        actions=[
                            URITemplateAction(
                                label='連結文淵閣網頁',
                                uri='http://www.e-happy.com.tw'
                            ),
                            PostbackTemplateAction(
                                label='喜歡',
                                data='action=sell&item=喜歡唷'
                            ),
                            PostbackTemplateAction(
                                label='不太喜歡',
                                data='action=sell&item=不太喜歡耶'
                            ),
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/4QfKuz1.png',
                        title='這是樣板10',
                        text='第10個轉盤樣板',
                        actions=[
                            URITemplateAction(
                                label='連結文淵閣網頁',
                                uri='http://www.e-happy.com.tw'
                            ),
                            PostbackTemplateAction(
                                label='喜歡',
                                data='action=sell&item=喜歡唷'
                            ),
                            PostbackTemplateAction(
                                label='不太喜歡',
                                data='action=sell&item=不太喜歡耶'
                            ),
                        ]
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))

def sendPizza(event):
    try:
        message = TextSendMessage(
            text = '您好，我們將盡快為您推薦今日熱門食譜。'
        )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))

def sendYes(event):
    try:
        message = TextSendMessage(
            text='感謝您的購買，\n我們將盡快寄出商品。',
        )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))

def sendNo(event):
    try:
        message = TextSendMessage(
            text='您確定嗎?，\n傷心嗚嗚...',
        )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))

def sendBack_buy(event, backdata):  #處理Postback
    try:
        text1 = '感謝您耐心等候，我們將盡快為您搜尋。\n(action 的值為 ' + backdata.get('action') + ')'
        text1 += '\n(可將處理程式寫在此處。)'
        message = TextSendMessage(  #傳送文字
            text = text1
        )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))

def sendBack_sell(event, backdata):  #處理Postback
    try:
        message = TextSendMessage(  #傳送文字
            text = '您的選擇是 ' + backdata.get('item')
        )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))

#4
def sendQuickreply(event):  #快速選單
    try:
        message = TextSendMessage(
            text='請選擇今日推薦套餐',
            quick_reply=QuickReply(
                items=[
                    QuickReplyButton(
                        action=MessageAction(label="牛肉套餐", text="牛牛牛")
                    ),
                    QuickReplyButton(
                        action=MessageAction(label="喜洋洋套餐", text="羊羊羊")
                    ),
                    QuickReplyButton(
                        action=MessageAction(label="肥豬肥套餐", text="豬豬豬")
                    ),
                    QuickReplyButton(
                        action=MessageAction(label="紙包雞雞包紙套餐", text="GGG")
                    ),
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
