from sqlalchemy.orm import Session
from repositories.user_repository import insert_user, get_user_by_email
from schemas.user_schema import UserCreate

def create_user(db: Session, user: UserCreate):
    existing_user = get_user_by_email(db, user.email)
    if existing_user:
        raise ValueError("El usuario ya existe")
    return insert_user(db, user)
