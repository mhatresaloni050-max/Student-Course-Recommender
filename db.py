from dotenv import load_dotnev
import os
from pymongo import MongoClient

<<<<<<< HEAD
client = MongoClient("mongodb://localhost:27017/")
db = client["student_ai"]

users = db["users"]
students = db["students"]
=======
load_dotenv()
mongo_uri = os.getenv("Mongo_URL")
client=MongoClient(mongo_uri)
>>>>>>> cbfc4e2f2274f1b4e76a661279ccf8f573b8b6a1
