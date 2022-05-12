import requests


def fetch_spacex_last_launch(folder):
    image_link = "https://api.spacexdata.com/v3/launches"
    folder_spacex = folder

    response = requests.get(image_link)
    response.raise_for_status()
    launches = response.json()
    try:
        while len(launches):
            launch = launches.pop()
            if not len(launch["links"]["flickr_images"]):
                continue
            image_list = launch["links"]["flickr_images"]
        for number, link in enumerate(image_list):
            file_name = f"{folder_spacex}/spacex{number}.jpg"
            link_image = requests.get(link)
            with open(file_name, 'wb') as file:
                file.write(link_image.content)
    except requests.exceptions.HTTPError as error:
        exit("Can't get data from server:\n{0}".format(error))