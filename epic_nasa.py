import datetime

import requests

def epic_nasa(folder, API_KEY):
    link_epic = "https://api.nasa.gov/EPIC/{}"
    params = {
        "api_key": API_KEY
    }
    folder_nasa = folder
    response = requests.get(
               link_epic.format("api/natural/image"),
               params = params
               )
    
    response.raise_for_status()
    image_link = response.json()
    
    for image in image_link:
        filename = image["image"]
        epic_image_date = image["date"]
        epic_image_date = datetime.datetime.strptime(epic_image_date, '%Y-%m-%d  %H:%M:%S')
        epic_image_date = epic_image_date.strftime('%Y/%m/%d')
        
        path = f"archive/natural/{epic_image_date}/png/{filename}.png"
        response = requests.get(
                   link_epic.format(path),
                   params = params
                   )
        file_name = f"{folder_nasa}/{filename}.png"
        with open(file_name, 'wb') as file:
            file.write(response.content)