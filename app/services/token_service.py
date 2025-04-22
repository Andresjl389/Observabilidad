from uuid import UUID
from fastapi import HTTPException
from sqlalchemy.orm import Session
from schemas.token_schema import TokenBase
from schemas.type_schema import GetType
from repositories.token_repository import get, get_by_id, update

def update_token(token: TokenBase,token_id:UUID, db: Session):
    try:
        existing_token = get_by_id(db, token_id)
        if not existing_token:
            return HTTPException(status_code=404, detail="El token no existe")
        
        for field, value in token.model_dump(exclude_unset=True).items():
            setattr(existing_token, field, value)

        return update(db, existing_token)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al actualizar el token: {str(e)}")


def get_all(db: Session):
    try:
        tokens = get(db)
        return tokens
    except Exception as e:
        raise HTTPException(detail=f"Error al actualizar el token: {str(e)}")