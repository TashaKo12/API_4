import requests


def download_image(link, file_path, params = None):
    link_image = requests.get(link, params = params)
    link_image.raise_for_status()
    with open(file_path, 'wb') as file:
        file.write(link_image.content)
