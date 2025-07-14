from fastapi import Request
from sqlalchemy.orm import Session
from schemas.token_schema import TokenBase
from schemas.info_schema import GetInfo, InfoBase
from models.token import Token
from uuid import UUID
    

def get_by_id(db: Session, token_id: UUID):
    return db.query(Token).filter(Token.id == token_id).first()

def update(db: Session, db_token: Token):
    db.commit()
    db.refresh(db_token)
    return db_token


def get(db: Session):
    return db.query(Token).all()