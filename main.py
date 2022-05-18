import os
import pathlib
import random
from time import sleep
from os import listdir

from dotenv import load_dotenv
from telegram.ext import Updater

import spacex
import nasa
import epic_nasa


API_KEY = os.environ["API_KEY"]
TG_TOKEN = os.environ["TG_TOKEN"]
CHAT_ID = os.environ['CHAT_ID']


def create_folders(folders):
    for folder in folders:
        pathlib.Path(folder).mkdir(parents=True, exist_ok=True) 


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

def main():
    load_dotenv()
    folder_spacex = "SpaceX"
    folder_nasa = "Nasa"
    folser_epic = "epic"
    
    folders = [
        folder_nasa,
        folder_spacex,
        folser_epic
    ]
	
    create_folders(folders)
    seconds_in_one_day = 86400
    while True:

        send_picture(folders, TG_TOKEN, CHAT_ID)
        sleep(seconds_in_one_day)
    
if __name__ == "__main__":
	main()