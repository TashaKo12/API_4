import os
import datetime
import pathlib

import requests
from urllib.parse import urlparse, unquote

from dotenv import load_dotenv
from download_image import download_image



def extraction_extensions_names_links(link):
    link_unquote = unquote(link)
    link_parse =  urlparse(link_unquote)
    path, fullname = os.path.split(link_parse.path)
    file_extension_path = os.path.splitext(fullname)
    file_name, extension = file_extension_path
     
    return extension, file_name


def get_images_nasa(folder_nasa, api_key):
    link_nasa = "https://api.nasa.gov/planetary/apod"
    count_link = 50
    params = {
        "api_key": api_key,
        "count": count_link
    }
    response = requests.get(link_nasa, params=params)
    response.raise_for_status()
    images_nasa_data = response.json()
    for image_nasa_data in images_nasa_data:
        if image_nasa_data["url"]:
            link_nasa = image_nasa_data["url"]
            extension, file_name = extraction_extensions_names_links(link_nasa)
            file_path = f"{folder_nasa}/{file_name}{extension}"
            download_image(link_nasa, file_path)


def get_epic_images_nasa(folder_epic, api_key):
    link_epic = "https://api.nasa.gov/EPIC/{}"
    params = {
        "api_key": api_key
    }
    response = requests.get(
               link_epic.format("api/natural/image"),
               params = params
               )
    
    response.raise_for_status()
    images_epic_data = response.json()
    
    for image_epic_data in images_epic_data:
        filename = image_epic_data["image"]
        epic_image_data = image_epic_data["date"]
        epic_image_data = datetime.datetime.strptime(epic_image_data, '%Y-%m-%d  %H:%M:%S')
        epic_image_data = epic_image_data.strftime('%Y/%m/%d')
        link_path = f"archive/natural/{epic_image_data}/png/{filename}.png"
        link = link_epic.format(link_path)
        file_path = f"{folder_epic}/{filename}.png"
        download_image(link, file_path, params)


def main():
    load_dotenv()

    api_key = os.environ["API_KEY"]
    folder_nasa = os.environ["FOLDER_NASA"]
    folder_epic = os.environ["FOLDER_EPIC"]

    pathlib.Path(folder_nasa).mkdir(parents=True, exist_ok=True)
    pathlib.Path(folder_epic).mkdir(parents=True, exist_ok=True)

    get_images_nasa(folder_nasa, api_key)
    get_epic_images_nasa(folder_epic, api_key)



if __name__ == "__main__":
	main()