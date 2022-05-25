import os

import random
from time import sleep
from os import listdir

from dotenv import load_dotenv
from telegram.ext import Updater


TG_TOKEN = os.environ["TG_TOKEN"]
CHAT_ID = os.environ['CHAT_ID']
    
FOLDER_SPACEX = os.environ["FOLDER_SPACEX"]
FOLDER_NASA = os.environ["FOLDER_NASA"]
FOLDER_EPIC = os.environ["FOLDER_EPIC"]


def random_path(folders):
    random_directory = random.choice(folders)
    random_picture = random.choice(listdir(random_directory))
    return random_directory, random_picture


def send_picture(folders, tg_token, chat_id):
    random_directory, random_picture = random_path(folders)
    updater = Updater(token=tg_token)
    updater.bot.send_photo(
        chat_id=chat_id,
        photo=open(f'{random_directory}/{random_picture}', 'rb')
    )


def main():
    
    load_dotenv()
    
    
    folders = [
        FOLDER_NASA,
        FOLDER_SPACEX,
        FOLDER_EPIC
    ]

    seconds_in_one_day = 86400
    while True:
        send_picture(folders, TG_TOKEN, CHAT_ID)
        sleep(seconds_in_one_day)


if __name__ == "__main__":
	main()