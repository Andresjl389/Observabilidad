from uuid import UUID
from sqlalchemy.orm import Session
from models.user import User
from schemas.user_schema import UserCreate
from core.security import get_password_hash


async def insert_user(db: Session, user: UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = User(
        name = user.name,
        email = user.email,
        password = hashed_password,
        role_id = 'b64bcee3-1bee-468e-9825-39a7a77112bc'
        )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def get_user_by_id(db: Session, id: UUID):
    return db.query(User).filter(User.id == id).first()