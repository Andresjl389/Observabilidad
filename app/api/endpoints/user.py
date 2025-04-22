from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from core.security import get_current_user
from schemas.user_schema import GetUser, Token, UserCreate, UserLogin
from core.db import get_db
from sqlalchemy.orm import Session
from services.user_service import create_user, get_user, login_user


user_router = APIRouter(
    prefix='/auth',
    tags=['Auth']
)


@user_router.post("/register", response_model=UserCreate, status_code=201)
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        return await create_user(db, user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@user_router.post('/login', response_model=Token)
def login(user: UserLogin, db: Session = Depends(get_db)):
    return login_user(db, user)


@user_router.get('/user', response_model=GetUser)
def get(
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
    ):
    return get_user(current_user, db)