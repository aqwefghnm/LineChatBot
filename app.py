import os
import sys

from flask import Flask, jsonify, request, abort, send_file
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

from fsm import TocMachine
from utils import send_text_message, send_carousel_message, send_button_message, send_image_message, send_text_message_AI


load_dotenv()


machine = TocMachine(
    states=[
        'input_age',
        'input_gender',
        'input_height',
        'input_weight',
        'input_days',
        'choose',
        'muscle',
        'thin',
        'show_cal',
        'show_food',
        'show_video',
        'get_video',
        'thin_type1',
        'thin_type2',
        'show_img',
        'query'
    ],
    transitions=[
        {'trigger': 'advance', 'source': 'user', 'dest': 'input_gender', 'conditions': 'is_going_to_input_gender'},
        {'trigger': 'advance', 'source': 'input_gender', 'dest': 'input_age', 'conditions': 'is_going_to_input_age'},
        {'trigger': 'advance', 'source': 'input_age', 'dest': 'input_height', 'conditions': 'is_going_to_input_height'},
        {'trigger': 'advance', 'source': 'input_height', 'dest': 'input_weight', 'conditions': 'is_going_to_input_weight'},
        {'trigger': 'advance', 'source': 'input_weight', 'dest': 'input_days', 'conditions': 'is_going_to_input_days'},
        {'trigger': 'advance', 'source': 'input_days', 'dest': 'choose', 'conditions': 'is_going_to_choose'},
        {'trigger': 'advance', 'source': 'choose', 'dest': 'muscle', 'conditions': 'is_going_to_muscle'},
        {'trigger': 'advance', 'source': 'choose', 'dest': 'thin', 'conditions': 'is_going_to_thin'},
        {'trigger': 'advance', 'source': 'muscle', 'dest': 'show_cal', 'conditions': 'is_going_to_show_cal'},
        {'trigger': 'advance', 'source': 'muscle', 'dest': 'show_video', 'conditions': 'is_going_to_show_video'},
        {'trigger': 'advance', 'source': 'show_cal', 'dest': 'show_food', 'conditions': 'is_going_to_show_food'},
        {'trigger': 'advance', 'source': 'show_food', 'dest': 'show_img', 'conditions': 'is_going_to_show_img'},
        {'trigger': 'advance', 'source': 'show_video', 'dest': 'get_video', 'conditions': 'is_going_to_get_video'},
        {'trigger': 'advance', 'source': 'show_cal', 'dest': 'muscle', 'conditions': 'is_going_to_muscle'},
        {'trigger': 'advance', 'source': 'show_food', 'dest': 'muscle', 'conditions': 'is_going_to_muscle'},
        {'trigger': 'advance', 'source': 'show_video', 'dest': 'muscle', 'conditions': 'is_going_to_muscle'},
        {'trigger': 'advance', 'source': 'get_video', 'dest': 'muscle', 'conditions': 'is_going_to_muscle'},
        {'trigger': 'advance', 'source': 'thin', 'dest': 'thin_type1', 'conditions': 'is_going_to_thin_type1'},
        {'trigger': 'advance', 'source': 'thin', 'dest': 'thin_type2', 'conditions': 'is_going_to_thin_type2'},
        {'trigger': 'advance', 'source': 'thin_type1', 'dest': 'show_cal', 'conditions': 'is_going_to_show_cal'},
        {'trigger': 'advance', 'source': 'thin_type2', 'dest': 'show_cal', 'conditions': 'is_going_to_show_cal'},
        {'trigger': 'advance', 'source': 'show_cal', 'dest': 'thin', 'conditions': 'is_going_to_thin'},
        {'trigger': 'advance', 'source': 'show_food', 'dest': 'thin', 'conditions': 'is_going_to_thin'},
        {'trigger': 'advance', 'source': 'thin_type1', 'dest': 'thin', 'conditions': 'is_going_to_thin'},
        {'trigger': 'advance', 'source': 'thin_type2', 'dest': 'thin', 'conditions': 'is_going_to_thin'},
        {'trigger': 'advance', 'source': 'muscle', 'dest': 'choose', 'conditions': 'is_going_to_choose'},
        {'trigger': 'advance', 'source': 'thin', 'dest': 'choose', 'conditions': 'is_going_to_choose'},
        {'trigger': 'advance', 'source': 'show_food', 'dest': 'query', 'conditions': 'is_going_to_query'},
        {'trigger': 'advance', 'source': 'query', 'dest': 'show_food', 'conditions': 'is_going_to_show_food'},
        {'trigger': 'advance', 'source': 'show_img', 'dest': 'show_food', 'conditions': 'is_going_to_show_food'},
        {'trigger': 'advance', 'source': 'query', 'dest': 'query', 'conditions': 'is_going_to_query'},
        {
            'trigger': 'go_back',
            'source': [
                'input_age',
                'input_gender',
                'input_height',
                'input_weight',
                'input_days',
                'choose',
                'muscle',
                'thin',
                'show_cal',
                'show_food',
                'show_video',
                'get_video',
                'thin_type1',
                'thin_type2',
                'show_img',
                'query'
            ],
            'dest': 'user'
        },
    ],
    initial='user',
    auto_transitions=False,
    show_conditions=True,
)

