import requests
import json
import random
import time
from PIL import Image, ImageFont, ImageDraw

def exceptedProfit(coin, coinToMatch, serverBalance):
    response = json.loads(requests.get(f"https://api.hotbit.io/v2/p1/order.book?market={coin}/{coinToMatch}&side=1&offset=0&limit=1000").text)
    totalMarket = 0
    if response["error"] == None:
        for order in response["result"]["orders"]:
            totalMarket += float(order['price']) * float(order['amount'])

            if totalMarket >= serverBalance and totalMarket - serverBalance <= 30:
                return float((float(order['price']) / float(response['result']['orders'][0]['price']) - 1) * 100)
    return 0

def listOfAllCoins():
    coins = []
    marketStatus24h = json.loads(requests.get(f'https://api.hotbit.io/v2/p1/market.status24h').text)['result']
    for coin in marketStatus24h:
        if "USDT" in coin and coin != "GUSDTUSDT":
            coins.append(coin.replace("USDT", ""))

    return coins


def coin(coinToMatch, serverBalance, minVolume, maxVolume, minPercentage, maxPercentage):
    coins = []
    goodCoins = []

    marketStatus24h = json.loads(requests.get(f'https://api.hotbit.io/v2/p1/market.status24h').text)['result']
    for m in marketStatus24h:
        if coinToMatch in m:
            coins.append(m)

    random.shuffle(coins)

    for coin in coins:
        if coin != "GUSDTUSDT":
            if float(marketStatus24h[coin]['volume']) * float(marketStatus24h[coin]['last']) <= float(maxVolume) and float(marketStatus24h[coin]['volume']) * float(marketStatus24h[coin]['last']) >= float(minVolume):
                profit = exceptedProfit(coin.replace(coinToMatch, ''), coinToMatch, serverBalance)
                if profit != 0:
                    if profit >= minPercentage and profit <= maxPercentage:
                        goodCoins.append(coin.replace(coinToMatch, ''))
                        print(profit)
                time.sleep(0.25)

            if len(goodCoins) == int(numberOfCoinsYouWant):
                return goodCoins
    if len(goodCoins) == 0:
        return "No / not enough coins found"
    else:
        return goodCoins

def image(filename, coin, wrongCoin1, wrongCoin2):
    my_image = Image.open("Images/template.png")

    title_font = ImageFont.truetype('Font/Roboto-BlackItalic.ttf', 50)

    image_editable = ImageDraw.Draw(my_image)

    image_editable.text((100, 100), coin, (3, 252, 44), font=title_font)

    image_editable.text((75, 325), wrongCoin1, (252, 3, 23), font=title_font)

    image_editable.text((542, 349), wrongCoin2, (252, 3, 23), font=title_font)

    my_image.save(f"Images/{filename}")
