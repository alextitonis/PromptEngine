import requests
import base64

def WebImageToBase64(url: str):
    response = requests.get(url)

    if response.status_code == 200:
        image_base64 = base64.b64encode(response.content).decode('utf-8')
        return image_base64
    else:
        print("Failed to fetch the image. Status code:", response.status_code)
        return ""    