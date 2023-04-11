from pymongo import MongoClient
import json


mongo_client = MongoClient("mongodb://admin:8YqNhQoJNrZzYeHh3z3XaI6@localhost:21018")

print(mongo_client.list_database_names())
database = mongo_client['as']

accounts = database['accounts']

print("Started")
cursor = accounts.find()
new = []


with open('collection.json', 'w') as file:
    file.write('[')
    for document in cursor:
        document["_id"] = "1"
        file.write(json.dumps(document))
        file.write(',')
    file.write(']')
# with open('data.txt', 'w') as f:
#     f.write(json.dumps(count))

# print(count)

# for a in accounts.find():
#     print(a)