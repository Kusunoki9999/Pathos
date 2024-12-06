from fastapi import FastAPI, Request, Form, UploadFile, File
from dotenv import load_dotenv
from pathlib import Path
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import uvicorn
import os

load_dotenv()

app = FastAPI()

GOOGLE_MAP_API_KEY = os.getenv("GOOGLE_MAP_API_KEY")

@app.get("/",response_class = HTMLResponse)
async def root():
    index_path = Path("templates/index.html")
    return index_path.read_text(encoding = "utf-8")

@app.get("/api-key")
async def get_api_key():
    return {"api_key":GOOGLE_MAP_API_KEY}

@app.post("/form_data")
async def get_form_data(title: str = Form(None), caption: str = Form(None), image: UploadFile = File(...)): #...は必須フィールド
    return {
        "title": title,
        "caption": caption,
        "filename": image.filename,
        "content_type": image.content_type,
        }

app.mount("/static", StaticFiles(directory="static"), name="static")

if __name__ == "__main__":
    uvicorn.run(app, port=8080, log_level="debug")