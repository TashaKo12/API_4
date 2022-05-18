import os

import requests
from urllib.parse import urlparse, unquote

import download_image

def parsed_links(link):
    link_parse = urlparse(link)
    link_path = link_parse.path
    filename_path = os.path.split(link_path)[1]
    file_extension_path = os.path.splitext(filename_path)[1]
    file_name = os.path.splitext(filename_path)[0]
    extension = unquote(file_extension_path)
    return extension, file_name


def get_images_nasa(folder_nasa, API_KEY):
    link_nasa = "https://api.nasa.gov/planetary/apod"
    count_link = 50
    params = {
        "api_key": API_KEY,
        "count": count_link
    }
    response = requests.get(link_nasa, params=params)
    response.raise_for_status()
    images_nasa_data = response.json()
    for image_nasa_data in images_nasa_data:
        if image_nasa_data["url"]:
            link_nasa = image_nasa_data["url"]
            extension, file_name = parsed_links(link_nasa)
            file_path = f"{folder_nasa}/{file_name}{extension}"
            download_image.download_image(link_nasa, file_path)