from fastapi import Request
from sqlalchemy.orm import Session
from models.role import Role
from uuid import UUID
    

def get_by_id(db: Session, token_id: UUID):
    return db.query(Role).filter(Role.id == token_id).first()

def get(db: Session):
    return db.query(Role).all()