from uuid import UUID
from fastapi import HTTPException
from sqlalchemy.orm import Session
from repositories.role_repository import get
from schemas.role_schema import RoleEdit


def get_all(db: Session):
    try:
        roles = get(db)
        return roles
    except Exception as e:
        raise HTTPException(detail=f"Error: {str(e)}")