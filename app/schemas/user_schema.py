from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class GetUser(BaseModel):
    name: str
    email: EmailStr

class UserAuthenticated(BaseModel):  # Cambiado a PascalCase
    email: EmailStr

class Token(BaseModel):
    access_token: str
    token_type: str

    class Config:
        from_attributes = True  # Solo si usas objetos ORM
