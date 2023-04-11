import requests
from PIL import Image
from io import BytesIO
import uuid


class ImageDownloader:
    @staticmethod
    def download(image_url: str, folder_path: str, name: str):
        try:
            # print(f"Downloading {name}")
            response = requests.get(image_url)
            image = Image.open(BytesIO(response.content))
            rgb_im = image.convert('RGB')
            rgb_im.save(f"{folder_path}/{name}")
            return True
        except (Exception, BaseException):
            print(f"Error downloading {image_url}")
            return False

    @staticmethod
    def download_account_image(image_url: str, folder_path: str):
        image_name = f"{uuid.uuid4()}.jpg"
        ImageDownloader.download(image_url, folder_path, image_name)
        return image_name
