from database import user_collection

def register_user(user: dict):
    user['active'] = 0
    return user_collection.insert_one(user)

def approve_user(email: str, tool: str):
    return user_collection.update_one(
        {"email": email, "tool": tool}, {"$set": {"active": 1}}
    )

def deactivate_user(email: str, tool: str):
    return user_collection.delete_one({"email": email, "tool": tool})

def get_users():
    return list(user_collection.find({}, {"_id": 0}))
