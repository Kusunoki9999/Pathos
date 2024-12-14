from fastapi import FastAPI, Request, Form, UploadFile, File
from dotenv import load_dotenv
from pathlib import Path
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
from PIL.TiffImagePlugin import IFDRational
import uvicorn
import os
import json
import io

load_dotenv()

app = FastAPI()

GOOGLE_MAP_API_KEY = os.getenv("GOOGLE_MAP_API_KEY")
JSON_FILE_PATH = "form_data.json"
index_path = Path("templates/index.html")

def convert_exif_value(value):
    if isinstance(value, IFDRational):
        return float(value)
    elif isinstance(value, (list, tuple)):
        return [convert_exif_value(v) for v in value]
    return value

def save_to_json(data):
    try:
        if Path(JSON_FILE_PATH).exists():
            with open(JSON_FILE_PATH, "r", encoding="utf-8") as f:
                existing_data = json.load(f)
        else:
            existing_data = []

        existing_data.append(data)

        with open(JSON_FILE_PATH, "w", encoding="utf-8") as f:
            json.dump(existing_data, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Error saving data to JSON: {e}")

        
@app.get("/",response_class = HTMLResponse)
async def root():
    return index_path.read_text(encoding = "utf-8")

@app.get("/api-key")
async def get_api_key():
    return {"api_key":GOOGLE_MAP_API_KEY}

@app.post("/form_data",response_class = HTMLResponse)
async def get_form_data(
    title: str = Form(None),
    caption: str = Form(None),
    image: UploadFile = File(...) #...は必須フィールド
):
    
    image_data = await image.read()
    with Image.open(io.BytesIO(image_data)) as img:
        exif_data = img._getexif()
        
        if exif_data:
            for tag, value in exif_data.items():
                tag_name = TAGS.get(tag, tag)  # タグ番号を名前に変換(第二引数はdefaltのReturn値)
                if tag_name == "GPSInfo": # GPSInfoは辞書型でありbytes型ではない
                    gps_data = {}
                    for gps_tag, gps_value in value.items(): # GPSはタグ名付きの辞書に変換
                        gps_tag_name = GPSTAGS.get(gps_tag, gps_tag)
                        if gps_tag_name == "GPSLatitude":
                            gps_data["GPSLatitude"] = [
                                float(v) if isinstance(v, IFDRational) else v
                                for v in gps_value
                            ]
                        elif gps_tag_name == "GPSLongitude":
                            gps_data["GPSLongitude"] = [
                                float(v) if isinstance(v, IFDRational) else v
                                for v in gps_value
                            ]
                      
    data = {
        "title": title,
        "caption": caption,
        "filename": image.filename,
        "content_type": image.content_type,
        "gps": gps_data,
    }
    save_to_json(data)
    return index_path.read_text(encoding = "utf-8")


app.mount("/static", StaticFiles(directory="static"), name="static")

if __name__ == "__main__":
    uvicorn.run(app, port=8080, log_level="debug")