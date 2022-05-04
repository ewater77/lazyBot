import configparser
import requests
import sys
from libary.telegram import tgMessage, tgMessageHeartbeat, tgSticker
#from decimal import Decimal
import json
#from bs4 import BeautifulSoup

burp_proxies = {"http":"http://127.0.0.1:8080","https":"https://127.0.0.1:8080"}

def main():
    xrobotmon()

def xrobotmon():
	print("XRobotMon runcookie")
	telegramMessage = ""
	config  = configparser.ConfigParser()
	config.read('config/credential.ini')
	email = config['runcookie']['email']
	#url = "https://httpbin.org/post"
	url = "https://us-central1-robotmon-98370.cloudfunctions.net/xMiscAPI-useCookieKingdomCoupons"
	
	xRobotMonHeaders = {'Content-Type':"application/json"}
	data = json.dumps({'data':{'email':'s66ktrmf6q@privaterelay.appleid.com'}})
	response = requests.post(url,data=data,headers=xRobotMonHeaders, proxies=burp_proxies, verify=False)
	#response = requests.post(url,data=data,headers=xRobotMonHeaders)
	responseJson = json.loads(response.text)
	for runcookieCoupon in responseJson['result']:
		#print(runcookieCoupon['code'])
		if runcookieCoupon['code'] == 42203 :
			print(runcookieCoupon['coupon'] + ": used, code: " + str(runcookieCoupon['code']))
			telegramMessage += runcookieCoupon['coupon'] + ": used, code: " + str(runcookieCoupon['code']) + "\r\n"
			#tgMessageHeartbeat(runcookieCoupon['coupon'] + ": used, code: " + str(runcookieCoupon['code']))
		else:
			print(runcookieCoupon['coupon'] + ": new!?, code: " + str(runcookieCoupon['code']))
			tgMessage(runcookieCoupon['coupon'] + ": new!?, code: " + str(runcookieCoupon['code']))
			tgSticker("CAACAgUAAxkBAAIBNGDrS34d43ol_OgGEQK67zYV5lN-AAIEBQACJeDrDr5dyWExsEgYIAQ")
	if len(responseJson['result']) == 0:
		telegramMessage = "Run Cookie: \nno result"
	tgMessageHeartbeat(telegramMessage)

if __name__ == "__main__":
	if len(sys.argv) < 1:
		print("[*] Usage: python %s <InputFilePath>" % sys.argv[0])
	else:
		main()