import json
from json import JSONEncoder
from pymongo import MongoClient


class AccountEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__


class Account:
    def __init__(self, details):
        self.details = details

    @classmethod
    def from_json(cls, json_str):
        return cls(json.loads(json_str))

    def to_json(self):
        return json.dumps(self.details, cls=AccountEncoder)

    def get_images(self):
        return self.details['images'] if 'images' in self.details else []

    def set_images(self, images: list):
        self.details['images'] = images

    def to_dict(self):
        return json.loads(self.to_json())


class Database:
    def insert_account(self, account: Account): pass


class MongoDB(Database):
    def __init__(self, connection_uri: str):
        self.client = MongoClient(connection_uri)
        self.database = self.client["as"]
        self.accounts_collection = self.database["accounts"]

    def insert_account(self, account: Account):
        self.accounts_collection.insert_one(account.to_dict())