app = Flask(__name__, static_url_path='')


# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)
if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)

mode = 0

@app.route('/callback', methods=['POST'])
def webhook_handler():
    global mode
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info(f'Request body: {body}')

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue
        if not isinstance(event.message.text, str):
            continue
        print(f'\nFSM STATE: {machine.state}')
        print(f'REQUEST BODY: \n{body}')

        if mode == 1:
            if event.message.text.lower() == 'fitness':
                mode = 0
                send_text_message(event.reply_token, '返回健身小幫手')
                continue
            else:
                send_text_message_AI(event.reply_token, event.message.text)
                continue
        else:
            if event.message.text.lower() == 'chat':
                mode = 1
                send_text_message(event.reply_token, '進入聊天模式，隨時輸入『fitness』可返回健身小幫手')
                continue
            else:
                response = machine.advance(event)

        if response == False:
            if event.message.text.lower() == 'fsm':
                send_image_message(event.reply_token, 'https://f74062044.herokuapp.com/show-fsm')
            elif machine.state != 'user' and event.message.text.lower() == 'restart':
                send_text_message(event.reply_token, '輸入『fitness』即可開始使用健身小幫手。\n隨時輸入『chat』可以跟機器人聊天。\n隨時輸入『restart』可以從頭開始。\n隨時輸入『fsm』可以得到當下的狀態圖。')
                machine.go_back()
            elif machine.state == 'user':
                send_text_message(event.reply_token, '輸入『fitness』即可開始使用健身小幫手。\n隨時輸入『chat』可以跟機器人聊天。\n隨時輸入『restart』可以從頭開始。\n隨時輸入『fsm』可以得到當下的狀態圖。')
            elif machine.state == 'input_age' or machine.state == 'input_height' or machine.state == 'input_weight':
                send_text_message(event.reply_token, '請輸入一個整數')
            elif machine.state == 'input_gender':
                send_text_message(event.reply_token, '請輸入『男生』或『女生』')
            elif machine.state == 'input_days':
                send_text_message(event.reply_token, '請輸入一個『0~7的整數』')
            elif machine.state == 'choose':
                send_text_message(event.reply_token, '請輸入『增肌』或『減脂』')
            elif machine.state == 'muscle':
                send_text_message(event.reply_token, '輸入『熱量』可以查看您一天所需的熱量。\n輸入『影片』可以觀看健身影片。\n輸入『back』可重新選擇目標。')
            elif machine.state == 'thin':
                send_text_message(event.reply_token, '輸入『低醣飲食』可以查看何謂低醣飲食。\n輸入『生酮飲食』可以查看何謂生酮飲食。\n輸入『back』可重新選擇目標。')
            elif machine.state == 'show_cal':
                if event.message.text.lower() == 'bmr':
                    text = '即基礎代謝率，全名為 Basal Metabolic Rate。基礎代謝意思是身體為了要維持運作，在休息時消耗掉的熱量。基礎代謝率佔了總熱量消耗的一大部分。會影響到基礎代謝率高低的有很多，像是總體重、肌肉量、賀爾蒙、年齡等。'
                    send_text_message(event.reply_token, text)
                elif event.message.text.lower() == 'tdee':
                    text = '即每日總消耗熱量，全名為 Total Daily Energy Expenditure。指的是人體在一天內消耗的熱量，除了基礎代謝率所需的能量以外，還包括運動和其他活動消耗的熱量，像是走路、上下樓梯、活動肌肉等等。通常運動量愈大，TDEE也會愈高。'
                    send_text_message(event.reply_token, text)
                elif event.message.text.lower() != 'back':
                    send_text_message(event.reply_token, '輸入『食物』可以查看一天的熱量應如何攝取。\n輸入『BMR』或『TDEE』會有文字說明。\n輸入『back』返回選單。')
            elif machine.state == 'show_video' and event.message.text.lower() != 'back':
                send_text_message(event.reply_token, '輸入『胸』，『背』，『腿』，『肩』，『二頭』，『三頭』可搜尋相關影片。\n輸入『back』返回選單。')
            elif (machine.state == 'show_img' or machine.state == 'get_video') and (event.message.text.lower() != 'back'):
                send_text_message(event.reply_token, '輸入『back』返回選單。')
            elif machine.state == 'show_food' and event.message.text.lower() != 'back':
                send_text_message(event.reply_token, '輸入『圖片』可查看熱量圖。\n輸入『查詢』可查詢食物的營養素。\n輸入『back』返回選單。')
            elif (machine.state == 'thin_type1' or machine.state == 'thin_type2') and (event.message.text.lower() != 'back'):
                send_text_message(event.reply_token, '輸入『熱量』可以查看您一天所需的熱量。\n輸入『back』返回選單。')

    return 'OK'


@app.route('/show-fsm', methods=['GET'])
def show_fsm():
    machine.get_graph().draw('fsm.png', prog='dot', format='png')
    return send_file('fsm.png', mimetype='image/png')


if __name__ == '__main__':
    port = os.environ.get('PORT', 8000)
    app.run(host='0.0.0.0', port=port, debug=True)
