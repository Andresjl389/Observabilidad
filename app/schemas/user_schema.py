from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    role: str
    password: str

    class Config:
        from_attributes = True