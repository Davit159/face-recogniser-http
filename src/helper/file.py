import hashlib
import os

def get_file_md5(file_path: str):
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def remove_file(file_path: str):
    if os.path.exists(file_path):
        os.remove(file_path)
