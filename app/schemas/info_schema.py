from typing import Optional
from pydantic import BaseModel, EmailStr, UUID4

class InfoBase(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    icon: Optional[str] = None
    link: Optional[str] = None

# class GetInfo(InfoBase):
#     id: UUID4
#     class Config:
#         from_attributes = True

class GetInfo(InfoBase):
    id: UUID4
    user_id: UUID4
    type_id: UUID4
    filename: Optional[str] = None
    filepath: Optional[str] = None

    class Config:
        from_attributes = True

    