# utils/image_utils.py
import re
import base64
import io
from PIL import Image

def resize_image(base64_image: str, size: tuple = (350, 400)) -> str:
    """
    Resizes an image given in base64 format to the specified size and returns it as a base64 string.

    Args:
        base64_image (str): The image in base64 format with an optional prefix.
        size (tuple): The target size as (width, height).

    Returns:
        str: The resized image as a base64-encoded string with the data URI prefix.
    """
    # Remove the image header if present
    image_data = re.sub('^data:image/.+;base64,', '', base64_image)

    # Decode the base64 string to bytes
    image_bytes = base64.b64decode(image_data)
    
    # Open the image and resize it
    image = Image.open(io.BytesIO(image_bytes))
    resized_image = image.resize(size)

    # Convert the resized image back to base64
    img_io = io.BytesIO()
    resized_image.save(img_io, format='JPEG')
    img_io.seek(0)
    resized_image_base64 = base64.b64encode(img_io.getvalue()).decode('utf-8')

    # Return the base64 image with the data URI prefix
    return f"data:image/jpeg;base64,{resized_image_base64}"
