from pydantic import BaseModel, EmailStr

class RegisterUser(BaseModel):
    name: str
    email: EmailStr
    phone: str
    tool: str

class ApproveUser(BaseModel):
    email: EmailStr
