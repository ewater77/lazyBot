import requests
import configparser

def tgMessage(message):
    # send message to myself by telegram
    print("telegram notify")
    config  = configparser.ConfigParser()
    config.read('config/telegram.ini')
    bot_token = config['bot_credential']['bot_token']
    bot_chatID = config['chat_id']['private_chat_id']
    bot_message = message
    sendMessage = requests.get("https://api.telegram.org/bot" + bot_token + "/sendMessage?chat_id=" + bot_chatID + "&parse_mode=Markdown&text=" + bot_message)
    print(sendMessage.text)


def tgSticker(file_id):
    config  = configparser.ConfigParser()
    config.read('config/telegram.ini')
    bot_token = config['bot_credential']['bot_token']
    bot_chatID = config['chat_id']['private_chat_id']
    sendSticker = requests.get("https://api.telegram.org/bot" + bot_token + "/sendSticker?chat_id=" + bot_chatID + "&sticker=" + file_id)
    print(sendSticker.text)