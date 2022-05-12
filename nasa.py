import os

import requests
from urllib.parse import urlparse, unquote

import download_image

def parser_links(link):
    link_parse = urlparse(link)
    link_path = link_parse.path
    filename_path = os.path.split(link_path)[1]
    file_extension_path = os.path.splitext(filename_path)[1]
    file_name = os.path.splitext(filename_path)[0]
    expansion = unquote(file_extension_path)
    return expansion, file_name


def nasa_image(folder, API_KEY):
    link_nasa = "https://api.nasa.gov/planetary/apod"
    folder_nasa = folder
    count_link = 50
    params = {
        "api_key": API_KEY,
        "count": count_link
    }
    response = requests.get(link_nasa, params=params)
    response.raise_for_status()
    image_nasa = response.json()
    for link_image in image_nasa:
        if link_image["url"]:
            link_nasa = link_image["url"]
            expansion, file_name = parser_links(link_nasa)
            file_name = f"{folder_nasa}/{file_name}{expansion}"
            download_image.download_image(link_nasa, file_name)
        else:
            continue