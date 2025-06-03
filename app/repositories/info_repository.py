from fastapi import Request
from sqlalchemy.orm import Session
from schemas.info_schema import GetInfo, InfoBase
from models.info import Info
from uuid import UUID



def get_by_user_type(db: Session, type_id: UUID, request: Request, user_id: UUID = None) -> list[GetInfo]:
    query = db.query(Info).filter(Info.type_id == type_id)
    if user_id is not None:
        query = query.filter(Info.user_id == user_id)
    
    info_list = query.all()
    
    # Construir la URL completa para la imagen
    for info in info_list:
        if info.filename:
            info.filepath = f"{request.base_url}static/{info.filename}"  # Ahora la URL debe funcionar
    
    return info_list

def get_by_id(db: Session, info_id: UUID):
    return db.query(Info).filter(Info.id == info_id).first()
def get_all(request: Request, db: Session):
    info_list =  db.query(Info).all()


    for info in info_list:
        if info.filename:
            info.filepath = f"{request.base_url}static/{info.filename}"  # Ahora la URL debe funcionar
    
    return info_list
    


def create_info(
    db: Session,
    type_id: UUID,
    user_id: UUID,
    info: InfoBase,
    filename: str,
    filepath: str
):
    new_info = Info(
        title=info.title,
        description=info.description,
        icon=info.icon,
        link=info.link,
        filename=filename,
        filepath=filepath,
        type_id=type_id,
        user_id=user_id
    )
    db.add(new_info)
    db.commit()
    db.refresh(new_info)
    return new_info