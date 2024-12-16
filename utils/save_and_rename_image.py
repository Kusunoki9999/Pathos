from pathlib import Path
import uuid
import aiofiles 

images_dir = Path("static/images")

async def save_and_rename_image(image):
    unique_image_filename = f"{uuid.uuid4().hex}.jpg"
    image_path = images_dir / unique_image_filename

    async with aiofiles.open(image_path, "wb") as f:
        await f.write(image)

    return str(image_path)
