from typing import Optional
from pydantic import BaseModel, UUID4

class TokenBase(BaseModel):
    title: Optional[str] = None
    token: str

class GetToken(TokenBase):
    id: UUID4
    user_id: UUID4