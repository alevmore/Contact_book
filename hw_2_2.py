from bson.objectid import ObjectId
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

client = MongoClient(
    "mongodb+srv://alevmore:Morenko25@cluster0.17fckru.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0",
    server_api=ServerApi('1')
)

db = client.book


result_one = db.cats.insert_one(
    {
        "name": "barsik",
        "age": 3,
        "features": ["ходить в капці", "дає себе гладити", "рудий"],
    }
)

print(result_one.inserted_id)

result_many = db.cats.insert_many(
    [
        {
            "name": "Lama",
            "age": 2,
            "features": ["ходить в лоток", "не дає себе гладити", "сірий"],
        },
        {
            "name": "Liza",
            "age": 4,
            "features": ["ходить в лоток", "дає себе гладити", "білий"],
        },
    ]
)
print(result_many.inserted_ids)

result_find_one = db.cats.find_one({"_id": ObjectId ("6609a75ab07233fb8f98e8eb")})
print(result_find_one)

db.cats.update_one({"name": "barsik"}, {"$set": {"age": 4}})
result_update_one = db.cats.find_one({"name": "barsik"})
print(result_update_one)

db.cats.update_one({"name": "barsik"}, {'$push': {'features': 'пухнастий'}})
result_update_one = db.cats.find_one({"name": "barsik"})
print(result_update_one)

db.cats.delete_one({"name": "barsik"})
result_delete_one = db.cats.find_one({"name": "barsik"})
print(result_delete_one)

result_find_many = db.cats.find({})
for el in result_find_many:
    print(el)
db.cats.delete_many ({ "name": {"$regex": "L"}})
result_delete_many= db.cats.find({})
print (result_delete_many)
