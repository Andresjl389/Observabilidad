from uuid import UUID
from fastapi import APIRouter, Depends
from schemas.role_schema import RoleEdit
from services.role_service import get_all
from core.security import get_current_user
from schemas.token_schema import GetToken, TokenBase
from core.db import get_db
from sqlalchemy.orm import Session


role_router = APIRouter(
    tags=['Role']
)


@role_router.get('/roles', response_model=list[RoleEdit])
def get_tokens(
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
    ):
    return get_all(db)
