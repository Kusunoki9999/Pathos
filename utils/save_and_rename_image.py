from pathlib import Path
import uuid

images_dir = Path("static/images")

def save_and_rename_image(image):
    unique_image_filename = f"{uuid.uuid4().hex}.jpg"
    image_path = images_dir / unique_image_filename

    with open(image_path, "wb") as f:
        f.write(image.read())

    return str(image_path)
