import requests


def download_image(link, file_name, params = None):
    link_image = requests.get(link, params = params)
    with open(file_name, 'wb') as file:
        file.write(link_image.content)
