from fastapi import APIRouter, Depends, HTTPException, Request, Response
import requests
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from repositories.user_repository import get_user_by_email, insert_user
from core.security import create_access_token, get_current_user
from schemas.user_schema import GetUser, Token, UserCreate, UserLogin
from core.db import get_db
from sqlalchemy.orm import Session
from services.user_service import create_user, get_user, google_authenticate, login_user


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


@user_router.post('/login')
def login(user: UserLogin, response: Response, db: Session = Depends(get_db)):
    return login_user(db, user, response)


@user_router.get('/user', response_model=GetUser)
def get(
    request: Request,
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db),
    ):
    return get_user(current_user, db, request)


@user_router.post("/google-login", response_model=Token)
async def google_login(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    id_token = data.get("idToken")

    if not id_token:
        raise HTTPException(status_code=400, detail="ID token requerido")

    return google_authenticate(db, id_token)