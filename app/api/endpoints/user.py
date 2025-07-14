from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Request, Response
from core.security import get_current_user
from schemas.user_schema import GetUser, Token, UpdateUser, UserCreate, UserLogin
from core.db import get_db
from sqlalchemy.orm import Session
from services.user_service import create_user, delete_user, get_all_users, get_user, login_user, update_user


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
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db),
    ):
    return get_user(current_user, db)


@user_router.get('/all-users', response_model=list[GetUser])
def get_users(
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db),
    ):
    return get_all_users(db)

@user_router.delete('/user/{user_id}')
def delete(
    user_id: UUID,
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db),
    ):
    return delete_user(current_user, user_id, db)

@user_router.put('/user', response_model=GetUser)
def update_user_endpoint(
    user: UpdateUser,
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return update_user(current_user, user, db)