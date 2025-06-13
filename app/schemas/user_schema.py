from typing import Optional
from pydantic import UUID4, BaseModel, EmailStr
from schemas.role_schema import RoleBase

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
    role: RoleBase

class UserAuthenticated(BaseModel):  # Cambiado a PascalCase
    email: EmailStr

class Token(BaseModel):
    access_token: str
    token_type: str

    class Config:
        from_attributes = True  # Solo si usas objetos ORM
