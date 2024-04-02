import base64
from io import BytesIO
from PIL import Image

def PilToBase64(image: Image, format="JPEG"):
    buffered = BytesIO()
    image.save(buffered, format=format)
    img_bytes = buffered.getvalue()
    img_str = base64.b64encode(img_bytes).decode('utf-8')
    return img_str
