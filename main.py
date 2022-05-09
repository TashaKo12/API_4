import os
import pathlib
import random
from time import sleep
from os import listdir

import requests
import telegram
from dotenv import load_dotenv
from urllib.parse import urlparse, unquote


API_KEY = os.getenv["API_KEY"]
TG_TOKEN = os.getenv["TG_TOKEN"]
CHAT_ID = os.getenv['CHAT_ID']

def fetch_spacex_last_launch(folders):
    image_link = "https://api.spacexdata.com/v3/launches"
    folder_spacex = folders[0]

    response = requests.get(image_link)
    response.raise_for_status()
    images = response.json()
    try:
        while len(images):
            launch = images.pop()
            if not len(launch["links"]["flickr_images"]):
                continue
            image_list = launch["links"]["flickr_images"]
        for numder, link in enumerate(image_list):
            file_name = f"{folder_spacex}/spacex{numder}.jpg"
            link_image = requests.get(link)
            with open(file_name, 'wb') as file:
                file.write(link_image.content)
    except requests.exceptions.HTTPError as error:
        exit("Can't get data from server:\n{0}".format(error))
    

def creature_folder(folders):
    for folder in folders:
        pathlib.Path(folder).mkdir(parents=True, exist_ok=True) 


def parser_links(link):
    link_parse = urlparse(link)
    link_path = link_parse.path
    filename_path = os.path.split(link_path)[1]
    file_extension_path = os.path.splitext(filename_path)[1]
    file_name = os.path.splitext(filename_path)[0]
    expansion = unquote(file_extension_path)
    return expansion, file_name


def nasa_image(folders):
    link_nasa = "https://api.nasa.gov/planetary/apod"
    folder = folders[1]
    params = {
        "api_key": API_KEY,
        "count": 50
    }
    response = requests.get(link_nasa, params=params)
    response.raise_for_status()
    image_nasa = response.json()
    for link_image in image_nasa:
        if len(link_image["url"]):
            link_nasa = link_image["url"]
            expansion, file_name = parser_links(link_nasa)
            response = requests.get(link_nasa)
            file_name = f"{folder}/{file_name}{expansion}"
            with open(file_name, 'wb') as file:
                file.write(response.content)
        else:
            continue



def epic_nasa(folders):
    link_epic = "https://api.nasa.gov/EPIC/{}"
    params = {
        "api_key": API_KEY
    }
    folder = folders[2]
    response = requests.get(
               link_epic.format("api/natural/image"),
               params = params
               )
    
    response.raise_for_status()
    image_link = response.json()
    
    for image in image_link:
        filename = image["image"]
        epic_image_date = image["date"][:10].replace("-", "/")
        path = f"archive/natural/{epic_image_date}/png/{filename}.png"
        response = requests.get(
                   link_epic.format(path),
                   params = params
                   )
        file_name = f"{folder}/{filename}.png"
        with open(file_name, 'wb') as file:
            file.write(response.content)

def telegram_bot(folders):
    random_directory = random.choice(folders)
    random_picture = random.choice(listdir(random_directory))
    bot = telegram.Bot(token=TG_TOKEN)
    bot.send_document(chat_id=CHAT_ID, document=open(f'{random_directory}/{random_picture}', 'rb'))

def main():
    folders = [
        "SpaceX",
        "Nasa",
        "epic"
    ]
    creature_folder(folders)
    seconds_in_one_day = 86400
    while True:
        fetch_spacex_last_launch(folders)
        nasa_image(folders)
        epic_nasa(folders)
        telegram_bot(folders)
        sleep(seconds_in_one_day)
    
if __name__ == "__main__":
    load_dotenv()
	main()