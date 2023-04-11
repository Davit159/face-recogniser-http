import face_recognition
import json
import base64
import numpy

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

            # print(serialize_face_encoding(person_image_converted_face_encodings[0]))

            if results[0]:
                print(f"The person is {person['name']}")
                return
            else:
                print(f"Not {person['name']}")
                break


def serialize_face_encoding(face_encoding: numpy.ndarray):
    return json.dumps({
        'type': str(face_encoding.dtype),
        'shape': face_encoding.shape,
        'data': face_encoding.tolist()
    })


def unserialize_face_encoding(face_encoding_str: str):
    json_str = face_encoding_str
    json_obj = json.loads(json_str)
    face_encoding = numpy.ndarray(shape=(json_obj['shape']), dtype=json_obj['type'])
    for index, value in enumerate(json_obj['data']):
        face_encoding[index] = value
    return face_encoding


for person in database:
    person['face_encodings'] = []
    for image in person['images']:
        image_conv = face_recognition.load_image_file(f"images/{image}")
        image_face_encodings = face_recognition.face_encodings(image_conv)
        for face_encoding in image_face_encodings:
            person['face_encodings'].append(serialize_face_encoding(face_encoding))


with open('data.json', 'w') as f:
    json.dump(database, f)

# find_face('gor_gor_2.jpeg')
