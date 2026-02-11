from dotenv import load_dotnev
import os
from pymongo import MongoClient

load_dotenv()
mongo_uri = os.getenv("Mongo_URL")
client=MongoClient(mongo_uri)
