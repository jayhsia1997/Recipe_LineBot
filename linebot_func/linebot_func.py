from django.conf import settings

from linebot import LineBotApi
from linebot.models import (
    TextSendMessage,
    ImageSendMessage,
    TemplateSendMessage,
    QuickReplyButton,
    MessageAction,
    ButtonsTemplate,
    MessageTemplateAction,
    URITemplateAction,
    PostbackTemplateAction,
    ConfirmTemplate,
    CarouselTemplate,
    CarouselColumn,
    QuickReply,
    TextSendMessage,
    BubbleContainer,
    ImageComponent,
    BoxComponent,
    TextComponent,
    IconComponent,
    ButtonComponent,
    SeparatorComponent,
    FlexSendMessage,
    URIAction,
    ImageCarouselTemplate,
    ImageCarouselColumn,
)

import pymongo
import sys

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
client = pymongo.MongoClient(
    "mongodb://%s:%s@%s:%s/" % ("root", "root", "220.137.60.236", "27017")
)
db = client.test

# 查詢
def sendText(event):  # 傳送文字
    try:
        message = TextSendMessage(text="查詢請依以下格式查詢。\n食材1、食材2、食材3")
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="發生錯誤！"))


# 推薦
def sendFlex(event):  # 彈性配置
    try:
        size = 1
        mtext = event.message.text
        if mtext == '@熱門推薦':
            size = 5
        recipe_ingredients = []
        recipe_steps = []
        contents = []
        temp_recipe_data = db.clear_up_recipes.aggregate([{"$sample": {"size": size}}])
        for recipe_data in temp_recipe_data:
            for ingredients in recipe_data["ingredients"]:
                if ingredients["ingredient_name"] != None:
                    ingredient_name = ingredients["ingredient_name"]
                else:
                    ingredient_name = ""
                if ingredients["ingredient_quantity"] != None:
                    ingredient_quantity = ingredients["ingredient_quantity"]
                else:
                    ingredient_quantity = ""
                if ingredients["ingredient_unit"] != None:
                    ingredient_unit = ingredients["ingredient_unit"]
                else:
                    ingredient_unit = ""
                recipe_ingredients.append(
                    {
                        "contents": [
                            {
                                "color": "#aaaaaa",
                                "flex": 3,
                                "size": "sm",
                                "text": str(ingredient_name),
                                "type": "text",
                            },
                            {
                                "color": "#666666",
                                "flex": 1,
                                "size": "sm",
                                "text": str(ingredient_quantity + ingredient_unit),
                                "type": "text",
                            },
                        ],
                        "layout": "baseline",
                        "type": "box",
                    }
                )

            for cooking_steps in recipe_data["cooking_steps"]:
                steps = cooking_steps["steps"]
                methods = cooking_steps["methods"]
                recipe_steps.append(
                    {
                        "contents": [
                            {
                                "color": "#aaaaaa",
                                "flex": 1,
                                "size": "sm",
                                "text": "步驟" + str(steps) + "\n" + str(methods),
                                "type": "text",
                            }
                        ],
                        "layout": "baseline",
                        "type": "box",
                        "wrap": True,
                    }
                )

            contents.append(
                {
                    "direction": "ltr",
                    "type": "bubble",
                    "header": {
                        "contents": [
                            {
                                "size": "md",
                                "text": str(recipe_data["recipe_name"]),
                                "type": "text",
                                "weight": "bold",
                            }
                        ],
                        "layout": "vertical",
                        "type": "box",
                    },
                    "hero": {
                        "aspectMode": "cover",
                        "aspectRatio": "792:555",
                        "size": "full",
                        "type": "image",
                        "url": recipe_data["recipe_img_url"],
                    },
                    "body": {
                        "contents": [
                            {"size": "md", "text": "食材", "type": "text"},
                            {"color": "#0000FF", "type": "separator"},
                            {
                                "contents": recipe_ingredients,
                                "layout": "vertical",
                                "margin": "lg",
                                "type": "box",
                            },
                            {"size": "md", "text": "步驟", "type": "text"},
                            {"color": "#0000FF", "type": "separator"},
                            {
                                "contents": recipe_steps,
                                "layout": "vertical",
                                "margin": "lg",
                                "type": "box",
                                "wrap": True,
                            },
                        ],
                        "layout": "vertical",
                        "type": "box",
                        "wrap": True,
                    },
                }
            )
            recipe_ingredients = []
            recipe_steps = []

        bubble = {"type": "carousel", "contents": contents}
        message = FlexSendMessage(alt_text="彈性配置範例", contents=bubble)
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=""))

