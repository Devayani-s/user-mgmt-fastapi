from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from models import RegisterUser, ApproveUser
from pymongo import MongoClient
from bson import ObjectId

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MongoDB connection
client = MongoClient("mongodb://localhost:27017")
db = client["user_mgmt"]
collection = db["users"]

# # Setup template and static file directories
templates = Jinja2Templates(directory="templates")
# app.mount("/static", StaticFiles(directory="static"), name="static")  # optional

# ----------- HTML ROUTES ------------ #

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.get("/admin", response_class=HTMLResponse)
def admin_page(request: Request):
    users = list(collection.find())
    for user in users:
        user["_id"] = str(user["_id"])
    return templates.TemplateResponse("admin.html", {"request": request, "users": users})

@app.get("/approve", response_class=HTMLResponse)
def approve_page(request: Request):
    pending_users = list(collection.find({"active": 0}))
    for user in pending_users:
        user["_id"] = str(user["_id"])
    return templates.TemplateResponse("approve.html", {"request": request, "users": pending_users})

# ----------- API ENDPOINTS ------------ #


@app.post("/register")
async def register_user(user: RegisterUser, request: Request):
    print(await request.json())  # Debug log
    collection.insert_one({**user.dict(), "active": 0})
    return {"message": "User registered successfully"}


@app.post("/approve_user")
def approve_user(user: ApproveUser):
    result = collection.update_one({"email": user.email}, {"$set": {"active": 1}})
    if result.matched_count == 0:
        return {"error": "User not found"}
    return {"message": "User approved"}

@app.post("/deactivate_user")
def deactivate_user(user: ApproveUser):
    result = collection.delete_one({"email": user.email})
    if result.deleted_count == 0:
        return {"error": "User not found"}
    return {"message": "User deactivated"}

@app.get("/users")
def get_users():
    users = list(collection.find())
    for user in users:
        user["_id"] = str(user["_id"])
    return users


# Optional: JSON APIs
@app.get("/all_users")
def get_all_users():
    users = list(collection.find())
    for user in users:
        user["_id"] = str(user["_id"])
    return users

@app.get("/all_active_users")
def get_active_users():
    users = list(collection.find({"active": 1}))
    for user in users:
        user["_id"] = str(user["_id"])
    return users

