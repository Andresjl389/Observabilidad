from typing import Optional
from pydantic import BaseModel, UUID4

from schemas.user_schema import GetUser

class TokenBase(BaseModel):
    title: Optional[str] = None
    token: str

class GetToken(TokenBase):
    id: UUID4
    user: GetUser