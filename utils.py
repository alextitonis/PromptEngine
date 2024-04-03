import requests
import base64

def web_image_to_base64(url: str) -> str:
    response = requests.get(url)

    if response.status_code == 200:
        image_base64 = base64.b64encode(response.content).decode('utf-8')
        return image_base64
    else:
        print("Failed to fetch the image. Status code:", response.status_code)
        return ""    
    
def get_text_until_first_dot_or_newline(text) -> str:
    dot_index = text.find('.')
    newline_index = text.find('\n')
    
    if dot_index == -1 and newline_index == -1:
        return text
    elif dot_index == -1:
        return text[:newline_index]
    elif newline_index == -1:
        return text[:dot_index]
    else:
        return text[:min(dot_index, newline_index)]
