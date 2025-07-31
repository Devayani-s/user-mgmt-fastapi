from fastapi import FastAPI
from models import RegisterUser, ApproveUser
from pymongo import MongoClient
from bson import ObjectId
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow frontend to access the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all for testing
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = MongoClient("mongodb://localhost:27017")
db = client["user_mgmt"]
collection = db["users"]

@app.post("/register")
def register_user(user: RegisterUser):
    collection.insert_one({**user.dict(), "active": 0})
    return {"message": "User registered successfully"}

@app.get("/users")
def get_users():
    users = list(collection.find())
    for user in users:
        user["_id"] = str(user["_id"])
    return users

@app.post("/approve_user")
def approve_user(user: ApproveUser):
    result = collection.update_one(
        {"email": user.email},
        {"$set": {"active": 1}}
    )
    if result.matched_count == 0:
        return {"error": "User not found"}
    return {"message": "User approved"}

@app.post("/deactivate_user")
def deactivate_user(user: ApproveUser):
    result = collection.delete_one({"email": user.email})
    if result.deleted_count == 0:
        return {"error": "User not found"}
    return {"message": "User deactivated"}
@app.get("/all_users")
def get_all_users():
    users = list(collection.find({"active": 1}))
    for user in users:
        user["_id"] = str(user["_id"])
    return users
@app.get("/all_users")
def get_all_users():
    users = list(collection.find())  # No filter
    for user in users:
        user["_id"] = str(user["_id"])
    return users
