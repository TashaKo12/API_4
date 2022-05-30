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


def get_random_path(folders):
    random_directory = random.choice(folders)
    random_picture = random.choice(listdir(random_directory))
    random_path = f'{random_directory}/{random_picture}'
    return random_path


def send_picture(folders, tg_token, chat_id, random_path=None):
    
    if random_path:
        with open(random_path, 'rb') as file:
            photo = file
        updater = Updater(token=tg_token)
        updater.bot.send_photo(
            chat_id=chat_id,
            photo=photo
        )
    else:
        raise ValueError

    

def main():
    
    load_dotenv()
    
    
    folders = [
        FOLDER_NASA,
        FOLDER_SPACEX,
        FOLDER_EPIC
    ]
    seconds_in_one_day = 86400
    
    try:
        random_path = get_random_path(folders)
        while True:
            send_picture(folders, TG_TOKEN, CHAT_ID, random_path)
            sleep(seconds_in_one_day)       
    except ValueError as error:
        print("Can't get data from server:\n{0}".format(error))

    



if __name__ == "__main__":
    main()