# Line Fitness

## 前言
現在健身的人愈來愈多，大家也愈來愈注重飲食健康，再加上作者本身也有健身的習慣，因此想設計一個LineChatBot來幫助有健身習慣的人，藉由它可以更清楚每天應該怎麼吃、吃多少來讓健身的效果更好。

## 構想
先藉由使用者輸入的性別、年齡、身高、體重、運動習慣等，幫助使用者算出BMR與TDEE。再藉由增肌、減脂兩個面向來幫助所需要的人，其中增肌有提供訓練各部位的推薦影片;減脂則是有現在主流的低醣飲食與生酮飲食來提供給大家參考。增肌、減脂都能查詢當天三大營養素應該各吃多少，也可以藉由衛生署提供的各食物營養素分析來給使用者查詢。

## 環境
- ubuntu 18.04
- python 3.6.9

## 技術
- Olami
    - 具有NLP的聊天機器人
- Beautifulsoup4
    - 爬取youtube各健身部位的推薦影片

## 使用教學
1. install `pipenv`
```shell
pip3 install pipenv
```
2. install 所需套件
```shell
pipenv install --three
// 若遇到pygraphviz安裝失敗，則嘗試下面這行
sudo apt-get install graphviz graphviz-dev
```
3. 從`.env.sample`產生出一個`.env`，並填入以下四個資訊

- Line
    - LINE_CHANNEL_SECRET
    - LINE_CHANNEL_ACCESS_TOKEN
- Olami
    - APP_KEY
    - APP_SECRET
4. install `ngrok`

```shell
sudo snap install ngrok
```
5. run `ngrok` to deploy Line Chat Bot locally
```shell
ngrok http 8000
```
6. execute app.py
```shell
python3 app.py
```

## 使用說明
- 基本操作
    - 所有用到英文的指令大小寫皆可
    - 隨時輸入任何字若沒觸發到都會有提示
    - 以下三個指令皆可隨時輸入
        - `restart`
            - reset所有資訊
        - `chat`
            - 切換到聊天機器人模式
        - `fsm`
            - 傳回當前的fsm圖片
- 架構圖
    1. 輸入`fitness`開始使用健身小幫手
    2. 輸入性別 -> `男生`或`女生`
    3. 輸入年齡 -> `整數`
    4. 輸入身高 -> `整數`
    5. 輸入體重 -> `整數`
    6. 輸入一週運動的天數 -> `整數`
    7. 以下分成`增肌`與`減脂`來加以說明
