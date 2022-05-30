import requests


def download_image(link, file_path, params = None):
    response = requests.get(link, params = params)
    response.raise_for_status()
    with open(file_path, 'wb') as file:
        file.write(response.content)
