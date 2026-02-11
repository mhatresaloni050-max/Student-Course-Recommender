from pymongo import MongoClient

client = MongoClient("Mongo_URL")
db = client["studentdb"]

students = db["students"]

