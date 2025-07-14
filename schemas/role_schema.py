from typing import Optional
from pydantic import BaseModel, UUID4

class RoleBase(BaseModel):
    name: str
    
class RoleEdit(RoleBase):
    id: UUID4