from PIL import Image
from PIL.ExifTags import TAGS
import base64

encoded_path = r"encoded_text\save_encode.txt"
decoded_path = r"decoded_image\decoded.jpg"

with open(encoded_path, 'rb') as f:
    decode_data = base64.b64decode(f.read())

with open(decoded_path, 'wb') as f:
    f.write(decode_data)
