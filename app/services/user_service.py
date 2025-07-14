from datetime import timedelta
from uuid import UUID
from fastapi import HTTPException, Request, status
from sqlalchemy.orm import Session
from core.security import check_password_hash, create_access_token
from repositories.user_repository import delete, get_user_by_id, insert_user, get_user_by_email, update_user_repo, users
from schemas.user_schema import GetUser, UpdateUser, UserCreate, UserLogin
import logging
from fastapi import Response
logger = logging.getLogger(__name__)

ADMIN_ROLE_ID = UUID("864c38b2-4a35-40a1-84d4-39af5a18b3bc")


def create_user(db: Session, user: UserCreate):
    existing_user = get_user_by_email(db, user.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El usuario ya existe"
        )
    return insert_user(db, user)


def login_user(db: Session, user_login: UserLogin, response: Response)  -> GetUser:
    try:
        user = get_user_by_email(db, user_login.email)
        if not user or not check_password_hash(user_login.password, user.password):
            raise HTTPException(status_code=401, detail='Correo o contraseña incorrectos')
        
        token = create_access_token(data={'sub':str(user.id)}, expires_delta=timedelta(minutes=30))
        return {'access_token':token}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")


def get_user(id: UUID, db: Session) -> GetUser:
    user = get_user_by_id(db, id)
    if not user:
        raise HTTPException(status_code=401, detail='Usuario invalido')
    return user

def get_all_users(db: Session):
    return users(db)

def delete_user(current_user_id: UUID, user_id: UUID, db: Session):
    try:
        current_user = get_user_by_id(db, current_user_id)
        if not current_user or current_user.role.id != ADMIN_ROLE_ID:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to delete users."
            )

        deleted_info = delete(db, user_id)
        if not deleted_info:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        return {
            "message": "Deleted successfully",
            "id": str(user_id)
        }

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting user: {str(e)}"
        )
        

def update_user(current_user_id: UUID, user_data: UpdateUser, db: Session):
    current_user = get_user_by_id(db, current_user_id)

    if not current_user or current_user.role.id != ADMIN_ROLE_ID:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para actualizar usuarios."
        )

    updated_user = update_user_repo(db, user_data)
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado."
        )
    
    return updated_user
