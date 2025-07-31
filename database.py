from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["user_mgmt_db"]
user_collection = db["users"]
