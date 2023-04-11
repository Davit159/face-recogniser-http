import json
from confluent_kafka import Consumer, KafkaError
import requests
from pymongo import MongoClient


images_dir = "images"
accept_token = "203D9BC00226C3B49D9DC13990182E64118B34C33099576609FE13C05EC20F06"

mongo_client = MongoClient("mongodb+srv://manager:Manager_951951@as.ftql2.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")


print(mongo_client.db)
database = mongo_client["db"]

images_collection = database["image"]

accounts_collection = database["accounts"]


def save_accounts_info(account):
    del account['images']
    accounts_collection.insert_one(account)


def extract_image_info_from_account(account):
    image_info = {
        'images': account['images'],
        'account_provider': account['account_provider'],
        'account_id': account['account_id']
    }
    return image_info


def save_images(image_info):
    if "images" in image_info and len(image_info["images"]) > 0:
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


def collect_accounts(content):
    try:
        account = json.loads(content)


        account_images = extract_image_info_from_account(account)
        save_images(account_images)

        save_accounts_info(account)
        return json.dumps({"status": "ok"}), 200
    except BaseException as e:
        error = json.dumps({"status": "error", "message": str(e)})
        print(error)
        return error, 405


if __name__ == '__main__':
    consumer = Consumer({
        "bootstrap.servers": "localhost:9092",
        'group.id': 'face-recogniser'
    })
    consumer.subscribe(['accounts'])

    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                continue
            else:
                print(msg.error())
                break

        message = msg.value().decode('utf-8')
        print(f"Received message: {message}")
        collect_accounts(message)

