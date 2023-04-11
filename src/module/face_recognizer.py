import json
import numpy
import face_recognition


class FaceRecognizer:
    @staticmethod
    def get_face_encodings_from_image(image_path: str):
        # Load image from drive
        image = face_recognition.load_image_file(image_path)
        # Compute face encodings and mapping face_encoding items (ndarray) to wrapper class (FaceEncoding)
        return [FaceEncoding.from_ndarray(ndarray_item) for ndarray_item in face_recognition.face_encodings(image)]


class FaceEncoding:
    def __init__(self, enc_type: str, shape: int, data):
        self.type = enc_type
        self.shape = shape
        self.data = data

    @classmethod
    def from_ndarray(cls, face_encoding: numpy.ndarray):
        return cls(str(face_encoding.dtype), int(face_encoding.shape[0]), face_encoding.tolist())

    @classmethod
    def from_json(cls, json_data: str):
        json_obj = json.loads(json_data)
        return cls(str(json_obj['type']), int(json_obj['shape']), json_obj['data'])

    def to_ndarray(self):
        nda = numpy.ndarray(shape=(self.shape,), dtype=self.type)
        for i, v in enumerate(self.data):
            nda[i] = v
        return nda

    def to_json(self):
        return json.dumps({
            'type': self.type,
            'shape': self.shape,
            'data': self.data
        })