#!/usr/bin/python
# -*- coding: utf-8 -*-

# File Description: daily work for crypto
# Author: Walter Chen (walter@walter.com.tw)
# Date: 2021/07/05
# Version: 1.0
# Environment: Python 3.8.2 64bit

import sys
import requests
import configparser
from bs4 import BeautifulSoup
import json

from libary.telegram import tgMessage, tgMessageHeartbeat, tgSticker

burp_proxies = {"http":"http://192.168.10.102:8080","https":"http://192.168.10.102:8080"}

def ftxSwag():
    # nft lottery, enable draw every 22 hrs
    print("get ftx swag")
    config  = configparser.ConfigParser()
    config.read('config/credential.ini')
    authorization = config['ftx']['authorization']
    ftx_headers = {'Authorization':authorization, 'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    r = requests.post("https://ftx.com/api/swag/spin_wheel", headers=ftx_headers)
    r_json = json.loads(r.text)
    print(r_json)
    stickerID = ""
    if r_json['success'] == True:
        #if r_json['error'] == False:
        if r_json['result'] == False:
            telegramMessage = "FTX Swag: \r\ndraw `nothing`, keep trying..."
            stickerID = "CAACAgUAAxkBAAPmYOn8C4ZrnO1qJfdPdtQ-ai9FqaUAAgMFAAIl4OsOkcL1sIIVUQYgBA"
        else:
            telegramMessage = "FTX Swag: \r\ndraw `something!!`"
            stickerID = "CAACAgUAAxkBAAPqYOn-qbLYXOMdG3PPuY0g_3vH0igAAhcFAAIl4OsOYOQIRar6TdAgBA"
    elif r_json['error'] == "Already spun wheel in the last 24 hours":
        telegramMessage = "FTX Swag: \r\nAlready spun wheel in the last 24 hours"
        #stickerID = "CAACAgUAAxkBAAIBLGDrMQfk-2PWz5O0rg1hbBwxZ7DKAAJAEgAC1x2LBieD-RRfxNlZIAQ"
    else:
        telegramMessage = "FTX Swag: \r\nOther error occur, please check status"
    
    if stickerID != "":
        tgSticker(stickerID)
        tgMessage(telegramMessage)
    else:
        tgMessageHeartbeat(telegramMessage)

def coingeckoCandy():
    # get coingecko daily candy
    print("get coingeko candy")
    config  = configparser.ConfigParser()
    config.read('config/credential.ini')
    remember_user_token = config['coingecko']['remember_user_token']
    _session_id = config['coingecko']['_session_id']
    authenticity_token = config['coingecko']['authenticity_token']
    coingecgo_cookie = {"remember_user_token":remember_user_token
    ,"_session_id":_session_id}
    coingecgo_postData = {"authenticity_token":authenticity_token}
    coingecgo_header = {"X-Requested-With": "XMLHttpRequest",  'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    # Before retrive
    getCandyAmount = requests.get("https://www.coingecko.com/account/candy?locale=en", cookies=coingecgo_cookie, headers=coingecgo_header)
    sp = BeautifulSoup(getCandyAmount.text, 'html.parser')
    sel = sp.select("div[data-target='points.balance']")
    for s in sel:
        candyAmount = s.text
    beforeRetriveCandyAmount = candyAmount
    # Retrive
    getCandy = requests.post("https://www.coingecko.com/account/candy/daily_check_in", cookies=coingecgo_cookie, data=coingecgo_postData, headers=coingecgo_header, verify=False)
    if getCandy.status_code == 200:
        getCandyStatus = "Get candy process ok"
    else:
        getCandyStatus = "Get candy fail, please check status: " + str(getCandy.status_code)
    # After retrive
    getCandyAmount = requests.get("https://www.coingecko.com/account/candy?locale=en", cookies=coingecgo_cookie, headers=coingecgo_header)
    sp = BeautifulSoup(getCandyAmount.text, 'html.parser')
    sel = sp.select("div[data-target='points.balance']")
    for s in sel:
        candyAmount = s.text
    getCandy = int(candyAmount) - int(beforeRetriveCandyAmount)
    if getCandy != 0:
        getCandyMessage = "Get `" + str(getCandy) + "` candy"
    else:
        getCandyMessage = "Not get candy this time"
    # Get Message from candy page
    sel = sp.select("div[class='mb-2 font-weight-bold']")
    for s in sel:
        candyAmountToday = s.text
    telegramMessage = "CoinGecko Candy: \r\n"+ "Candy amount: `" + candyAmount + "`"
    #telegramMessage = "CoinGecko Candy: \r\n"+ "Candy amount: `" + candyAmount + "`\r\n" + getCandyMessage + "\r\n" + candyAmountToday + "\r\n"
    #telegramMessage += getCandyStatus    
    if getCandy != 0:
        tgSticker("CAACAgUAAxkBAAIBNGDrS34d43ol_OgGEQK67zYV5lN-AAIEBQACJeDrDr5dyWExsEgYIAQ")
        tgMessage(telegramMessage)
    else:
        tgMessageHeartbeat(telegramMessage)


def shopeeCoin():
    # get shopee coin daily 0.1 -> 0.2 -> 0.3 -> 0.4 -> 0.5 -> 0.5 -> 1 -> ...
    # 3 months expired
    print("get shopee coin")
    config  = configparser.ConfigParser()
    config.read('config/credential.ini')
    SPC_EC = config['shopee']['SPC_EC']
    shopeeCookie = {"SPC_EC":SPC_EC}
    shopeeHeaders = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

    # Retrive shopee coin
    rShpeeCheckin = requests.post("https://shopee.tw/mkt/coins/api/v2/checkin_new", cookies=shopeeCookie, headers=shopeeHeaders)
    #print(rShpeeCheckin.text)

    # After get shopee coin
    rShpoeeCoinAmount = requests.get("https://shopee.tw/api/v0/coins/api/summary/", cookies= shopeeCookie, headers=shopeeHeaders)
    jsonShpoeeCoinAmount= json.loads(rShpoeeCoinAmount.text)
    shpoeeCoinAmount = jsonShpoeeCoinAmount['coins']['available_amount']
    print("ShpoeeCoinAmount: " + str(shpoeeCoinAmount))

    #sp = BeautifulSoup(getCandyAmount.text, 'html.parser')
    jsonShpeeCheckin = json.loads(rShpeeCheckin.text)
    if jsonShpeeCheckin['msg'] == "success":
        if jsonShpeeCheckin['data']['success'] == True:
            #print("Shopee:\r\nget shopee coin")
            tgMessage("Shopee:\r\nget shopee coin, now have `" + str(shpoeeCoinAmount) + "`")
            tgSticker("CAACAgUAAxkBAAIBNGDrS34d43ol_OgGEQK67zYV5lN-AAIEBQACJeDrDr5dyWExsEgYIAQ")
        else:
            #print("Shopee:\r\nWait tomorrow")
            tgMessageHeartbeat("shopee:\r\nWait tomorrow, now have `" + str(shpoeeCoinAmount) + "`")
    else:
        #print("Shopee:\r\nsomething wrong...")
        tgMessage("Shopee:\r\nsomething wrong...")


def coinmarketcapDiamond():
    print("get coinmarketcap diamonds")
    config  = configparser.ConfigParser()
    config.read('config/credential.ini')
    Authorization = config['coinmarketcap']['Authorization']
    coinmarketcapHeaders = {'Authorization':Authorization, 'Content-Type':"application/json;charset=UTF-8"}
    coinmarketcapData = "{}"
    responseCoinmarketcapCheckin = requests.post("https://api.coinmarketcap.com/asset/v3/loyalty/check-in/", headers=coinmarketcapHeaders, data=coinmarketcapData)
    jsonCoinmarketcapCheckin = json.loads(responseCoinmarketcapCheckin.text)
    stickerID = ""
    if jsonCoinmarketcapCheckin["status"]["error_message"] == "SUCCESS":
        tmpMessage = "Coinmarketcap:\r\nGet coinmarketcap diamonds"
        stickerID = "CAACAgUAAxkBAAIBNGDrS34d43ol_OgGEQK67zYV5lN-AAIEBQACJeDrDr5dyWExsEgYIAQ"
        #tgSticker("CAACAgUAAxkBAAIBNGDrS34d43ol_OgGEQK67zYV5lN-AAIEBQACJeDrDr5dyWExsEgYIAQ")
    elif jsonCoinmarketcapCheckin["status"]["error_message"] == "The userId and checkIn date is unique,you can't check in twice a day":
        tmpMessage = "Coinmarketcap:\r\nWait tomorrow"
    else:
        tmpMessage = "Coinmarketcap:\r\nsometime error please check"
    #print(jsonCoinmarketcap.text)
    coinmarketcapCandyAmount = requests.post("https://api.coinmarketcap.com/asset/v3/loyalty/user-point-summary", headers=coinmarketcapHeaders, data=coinmarketcapData)
    jsonCoinmarketcapCandyAmount = json.loads(coinmarketcapCandyAmount.text)
    DiamondAmount = jsonCoinmarketcapCandyAmount["data"]["point"]
    tgMessage(tmpMessage + ", now have `" + str(DiamondAmount) + "`")
    if stickerID != "":
        tgSticker(stickerID)


def main():
    ftxSwag()
    #coingeckoCandy()
    shopeeCoin()
    #coinmarketcapDiamond()

if __name__ == "__main__":
	if len(sys.argv) < 1:
		print("[*] Usage: python %s <InputFilePath>" % sys.argv[0])
	else:
		main()