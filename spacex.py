import os
import pathlib

import requests

from dotenv import load_dotenv
from download_image import download_image



def fetch_spacex_last_launch(folder_spacex):
    
    image_link = "https://api.spacexdata.com/v3/launches"

    response = requests.get(image_link)
    response.raise_for_status()
    launches = response.json()
    
    for launch in launches:
        if launch["links"]["flickr_images"]:
            image_list = launch["links"]["flickr_images"]
            break
    for number, link in enumerate(image_list):
        file_path = f"{folder_spacex}/spacex{number}.jpg"
        download_image(link, file_path)
    


def main():
    load_dotenv()
    
    folder_spacex = os.environ["FOLDER_SPACEX"]

    pathlib.Path(folder_spacex).mkdir(parents=True, exist_ok=True)
    
    try:
        fetch_spacex_last_launch(folder_spacex)
    except requests.exceptions.HTTPError as error:
        print("Can't get data from server:\n{0}".format(error))


if __name__ == "__main__":
    main()