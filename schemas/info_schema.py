from typing import Optional
from pydantic import BaseModel, EmailStr, UUID4

from schemas.type_schema import GetType
from schemas.user_schema import GetUser

class InfoBase(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    icon: Optional[str] = None
    link: Optional[str] = None

# class GetInfo(InfoBase):
#     id: UUID4
#     class Config:
#         from_attributes = True

class InfoVideoBase(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    link: Optional[str] = None

class GetInfo(InfoBase):
    id: UUID4
    user_id: UUID4
    type_id: Optional[UUID4] = None
    filename: Optional[str] = None
    filepath: Optional[str] = None
    
class GetVideo(InfoVideoBase):
    id: UUID4
    user: GetUser
    type: GetType

    class Config:
        from_attributes = True

    