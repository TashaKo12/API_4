import os
from datetime import datetime
import pathlib

import requests
from urllib.parse import urlparse, unquote

from dotenv import load_dotenv
from download_image import download_image



def extract_extension_from_link(link):
    link_unquote = unquote(link)
    link_parse =  urlparse(link_unquote)
    path, fullname = os.path.split(link_parse.path)
    file_extension_path = os.path.splitext(fullname)
    file_name, extension = file_extension_path
     
    return extension, file_name


def get_nasa_images(folder_nasa, api_key):
    nasa_link_apod = "https://api.nasa.gov/planetary/apod"
    links_count = 50
    params = {
        "api_key": api_key,
        "count": links_count
    }
    response = requests.get(nasa_link_apod, params=params)
    response.raise_for_status()
    nasa_images = response.json()
    for image_nasa in nasa_images:
        if image_nasa["url"]:
            nasa_link_image = image_nasa["url"]
            extension, file_name = extract_extension_from_link(nasa_link_image)
            file_path = f"{folder_nasa}/{file_name}{extension}"
            download_image(nasa_link_image, file_path)


def get_epic_nasa_apod_images(folder_epic, api_key):
    link_epic = "https://api.nasa.gov/EPIC/api/natural/image"
    params = {
        "api_key": api_key
    }

    response = requests.get(
        link_epic,
        params = params
    )
    
    response.raise_for_status()
    epic_images = response.json()
    
    for epic_image in epic_images:
        filename = epic_image["image"]
        epic_image_date = epic_image["date"]
        epic_image_date = datetime.fromisoformat(epic_image_date).strftime("%Y/%m/%d")
        link_path = f"https://api.nasa.gov/EPIC/archive/natural/{epic_image_date}/png/{filename}.png"
        file_path = f"{folder_epic}/{filename}.png"
        download_image(link_path, file_path, params)


def main():
    load_dotenv()

    api_key = os.environ["API_KEY"]
    folder_nasa = os.environ["FOLDER_NASA"]
    folder_epic = os.environ["FOLDER_EPIC"]

    pathlib.Path(folder_nasa).mkdir(parents=True, exist_ok=True)
    pathlib.Path(folder_epic).mkdir(parents=True, exist_ok=True)

    get_nasa_images(folder_nasa, api_key)
    get_epic_nasa_apod_images(folder_epic, api_key)



if __name__ == "__main__":
    main()
