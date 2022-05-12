from os import listdir
import random

import telegram


def send_picture(folders, TG_TOKEN, CHAT_ID):
    random_directory = random.choice(folders)
    random_picture = random.choice(listdir(random_directory))
    bot = telegram.Bot(token=TG_TOKEN)
    bot.send_document(chat_id=CHAT_ID, document=open(f'{random_directory}/{random_picture}', 'rb'))