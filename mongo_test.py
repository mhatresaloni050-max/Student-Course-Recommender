from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")
db = client["test_db"]

db.test.insert_one({"msg": "MongoDB connected"})
print("MongoDB connection SUCCESS")
