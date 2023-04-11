from typing import Optional
from fastapi import Request
import face_recognition
from fastapi import FastAPI
from pydantic import BaseModel
import requests
from src.helper.file import get_file_md5, remove_file
from src.helper.media_downloader import ImageDownloader
from src.module.face_recognizer import FaceRecognizer

app = FastAPI()
IMAGES_DIR = '/var/local'
print('started')


@app.get("/face-encode")
def read_root(image_url: str):
    try:
        # Download image
        image_name = ImageDownloader.download_account_image(image_url, IMAGES_DIR)
        # Calculate image hash
        image_hash = get_file_md5(f"{IMAGES_DIR}/{image_name}")
        # Compute face encodings
        face_encodings = FaceRecognizer.get_face_encodings_from_image(f"{IMAGES_DIR}/{image_name}")

        return {'face_encodings': face_encodings}
    except:
        return {'code': 502, 'message': 'wrong url'}


print('finished')
