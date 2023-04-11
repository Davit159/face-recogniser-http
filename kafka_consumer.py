from src.module.face_recognizer import FaceRecognizer
from src.module.kafka_consumer import KafkaConsumer, KafkaMessage
from src.helper.file import get_file_md5, remove_file
from src.module.database import MongoDB, Account
from src.helper.media_downloader import ImageDownloader

images_count = 0
def consume(message: KafkaMessage):
    global images_count
    # Process data
    account = Account.from_json(message.to_json())
    print("Consumed ", account.to_dict())

    image_collection = []
    images = account.get_images()
    images_count = len(images)
    if images_count > 10:
        images_count = 10
    for i in range(images_count):
        image_url = images[i]
        try:
            # Download image
            image_name = ImageDownloader.download_account_image(image_url, IMAGES_DIR)
            # Calculate image hash

            image_hash = get_file_md5(f"{IMAGES_DIR}/{image_name}")
            # Compute face encodings

            face_encodings = FaceRecognizer.get_face_encodings_from_image(f"{IMAGES_DIR}/{image_name}")

            # Check if any faces found on picture
            faces_found = len(face_encodings)
            print(1111111111111111111111111)
            # Append image information to image collection
            if faces_found == 0:
                remove_file(f"{IMAGES_DIR}/{image_name}")
                continue
            print(22222222222222222222222222222222)
            image_collection.append({
                'name': image_name,
                'hash': image_hash,
                'faces_found': faces_found,
                'face_encodings': face_encodings
            })
        except(BaseException, Exception) as ex:
            print(ex)
            print(f"error with some image - {image_url}")
    account.set_images(image_collection)
    print(3333333333333333333333333333)
    if len(image_collection) > 0:
        mongo_client.insert_account(account)
    # print(account.to_dict())


IMAGES_DIR = '/var/local'

mongo_client = MongoDB("mongodb://admin:8YqNhQoJNrZzYeHh3z3XaI6@10.5.0.10:27017")

# KAFKA_CONSUMER_CONFIGURATION = {
#     'bootstrap.servers': 'localhost:9092',
#     'message.max.bytes': 5242880,
#     'security.protocol': 'SASL_PLAINTEXT',
#     'sasl.username': 'admin',
#     'sasl.password': 'admin-secret',
#     'sasl.mechanism': 'PLAIN',
#     'group.id': 'accounts_all',
#     'queued.max.messages.kbytes': 2000000,
#     'default.topic.config': {'auto.offset.reset': 'smallest'},
#     'session.timeout.ms': 10000,
# }

KAFKA_CONSUMER_CONFIGURATION = {
    'bootstrap.servers': 'rocket-01.srvs.cloudkafka.com:9094',
    'message.max.bytes': 5242880,
    'security.protocol': 'SASL_SSL',
    'sasl.username': 'vf6c2fc0',
    'sasl.password': 'r-DzbtQNiKtylOjPKspiJdRmjF7xkAKL',
    'sasl.mechanism': 'SCRAM-SHA-256',
    'group.id': 'accounts_all',
}

subscribe_topics = ["vf6c2fc0-default"]

print('Starting consumer on topic ' + str(subscribe_topics))
print('Starting consuming')

kafka_consumer = KafkaConsumer(KAFKA_CONSUMER_CONFIGURATION, subscribe_topics)
kafka_consumer.consume(consume)


