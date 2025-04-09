from fastapi import HTTPException
from sqlalchemy.orm import Session
from repositories.type_repository import get
from schemas.type_schema import GetType

def get_types(db: Session)  -> list[GetType]:
    try:
        return get(db)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error fetching types: {str(e)}")
