import uvicorn
from fastapi import FastAPI, File, UploadFile
import sys
import os
import shutil
from brain.run import main





app = FastAPI()

@app.get("/")
async def home():
    return {"Welcome to mialoo"}


@app.post("/mindmap")
#TODO: PDF müsste man nicht unbedingt nochmals speichern, sondern direkt nach dem Einlesen, damit arbeiten
async def text_api(file: UploadFile = File(...)):
    path_to_file = "app/brain/data/"+ f"{file.filename}"
    with open(path_to_file, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    mindmap = await main(path_to_file)
    return mindmap

if __name__ == "__main__":
    uvicorn.run(app)