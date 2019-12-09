from transitions.extensions import GraphMachine
from utils import send_text_message, send_carousel_message, send_button_message, send_image_message
from bs4 import BeautifulSoup
import requests
from linebot.models import ImageCarouselColumn, URITemplateAction, MessageTemplateAction
import pandas as pd

# global variable
age = 0
gender = ''
height = 0
weight = 0
days = 0
BMR = 0
TDEE = 0
part = ''
diet_type = -1
df = pd.read_csv('food.csv')

class TocMachine(GraphMachine):

    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)

    # user start
    def is_going_to_input_gender(self, event):
        text = event.message.text
        return text.lower() == 'fitness'

    def on_enter_input_gender(self, event):
        title = '請先提供您的基本資訊'
        text = '您是『男生』還是『女生』'
        btn = [
            MessageTemplateAction(
                label = '男生',
                text ='男生'
            ),
            MessageTemplateAction(
                label = '女生',
                text = '女生'
            ),
        ]
        url = 'https://i.imgur.com/T2bLdbN.jpg'
        send_button_message(event.reply_token, title, text, btn, url)

    def is_going_to_input_age(self, event):
        global gender
        text = event.message.text

        if text == '男生':
            gender = '男生'
            return True
        elif text == '女生':
            gender = '女生'
            return True
        return False

    def on_enter_input_age(self, event):
        send_text_message(event.reply_token, '請輸入您的年齡(整數)')

    def is_going_to_input_height(self, event):
        global age
        text = event.message.text

        if text.lower().isnumeric():
            age = int(text)
            return True
        return False

    def on_enter_input_height(self, event):
        send_text_message(event.reply_token, '請輸入您的身高(整數)')

    def is_going_to_input_weight(self, event):
        global height
        text = event.message.text

        if text.lower().isnumeric():
            height = int(text)
            return True
        return False

    def on_enter_input_weight(self, event):
        send_text_message(event.reply_token, '請輸入您的體重(整數)')

    def is_going_to_input_days(self, event):
        global weight
        text = event.message.text

        if text.lower().isnumeric():
            weight = int(text)
            return True
        return False

    def on_enter_input_days(self, event):
        send_text_message(event.reply_token, '請輸入您一週運動的天數(0~7的整數)')

    def is_going_to_choose(self, event):
        global days, diet_type
        text = event.message.text

        if text.lower().isnumeric():
            days = int(text)
            if days >=0 and days <=7:
                return True

        if text.lower() == 'back' and diet_type != -1:
            return True

        return False

    # state of choose
    def on_enter_choose(self, event):
        global age, gender, height, weight, days
        title = '您的目標是『增肌』還是『減脂』'
        text = '年齡: ' + str(age) + '歲，性別: ' + gender + '，\n身高: ' + str(height) + '公分，體重: ' + str(weight) + '公斤，\n一週運動' + str(days) + '天'
        btn = [
            MessageTemplateAction(
                label = '增肌',
                text ='增肌'
            ),
            MessageTemplateAction(
                label = '減脂',
                text = '減脂'
            ),
        ]
        url = 'https://i.imgur.com/3i4SoVG.jpg'
        send_button_message(event.reply_token, title, text, btn, url)

    def is_going_to_muscle(self, event):
        global diet_type
        text = event.message.text
        if (text == '增肌') or ((self.state == 'show_cal' or self.state == 'show_food' or self.state == 'show_video' or self.state == 'get_video') and (text.lower() == 'back') and diet_type == 0):
            return True
        return False

    # state of muscle
    def on_enter_muscle(self, event):
        global diet_type
        diet_type = 0
        title = '增肌選單'
        text = '輸入『熱量』可以查看您一天所需的熱量。\n輸入『影片』可以觀看健身影片。'
        btn = [
            MessageTemplateAction(
                label = '熱量',
                text ='熱量'
            ),
            MessageTemplateAction(
                label = '影片',
                text = '影片'
            ),
            MessageTemplateAction(
                label = 'back',
                text = 'back'
            ),
        ]
        url = 'https://i.imgur.com/JAtmCJ9.jpg'
        send_button_message(event.reply_token, title, text, btn, url)

    def is_going_to_show_cal(self, event):
        text = event.message.text
        if text == '熱量':
            return True
        return False

    def on_enter_show_cal(self, event):
        global age, gender, height, weight, days, BMR, TDEE, diet_type
        if gender == '男生':
            BMR = 13.7*weight + 5.0*height - 6.8*age + 66
        else:
            BMR = 9.6*weight + 1.8*height - 4.7*age + 655

        if days == 0:
            TDEE = BMR*1.2
        elif days >= 1 and days <= 2:
            TDEE = BMR*1.375
        elif days >= 3 and days <= 5:
            TDEE = BMR*1.55
        else:
            TDEE = BMR*1.725

        choose_str = '增肌'
        if diet_type != 0:
            choose_str = '減脂'

        title = 'BMR: ' + '{:.1f}'.format(BMR) + '大卡\nTDEE: ' + '{:.1f}'.format(TDEE) + '大卡'
        text = '輸入『食物』可查看一天的熱量應如何攝取\n輸入『BMR』或『TDEE』有說明'
        btn = [
            MessageTemplateAction(
                label = '食物',
                text ='食物'
            ),
            MessageTemplateAction(
                label = 'BMR',
                text = 'BMR'
            ),
            MessageTemplateAction(
                label = 'TDEE',
                text ='TDEE'
            ),
            MessageTemplateAction(
                label = 'back',
                text = 'back'
            ),
        ]
        url = 'https://i.imgur.com/dn88Kbx.gif'
        send_button_message(event.reply_token, title, text, btn, url)

    def is_going_to_show_food(self, event):
        text = event.message.text
        if text == '食物' or ((self.state == 'query' or self.state == 'show_img') and text.lower() == 'back'):
            return True
        return False

    def on_enter_show_food(self, event):
        global TDEE, diet_type
        carbo = 0
        protein = 0
        fat = 0
        diet_str1 = '減脂'
        diet_str2 = '少'
        t1 = ''
        t2 = ''
        t3 = ''
        if diet_type == 0:
            carbo = TDEE*0.5/4
            protein = TDEE*0.3/4
            fat = TDEE*0.2/9
            diet_str1 = '增肌'
            diet_str2 = '多'
            t1 = '(50%)'
            t2 = '(30%)'
            t3 = '(20%)'
        elif diet_type == 1:
            carbo = TDEE*0.2/4
            protein = TDEE*0.3/4
            fat = TDEE*0.5/9
            t1 = '(20%)'
            t2 = '(30%)'
            t3 = '(50%)'
        else:
            carbo = TDEE*0.1/4
            protein = TDEE*0.2/4
            fat = TDEE*0.7/9
            t1 = '(10%)'
            t2 = '(20%)'
            t3 = '(70%)'

        title = '想要' + diet_str1 + '的話，每天可以' + diet_str2 + '吃大約300~500大卡的熱量'
        text = '碳水化合物: ' + str(int(carbo)) + '克'+ t1 + '\n蛋白質: ' + str(int(protein)) + '克' + t2 + '\n脂肪: ' + str(int(fat)) + '克' + t3
        btn = [
            MessageTemplateAction(
                label = '圖片',
                text = '圖片'
            ),
            MessageTemplateAction(
                label = '查詢',
                text = '查詢'
            ),
            MessageTemplateAction(
                label = 'back',
                text = 'back'
            ),
        ]
        url = 'https://i.imgur.com/ncGVuDv.jpg'
        send_button_message(event.reply_token, title, text, btn, url)

    def is_going_to_show_img(self, event):
        text = event.message.text
        if text == '圖片':
            return True
        return False

    def on_enter_show_img(self, event):
        url = ''
        if diet_type == 0:
            url = 'https://i.imgur.com/qwFvFt0.png'
        elif diet_type == 1:
            url = 'https://i.imgur.com/PhkKYBi.png'
        else:
            url = 'https://i.imgur.com/v01jDp9.png'

        send_image_message(event.reply_token, url)

    def is_going_to_show_video(self, event):
        text = event.message.text
        if text == '影片':
            return True
        return False

    def on_enter_show_video(self, event):
        title = '您想要訓練哪個部位'
        text = '輸入你想要訓練的部位名稱'
        btn = [
            MessageTemplateAction(
                label = '胸',
                text ='胸'
            ),
            MessageTemplateAction(
                label = '背',
                text = '背'
            ),
            MessageTemplateAction(
                label = '腿',
                text ='腿'
            ),
            MessageTemplateAction(
                label = 'back',
                text = 'back'
            ),
        ]
        url = 'https://i.imgur.com/JzBU2kv.jpg'
        send_button_message(event.reply_token, title, text, btn, url)

    def is_going_to_get_video(self, event):
        global part
        text = event.message.text
        if text == '胸' or text == '背' or text == '腿' or text == '肩' or text == '二頭' or text == '三頭':
            part = text
            return True
        return False

    def on_enter_get_video(self, event):
        global part
        url = 'https://www.youtube.com/results?search_query=' + '健身+' + part
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html.parser')

        url_list = []
        img_list = []
        for i in range(5):
            url_list.append('https://www.youtube.com' + soup.select('.yt-lockup-video')[i].select("a[rel='spf-prefetch']")[0].get("href"))
            img_list.append(soup.select('.yt-lockup-video')[i].select('img')[0].get('src'))

        col = []
        for i in range(5):
            c = ImageCarouselColumn(
                image_url = img_list[i],
                action = URITemplateAction(
                    label = '點我觀看影片',
                    uri = url_list[i]
                )
            )
            col.append(c)

        send_carousel_message(event.reply_token, col)

    def is_going_to_thin(self, event):
        global diet_type
        text = event.message.text
        if (text == '減脂') or ((self.state == 'show_cal' or self.state == 'show_food' or self.state == 'thin_type1' or self.state == 'thin_type2') and (text.lower() == 'back') and diet_type != 0):
            return True
        return False

    # state of thin
    def on_enter_thin(self, event):
        global diet_type
        diet_type = 0
        title = '減脂選單'
        text = '您想要嘗試哪種減脂方式'
        btn = [
            MessageTemplateAction(
                label = '低醣飲食',
                text = '低醣飲食'
            ),
            MessageTemplateAction(
                label = '生酮飲食',
                text = '生酮飲食'
            ),
            MessageTemplateAction(
                label = 'back',
                text = 'back'
            ),
        ]
        url = 'https://i.imgur.com/vRm16Gk.jpg'
        send_button_message(event.reply_token, title, text, btn, url)

    def is_going_to_thin_type1(self, event):
        text = event.message.text
        if text == '低醣飲食':
            return True
        return False

    def on_enter_thin_type1(self, event):
        global diet_type
        diet_type = 1
        title = '低醣飲食的原理，就是藉由降低體內葡萄糖和肝醣的含量，來強迫身體去燃燒脂肪'
        text = '輸入『熱量』可以查看您一天所需的熱量'
        btn = [
            MessageTemplateAction(
                label = '熱量',
                text = '熱量'
            ),
            MessageTemplateAction(
                label = 'back',
                text = 'back'
            ),
        ]
        url = 'https://i.imgur.com/75MKX2k.jpg'
        send_button_message(event.reply_token, title, text, btn, url)

    def is_going_to_thin_type2(self, event):
        text = event.message.text
        if text == '生酮飲食':
            return True
        return False

    def on_enter_thin_type2(self, event):
        global diet_type
        diet_type = 2
        title = '生酮飲食是一種高脂肪低碳水的飲食，強迫人體燃燒脂肪而非碳水，模擬飢餓狀態'
        text = '輸入『熱量』可以查看您一天所需的熱量'
        btn = [
            MessageTemplateAction(
                label = '熱量',
                text = '熱量'
            ),
            MessageTemplateAction(
                label = 'back',
                text = 'back'
            ),
        ]
        url = 'https://i.imgur.com/3zdtFhV.jpg'
        send_button_message(event.reply_token, title, text, btn, url)

    def is_going_to_query(self, event):
        text = event.message.text
        if text == '查詢' or self.state == 'query':
            return True
        return False

    def on_enter_query(self, event):
        text = event.message.text
        if text == '查詢':
            send_text_message(event.reply_token, '請輸入你想查詢的食物')
            return
        df2 = df[df['樣品名稱'].str.contains(event.message.text)]
        if len(df2) == 0:
            text = '找不到任何有關這名稱的食物，請再輸入一次，或者輸入『back』返回'
            send_text_message(event.reply_token, text)
        else:
            text = '以下為每100克中的含量:\n\n'
            for index, row in df2.iterrows():
                if index%3 == 0:
                    text += row['樣品名稱'] + '\n'
                    text += '脂肪: ' + str(row['每100克含量']).strip() + 'g\n'
                elif index%3 == 1:
                    text += '蛋白質: ' + str(row['每100克含量']).strip() + 'g\n'
                else:
                    text += '碳水化合物: ' + str(row['每100克含量']).strip() + 'g\n\n'
            send_text_message(event.reply_token, text)

