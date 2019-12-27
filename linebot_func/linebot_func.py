from django.conf import settings

from linebot import LineBotApi
import linebot.models as linebot_models

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)


# 傳送文字
def sendText(event):
    try:
        message = linebot_models.TextSendMessage(text="是在哈瞜嗎? 小瓜呆~\n嘿嘿！")
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(
            event.reply_token, linebot_models.TextSendMessage(text="發生錯誤！")
        )


# 傳送圖片
def sendImage(event):
    try:
        message = linebot_models.ImageSendMessage(
            original_content_url="https://i.imgur.com/yXPDy5Z.jpg",
            preview_image_url="https://i.imgur.com/yXPDy5Z.jpg",
        )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(
            event.reply_token, linebot_models.TextSendMessage(text="發生錯誤！")
        )


# 按鈕樣版
def sendButton(event):
    try:
        message = linebot_models.TemplateSendMessage(
            alt_text="按鈕樣板",
            template=ButtonsTemplate(
                thumbnail_image_url="https://i.imgur.com/4QfKuz1.png",  # 顯示的圖片
                title="按鈕樣版示範",  # 主標題
                text="請選擇：",  # 副標題
                actions=[
                    linebot_models.MessageTemplateAction(
                        label="文字訊息", text="@購買披薩"
                    ),  # 顯示文字計息
                    linebot_models.URITemplateAction(  # 開啟網頁
                        label="連結網頁", uri="http://www.e-happy.com.tw"
                    ),
                    linebot_models.PostbackTemplateAction(  # 執行Postback功能,觸發Postback事件
                        label="回傳訊息",  # 按鈕文字
                        # text='@購買披薩',  #顯示文字計息
                        data="action=buy",  # Postback資料
                    ),
                ],
            ),
        )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(
            event.reply_token, linebot_models.TextSendMessage(text="發生錯誤！")
        )


# 確認樣板
def sendConfirm(event):
    try:
        message = linebot_models.TemplateSendMessage(
            alt_text="確認樣板",
            template=linebot_models.ConfirmTemplate(
                text="你確定要購買這項商品嗎？",
                actions=[
                    linebot_models.MessageTemplateAction(
                        label="是", text="@yes"
                    ),  # 按鈕選項
                    linebot_models.MessageTemplateAction(label="否", text="@no"),
                ],
            ),
        )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(
            event.reply_token, linebot_models.TextSendMessage(text="發生錯誤！")
        )


# 轉盤樣板
def sendCarousel(event):
    try:
        message = linebot_models.TemplateSendMessage(
            alt_text="轉盤樣板",
            template=linebot_models.CarouselTemplate(
                columns=[
                    linebot_models.CarouselColumn(
                        thumbnail_image_url="https://i.imgur.com/4QfKuz1.png",
                        title="這是樣板一",
                        text="第一個轉盤樣板",
                        actions=[
                            linebot_models.MessageTemplateAction(
                                label="文字訊息一", text="賣披薩"
                            ),
                            linebot_models.URITemplateAction(
                                label="連結文淵閣網頁", uri="http://www.e-happy.com.tw"
                            ),
                            linebot_models.PostbackTemplateAction(
                                label="回傳訊息一", data="action=sell&item=披薩"
                            ),
                        ],
                    ),
                    linebot_models.CarouselColumn(
                        thumbnail_image_url="https://i.imgur.com/qaAdBkR.png",
                        title="這是樣板二",
                        text="第二個轉盤樣板",
                        actions=[
                            linebot_models.MessageTemplateAction(
                                label="文字訊息二", text="賣飲料"
                            ),
                            linebot_models.URITemplateAction(
                                label="連結台大網頁", uri="http://www.ntu.edu.tw"
                            ),
                            linebot_models.PostbackTemplateAction(
                                label="回傳訊息二", data="action=sell&item=飲料"
                            ),
                        ],
                    ),
                ]
            ),
        )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(
            event.reply_token, linebot_models.TextSendMessage(text="發生錯誤！")
        )


# 快速選單
def sendQuickreply(event):
    try:
        message = linebot_models.TextSendMessage(
            text="請選擇今日推薦套餐",
            quick_reply=QuickReply(
                items=[
                    linebot_models.QuickReplyButton(
                        action=linebot_models.MessageAction(label="牛肉套餐", text="牛肉套餐")
                    ),
                    linebot_models.QuickReplyButton(
                        action=linebot_models.MessageAction(label="喜洋洋套餐", text="喜洋洋套餐")
                    ),
                    linebot_models.QuickReplyButton(
                        action=linebot_models.MessageAction(label="肥豬肥套餐", text="肥豬肥套餐")
                    ),
                    linebot_models.QuickReplyButton(
                        action=linebot_models.MessageAction(
                            label="紙包雞雞包紙套餐", text="紙包雞雞包紙套餐"
                        )
                    ),
                ]
            ),
        )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(
            event.reply_token, linebot_models.TextSendMessage(text="發生錯誤！")
        )
