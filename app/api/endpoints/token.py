from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from services.token_service import get_all, update_token
from schemas.token_schema import GetToken, TokenBase
from core.db import get_db
from sqlalchemy.orm import Session


token_router = APIRouter(
    tags=['Token']
)


@token_router.put('/token/{token_id}')
def add_token(
    token: TokenBase,
    token_id: UUID,
    db: Session = Depends(get_db)
):
    return update_token(token, token_id, db)


@token_router.get('/token',response_model=list[GetToken])
def get_tokens(db: Session = Depends(get_db)):
    return get_all(db)