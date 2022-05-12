from os import listdir
import random

from telegram.ext import Updater



def random_path(folders):
    random_directory = random.choice(folders)
    random_picture = random.choice(listdir(random_directory))
    return random_directory, random_picture
    
def send_picture(folders, TG_TOKEN, CHAT_ID):
    random_directory, random_picture = random_path(folders)
    updater = Updater(token=TG_TOKEN)
    updater.bot.send_photo(
        chat_id=CHAT_ID,
        photo=open(f'{random_directory}/{random_picture}', 'rb')
    )