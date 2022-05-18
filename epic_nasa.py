import datetime

import requests

import download_image


def get_epic_images_nasa(folder, api_key):
    link_epic = "https://api.nasa.gov/EPIC/{}"
    params = {
        "api_key": api_key
    }
    folder_nasa = folder
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
        file_path = f"{folder_nasa}/{filename}.png"
        download_image.download_image(link, file_path, params)
        