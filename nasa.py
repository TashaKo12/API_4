import os

import requests
from urllib.parse import urlparse, unquote

import download_image


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
            download_image.download_image(link_nasa, file_path)


