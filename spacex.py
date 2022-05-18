import requests

import download_image


def fetch_spacex_last_launch(folder):
    image_link = "https://api.spacexdata.com/v3/launches"
    folder_spacex = folder

    response = requests.get(image_link)
    response.raise_for_status()
    launches = response.json()
    try:
        for launch in launches:
            if launch["links"]["flickr_images"]:
                image_list = launch["links"]["flickr_images"]
        for number, link in enumerate(image_list):
            file_path = f"{folder_spacex}/spacex{number}.jpg"
            download_image.download_image(link, file_path)
    except requests.exceptions.HTTPError as error:
        exit("Can't get data from server:\n{0}".format(error))