- `增肌` 
    - `熱量`
        - 算出BMR與TDEE
        - `食物`
            - 可查看一天三大營養素需要吃多少
            - 可回傳三大營養素所佔熱量比例的圓餅圖
            - 可搜尋食物名稱來知道該食物的三大營養素
        - `BMR`
            - 文字說明何謂BMR
        - `TDEE`
            - 文字說明何謂TDEE
    - `影片`
        - 會推薦youtube上的健身影片
        - 可根據想練的部位來加以訓練
            - 胸
            - 背
            - 腿
            - 肩 (未顯示在Button上）
            - 二頭 (未顯示在Button上）
            - 三頭 (未顯示在Button上）
- `減脂`
    - `低醣飲食`
        - `熱量`
            - 算出BMR與TDEE
            - `食物`
                - 可查看一天三大營養素需要吃多少
                - 可回傳三大營養素所佔熱量比例的圓餅圖
                - 可搜尋食物名稱來知道該食物的三大營養素
            - `BMR`
                - 文字說明何謂BMR
            - `TDEE`
                - 文字說明何謂TDEE
    - `生酮飲食`
        - `熱量`
            - 算出BMR與TDEE
            - `食物`
                - 可查看一天三大營養素需要吃多少
                - 可回傳三大營養素所佔熱量比例的圓餅圖
                - 可搜尋食物名稱來知道該食物的三大營養素
            - `BMR`
                - 文字說明何謂BMR
            - `TDEE`
                - 文字說明何謂TDEE

## 使用示範
### 輸入個人資訊
![](https://i.imgur.com/RAXRooY.jpg)
![](https://i.imgur.com/3VkDy82.jpg)
![](https://i.imgur.com/JhK01qT.jpg)
![](https://i.imgur.com/OCsoSBk.jpg)
### 增肌
![](https://i.imgur.com/OodsURE.jpg)
![](https://i.imgur.com/95lZAGO.jpg)
![](https://i.imgur.com/DOj8yEs.jpg)
![](https://i.imgur.com/bgeHzOf.jpg)
![](https://i.imgur.com/R2vy5FN.jpg)
![](https://i.imgur.com/TfHJx3t.jpg)
![](https://i.imgur.com/6ZEIZzI.jpg)
![](https://i.imgur.com/2iNuLe8.jpg)
### 減脂(生酮飲食)
![](https://i.imgur.com/Aej3bXd.jpg)
![](https://i.imgur.com/shzYGJD.jpg)
![](https://i.imgur.com/nxUfsPP.jpg)
![](https://i.imgur.com/pvibAF1.jpg)
![](https://i.imgur.com/xqbqg5A.jpg)
![](https://i.imgur.com/hsoAJeE.jpg)
![](https://i.imgur.com/7KyAzOK.jpg)
### 隨時畫FSM
![](https://i.imgur.com/kk8b9aa.jpg)
### 聊天機器人
![](https://i.imgur.com/co5NtdJ.jpg)
![](https://i.imgur.com/v0uG700.jpg)


## FSM
![](https://i.imgur.com/GMrkfDT.png)
### state說明
- user: 輸入fitness開始使用健身小幫手
- input_gender: 輸入男生或女生
- input_age: 輸入年齡(整數)
- input_height: 輸入身高(整數)
- input_weight: 輸入體重(整數)
- input_days: 輸入一周運動天數(整數)
- choose: 顯示個人資訊，並選擇要增肌還是減脂
- muscle: 選擇要看增肌所需的熱量或是進入搜尋健身影片模式
- show_video: 輸入想訓練的部位
- get_video: 秀出youtube推薦的健身影片
- thin: 選擇要低醣飲食還是生酮飲食
- thin_type1: 說明何謂低醣飲食
- thin_type2: 說明何謂生酮飲食
- show_cal: 顯示使用者的BMR與TDEE
- show_food: 根據使用者要增肌或低醣飲食或生酮飲食，顯示使用者一天三大營養素應該各吃多少
- show_img: 根據使用者要增肌或低醣飲食或生酮飲食，回傳三大營養素比例的圓餅圖
- query: 作者事先整理過衛生署公布的各食物營養素，使用者可輸入他想要查詢的食物，會回傳所有相關該關鍵字的食物三大營養素提供給作者參考

## Deploy in Heroku
Setting to deploy webhooks on Heroku.

### Heroku CLI installation

* [macOS, Windows](https://devcenter.heroku.com/articles/heroku-cli)

or you can use Homebrew (MAC)
```sh
brew tap heroku/brew && brew install heroku
```

or you can use Snap (Ubuntu 16+)
```sh
sudo snap install --classic heroku
```

### Connect to Heroku

1. Register Heroku: https://signup.heroku.com

2. Create Heroku project from website

3. CLI Login

	`heroku login`

### Upload project to Heroku

1. Add local project to Heroku project

	heroku git:remote -a {HEROKU_APP_NAME}

2. Upload project

	```
	git add .
	git commit -m "Add code"
	git push -f heroku master
	```

3. Set Environment - Line Messaging API Secret Keys

	```
	heroku config:set LINE_CHANNEL_SECRET=your_line_channel_secret
	heroku config:set LINE_CHANNEL_ACCESS_TOKEN=your_line_channel_access_token
    heroku config:set APP_KEY=your_olami_APP_KEY
    heroku config:set APP_SECRET=your_olami_APP_SECRET
	```

4. Your Project is now running on Heroku!

	url: `{HEROKU_APP_NAME}.herokuapp.com/callback`

	debug command: `heroku logs --tail --app {HEROKU_APP_NAME}`

5. If fail with `pygraphviz` install errors

	run commands below can solve the problems
	```
	heroku buildpacks:set heroku/python
	heroku buildpacks:add --index 1 heroku-community/apt
	```

