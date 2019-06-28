from pymongo import MongoClient

client = MongoClient('mongodb://127.0.0.1:27017')
db = client.musicdb
musicData = db.musicData
result = musicData.insert_one(
    {'name':'Diamonds','author':'Tom','playcounts':22}
)
print(result.inserted_id)