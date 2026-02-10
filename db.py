from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["student_ai"]

users = db["users"]
students = db["students"]
