import time

import face_recognition
import json
import base64
import numpy
import hashlib

def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


database = [
    {'name': 'Biden', 'images': [
        'biden.jpeg', 'unknown.jpg'
    ]},
    {'name': 'Dav', 'images': [
            'dav_951.jpeg'
        ]},
    {'name': 'Gor', 'images': [
        'gor_gor_1.jpeg', 'gor_gor_2.jpeg', 'gor_gor_3.jpeg', 'gor_gor_4.jpeg', 'gor_gor_5.jpeg',
    ]},
    {'name': 'Kevin', 'images': [
        'image.jpeg'
    ]},
    {'name': 'Sasha', 'images': [
        'image (1).jpeg'
    ]},
    {'name': 'Obama', 'images': [
        'obama.jpeg'
    ]},
]


def find_face(search_image):
    unknown_image = face_recognition.load_image_file(f"images/{search_image}")

    for person in database:
        for person_image in person['images']:
            person_image_converted = face_recognition.load_image_file(f"images/{person_image}")

            person_image_converted_face_encodings = face_recognition.face_encodings(person_image_converted)
            second_encoding = face_recognition.face_encodings(unknown_image)[0]

            results = face_recognition.compare_faces(person_image_converted_face_encodings, second_encoding)

            if results[0]:
                print(f"The person is {person['name']}")
                return
            else:
                print(f"Not {person['name']}")
                break


t0 = time.time()
find_face('gor_gor_2.jpeg')
t1 = time.time()

total = t1-t0
print(float(total))
