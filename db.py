from pymongo import MongoClient

client = MongoClient("mongodb+srv://mhatresaloni050_db_user:fA7fMbsDJR1xqfYH@cluster0.2ojqyuv.mongodb.net/?appName=Cluster0")
db = client["studentdb"]

students = db["students"]

