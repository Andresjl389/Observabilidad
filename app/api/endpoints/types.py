from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from core.security import get_current_user
from schemas.type_schema import GetType
from services.type_service import get_types
from schemas.user_schema import UserCreate
from core.db import get_db
from sqlalchemy.orm import Session



types_router = APIRouter(
    tags=['Types']
)

@types_router.get("/types", response_model=list[GetType], status_code=200)
async def get_all_types(db: Session = Depends(get_db)):
    try:
        return get_types(db)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
