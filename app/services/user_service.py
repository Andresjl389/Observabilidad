from datetime import timedelta
from uuid import UUID
from fastapi import HTTPException
from sqlalchemy.orm import Session
from core.security import check_password_hash, create_access_token
from repositories.user_repository import get_user_by_id, insert_user, get_user_by_email
from schemas.user_schema import GetUser, UserCreate, UserLogin

def create_user(db: Session, user: UserCreate):
    existing_user = get_user_by_email(db, user.email)
    if existing_user:
        raise ValueError("El usuario ya existe")
    return insert_user(db, user)


def login_user(db: Session, user_login: UserLogin):
    user = get_user_by_email(db, user_login.email)
    if not user or not check_password_hash(user_login.password, user.password):
        raise HTTPException(status_code=401, detail='Correo o contraseña incorrectos')
    
    token = create_access_token(data={'sub':str(user.id)}, expires_delta=timedelta(minutes=30))
    return {'access_token':token, 'token_type':'bearer'}

def get_user(id: UUID, db: Session) -> GetUser:
    user = get_user_by_id(db, id)
    if not user:
        raise HTTPException(status_code=401, detail='Usuario invalido')
    return user
