from pymongo import MongoClient

client = MongoClient('mongodb://127.0.0.1:27017')
db = client.musicdb
cursor = db.musicData.find()
for document in cursor:
    print(document)