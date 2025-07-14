from uuid import UUID
from sqlalchemy.orm import Session
from models.user import User
from schemas.user_schema import UpdateUser, UserCreate
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

def users(db: Session):
    return db.query(User).all()

def delete(db: Session, user_id: UUID):
    user = get_user_by_id(db, user_id)
    if user is None:
        return None  # Esto evita que intentes eliminar un None
    db.delete(user)
    db.commit()
    return {"message": "Deleted successfully", "id": str(user_id)}

def update_user_repo(db: Session, user_data: UpdateUser):
    user = get_user_by_id(db, user_data.id)
    if not user:
        return None

    user.name = user_data.name
    user.email = user_data.email
    user.role_id = user_data.role_id
    db.commit()
    db.refresh(user)
    return user