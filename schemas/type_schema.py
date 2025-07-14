from typing import Optional
from pydantic import BaseModel, UUID4

class TypeBase(BaseModel):
    name: str

class GetType(TypeBase):
    id: UUID4

    class Config:
        from_attributes = True