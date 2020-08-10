import requests
import telebot
import time

VKToken = '3ea7affa5a1716323c941bb00686fec0311b70399b413218a20ec4eecfc065feac1145daf86eb0b41c1a8'
Version = 5.92
Domain = 'trtgrp'

BotToken = '1371605417:AAHVR9IrbpkzIkTTYSihXqEwhcMwtY9Qggw'
Bot = telebot.TeleBot (BotToken)

LAST_ID_FILE = 'last_post_id.txt'

@Bot.message_handler(commands=['start'])
def start_message(message):
    Bot.send_message(message.chat.id, 'Bot is on')

def Update ():



    Response = requests.get ('https://api.vk.com/method/wall.get',
                             params={
                                 'access_token' : VKToken,
                                 'v' : Version,
                                 'domain' : Domain
                             }
                             )

    data = Response.json()
    last_id_file_work = open(LAST_ID_FILE, 'r')
    last_post_id = int(last_id_file_work.read())

    if (last_post_id > data['response']['count']):
        last_id_file_work = open(LAST_ID_FILE, 'w')
        last_id_file_work.write(str(data['response']['count']))
        last_id_file_work.close()

    if (data['response']['count'] > last_post_id):
        count_of_new_posts = data['response']['count'] - last_post_id

        index = count_of_new_posts
        while (count_of_new_posts > 0):
            if (data['response']['items'][count_of_new_posts]['text'] != ''):
                Bot.send_message('@capbottest', data['response']['items'][count_of_new_posts]['text'])
            count_of_new_posts -= 1

        last_id_file_work.close()
        last_id_file_work = open(LAST_ID_FILE, 'w')
        last_id_file_work.write(str(data['response']['count']))
        last_id_file_work.close()

while (True):
    Update()
    time.sleep(1)

Bot.polling()

# Response = requests.get ('https://api.vk.com/method/wall.get',
#                              params={
#                                  'access_token' : VKToken,
#                                  'v' : Version,
#                                  'domain' : Domain
#                              }
#                              )
#
# Data = Response.json()
# print (1)