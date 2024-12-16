from fastapi import FastAPI, Request, Form, UploadFile, File
from dotenv import load_dotenv
from pathlib import Path
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from utils.save_and_rename_image import save_and_rename_image
from utils.get_GPSInfo import extract_gps_from_image
from utils.json_operater import save_to_json
import uvicorn
import os
import json


load_dotenv()
app = FastAPI()

GOOGLE_MAP_API_KEY = os.getenv("GOOGLE_MAP_API_KEY")
index_path = Path("templates/index.html")
images_dir = Path("static/images")
JSON_FILE_PATH = "form_data.json"


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
    
    image_path = await save_and_rename_image(image)
    gps_data = extract_gps_from_image(image)
                      
    data = {
        "title": title,
        "caption": caption,
        "filename": image.filename,
        "image_path": image_path,
        "gps": gps_data,
    }
    
    save_to_json(data)
    return index_path.read_text(encoding = "utf-8")

@app.get("/user-post-details")
async def get_locations():
    with open(JSON_FILE_PATH, "r", encoding="utf-8") as f:
        post_details = json.load(f)
    return post_details

app.mount("/static", StaticFiles(directory="static"), name="static")

if __name__ == "__main__":
    uvicorn.run(app, port=8080, log_level="debug")