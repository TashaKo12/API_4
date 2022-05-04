import os
import pathlib

import requests
import telegram
from urllib.parse import urlparse, unquote


API_KEY = os.environ["API_KEY"]
TG_TOKEN = os.environ["TG_TOKEN"]
CHAT_ID = os.environ['CHAT_ID']

def fetch_spacex_last_launch():
    image_link = "https://api.spacexdata.com/v3/launches"
    folder = "SpaceX"

    response = requests.get(image_link)
    response.raise_for_status()
    images = response.json()
    try:
        pathlib.Path(folder).mkdir(
                                    parents=True, 
                                    exist_ok=True
                                  )
        while len(images):
            launch = images.pop()
            if not len(launch["links"]["flickr_images"]):
                continue
            image_list = launch["links"]["flickr_images"]
        for numder, link in enumerate(image_list):
            file_name = f"{folder}/spacex{numder}.jpg"
            link_image = requests.get(link)
            with open(file_name, 'wb') as file:
                file.write(link_image.content)
    except requests.exceptions.HTTPError as error:
        exit("Can't get data from server:\n{0}".format(error))
    

def creature_folder(folder):
    pathlib.Path(folder).mkdir(parents=True, exist_ok=True) 


def parser_links(link):
    link_parse = urlparse(link)
    link_path = link_parse.path
    filename_path = os.path.split(link_path)[1]
    file_extension_path = os.path.splitext(filename_path)[1]
    file_name = os.path.splitext(filename_path)[0]
    expansion = unquote(file_extension_path)
    return expansion, file_name


def nasa_image():
    link_nasa = "https://api.nasa.gov/planetary/apod"
    folder = "Nasa"
    params = {
        "api_key": API_KEY,
        "count": 50
    }
    response = requests.get(link_nasa, params=params)
    response.raise_for_status()
    image_nasa = response.json()
    pathlib.Path(folder).mkdir(parents=True, exist_ok=True)
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



def epic_nasa():
    link_epic = "https://api.nasa.gov/EPIC/{}"
    params = {
        "api_key": API_KEY
    }
    folder = "epic"
    pathlib.Path(folder).mkdir(parents=True, exist_ok=True)
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

def telegram_bot():
    bot = telegram.Bot(token=TG_TOKEN)
    bot.send_message(text="Я выжил", chat_id=chat_id)

def main():
    #fetch_spacex_last_launch()
    #nasa_image()
    #epic_nasa()
    telegram_bot()
    
if __name__ == "__main__":
	main()