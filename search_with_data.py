import time

import face_recognition
import json
import base64
import numpy

def unserialize_face_encoding(face_encoding_str: str):
    json_str = face_encoding_str
    json_obj = json.loads(json_str)
    fe = numpy.ndarray(shape=(json_obj['shape']), dtype=json_obj['type'])
    for index, value in enumerate(json_obj['data']):
        fe[index] = value
    return fe


database = []
with open('data.json', 'r') as f:
    database = json.load(f)

for person in database:
    face_encodings = []
    for face_encoding in person['face_encodings']:
        face_encodings.append(unserialize_face_encoding(face_encoding))
    person['face_encodings'] = face_encodings


def find_face(search_image):
    unknown_image = face_recognition.load_image_file(f"images/{search_image}")

    for person in database:
        second_encoding = face_recognition.face_encodings(unknown_image)[0]

        results = face_recognition.compare_faces(person['face_encodings'], second_encoding)

        if results[0]:
            print(f"The person is {person['name']}")
            return
        else:
            print(f"Not {person['name']}")



def serialize_face_encoding(face_encoding: numpy.ndarray):
    return json.dumps({
        'type': str(face_encoding.dtype),
        'shape': face_encoding.shape,
        'data': face_encoding.tolist()
    })


t0 = time.time()
find_face('obama.jpeg')
t1 = time.time()

total = t1-t0
print(float(total))