import os
import pathlib
from time import sleep

from dotenv import load_dotenv

import spacex
import nasa
import epic_nasa
import telegram_bot


API_KEY = os.environ["API_KEY"]
TG_TOKEN = os.environ["TG_TOKEN"]
CHAT_ID = os.environ['CHAT_ID']
    

def creature_folders(folders):
    for folder in folders:
        pathlib.Path(folder).mkdir(parents=True, exist_ok=True) 


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
    creature_folders(folders)
    seconds_in_one_day = 86400
    while True:
        spacex.fetch_spacex_last_launch(folder_spacex)
        nasa.nasa_image(folder_nasa, API_KEY)
        epic_nasa.epic_nasa(folser_epic, API_KEY)
        telegram_bot.telegram_bot(folders, TG_TOKEN, CHAT_ID)
        sleep(seconds_in_one_day)
    
if __name__ == "__main__":
	main()