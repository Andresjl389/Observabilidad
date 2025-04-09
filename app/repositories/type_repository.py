
from fastapi import Request
from sqlalchemy.orm import Session
from models.type_info import Type
from schemas.type_schema import GetType
from models.info import Info
from uuid import UUID



def get(db: Session) -> list[GetType]:
    return db.query(Type).all()


# def create_info(
#     db: Session,
#     type_id: UUID,
#     user_id: UUID,
#     info: InfoBase,
#     filename: str,
#     filepath: str
# ):
#     new_info = Info(
#         title=info.title,
#         description=info.description,
#         icon=info.icon,
#         link=info.link,
#         filename=filename,
#         filepath=filepath,
#         type_id=type_id,
#         user_id=user_id
#     )
#     db.add(new_info)
#     db.commit()
#     db.refresh(new_info)
#     return new_info