import json

from datetime import timedelta
import requests
from pymongo import MongoClient

from flask import Flask, request, abort

images_dir = "images"

mongo_client = MongoClient("mongodb+srv://manager:Manager_951951@as.ftql2.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

database = mongo_client["kafka"]

images_collection = database["image"]

accounts_collection = database["accounts"]


def save_accounts_info(accounts):
    for account in accounts:
        del account['images']
    accounts_collection.insert_many(accounts)


def extract_image_info_from_account(account):
    image_info = {
        'images': account['images'],
        'account_provider': account['account_provider'],
        'account_id': account['account_id']
    }
    return image_info


def save_images(image_info):
    req_body = {'images': image_info['images']}
    res = requests.post('http://localhost:5000/images', json=req_body).json()
    image_id_list = res['id_list']
    images = []
    for image_id in image_id_list:
        images.append({
            "id": image_id,
            "acc_prov": image_info['account_provider'],
            "acc_id": image_info['account_id']
        })
    if len(images) > 0:
        images_collection.insert_many(images)


@api.route('/accounts', methods=['POST'])
def collect_accounts():
    try:
        content = request.get_json(silent=True)
        if content is None:
            print("wrong Request !!!!")
            abort(405)

        accounts = content["accounts"]

        for account in accounts:
            account_images = extract_image_info_from_account(account)
            save_images(account_images)

        save_accounts_info(accounts)
        return json.dumps({"status": "ok"}), 200
    except BaseException as e:
        return json.dumps({"status": "error", "message": str(e)}), 405


if __name__ == '__main__':
    api.run('0.0.0.0', port=8000)