# 問卷
def sendCarousel(event):
    try:
        columns = []
        temp_recipe_data = db.clear_up_recipes.aggregate([{"$sample": {"size": 10}}])
        for recipe_data in temp_recipe_data:
            columns.append(
                {
                    "title": recipe_data["recipe_name"],
                    "text": "請選擇喜歡或不喜歡",
                    "thumbnailImageUrl": recipe_data['recipe_img_url'],
                    "actions": [
                        {
                            "data": "action=sell&item=喜歡\n%s" % recipe_data['recipe_name'],
                            "label": "喜歡",
                            "type": "postback",
                        },
                        {
                            "data": "action=sell&item=不喜歡\n%s" % recipe_data['recipe_name'],
                            "label": "不喜歡",
                            "type": "postback",
                        },
                    ],
                }
            )
        template = {"type": "carousel", "columns": columns}
        message = TemplateSendMessage(alt_text="轉盤樣板", template=template)
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="發生錯誤！"))
     

def sendBack_buy(event, backdata):  # 處理Postback
    try:
        text1 = "感謝您耐心等候，我們將盡快為您搜尋。\n(action 的值為 " + backdata.get("action") + ")"
        text1 += "\n(可將處理程式寫在此處。)"
        message = TextSendMessage(text=text1)  # 傳送文字
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="發生錯誤！"))


def sendBack_sell(event, backdata):  # 處理Postback
    try:
        message = TextSendMessage(text="您" + backdata.get("item"))  # 傳送文字
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="發生錯誤！"))


def manageForm(event, mtext):
    try:
        flist = mtext[3:].split("/")
        text1 = "姓名：" + flist[0] + "\n"
        text1 += "日期：" + flist[1] + "\n"
        text1 += "包廂：" + flist[2]
        message = TextSendMessage(text=text1)
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="發生錯誤！"))


# 3
def sendButton(event):  # 按鈕樣版
    try:
        message = TemplateSendMessage(
            alt_text="按鈕樣板",
            template=ButtonsTemplate(
                thumbnail_image_url="https://i.imgur.com/4QfKuz1.png",  # 顯示的圖片
                title="按鈕樣版示範",  # 主標題
                text="請選擇：",  # 副標題
                actions=[
                    MessageTemplateAction(label="熱門食譜推薦", text="@熱門食譜推薦"),  # 顯示文字計息
                    URITemplateAction(  # 開啟網頁
                        label="連結網頁", uri="http://www.e-happy.com.tw"
                    ),
                    PostbackTemplateAction(  # 執行Postback功能,觸發Postback事件
                        label="搜尋中請稍後",  # 按鈕文字
                        text="@搜尋中請稍後",  # 顯示文字訊息
                        data="action=buy",  # Postback資料
                    ),
                ],
            ),
        )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="發生錯誤！"))


# 5
def sendConfirm(event):  # 確認樣板
    try:
        message = TemplateSendMessage(
            alt_text="確認樣板",
            template=ConfirmTemplate(
                text="查詢請依以下格式\n食材1,食材2,食材3",
                actions=[
                    MessageTemplateAction(label="是", text="@yes"),  # 按鈕選項
                    MessageTemplateAction(label="否", text="@no"),
                ],
            ),
        )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="發生錯誤！"))




def sendPizza(event):
    try:
        message = TextSendMessage(text="您好，我們將盡快為您推薦今日熱門食譜。")
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="發生錯誤！"))


def sendYes(event):
    try:
        message = TextSendMessage(text="感謝您的購買，\n我們將盡快寄出商品。")
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="發生錯誤！"))


def sendNo(event):
    try:
        message = TextSendMessage(text="您確定嗎?，\n傷心嗚嗚...")
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="發生錯誤！"))


# 4
def sendQuickreply(event):  # 快速選單
    try:
        message = TextSendMessage(
            text="請選擇今日推薦套餐",
            quick_reply=QuickReply(
                items=[
                    QuickReplyButton(action=MessageAction(label="牛肉套餐", text="牛牛牛")),
                    QuickReplyButton(action=MessageAction(label="喜洋洋套餐", text="羊羊羊")),
                    QuickReplyButton(action=MessageAction(label="肥豬肥套餐", text="豬豬豬")),
                    QuickReplyButton(
                        action=MessageAction(label="紙包雞雞包紙套餐", text="GGG")
                    ),
                ]
            ),
        )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="發生錯誤！"))

