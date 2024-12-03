from fastapi import FastAPI, Request
from dotenv import load_dotenv
from fastapi.staticfiles import StaticFiles
import uvicorn
import os

load_dotenv()

app = FastAPI()

GOOGLE_MAP_API_KEY = os.getenv("GOOGLE_MAP_API_KEY")

app.mount("/", StaticFiles(directory="path/to/your/html/directory", html=True), name="static")

@app.get("/")
async def root():
    return {"message":"Hello,world"}

@app.get("/api-key")
async def get_api_key():
    return {"api_key":GOOGLE_MAP_API_KEY}

if __name__ == "__main__":
    uvicorn.run(app, port=8080, log_level="debug")