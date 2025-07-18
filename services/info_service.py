import os
import shutil
from uuid import UUID
from fastapi import HTTPException, Request, UploadFile
from sqlalchemy.orm import Session
from schemas.info_schema import GetInfo, InfoBase
from repositories.info_repository import delete, get_all, get_by_id, get_by_user_type, create_info, get_videos, update_info
from schemas.user_schema import UserCreate
from repositories.type_repository import get as get_type

UPLOAD_DIR = os.path.join(os.getcwd(), "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True) 

def get_by_filter(db: Session, type_id: UUID,request: Request, user_id: UUID = None)  -> list[GetInfo]:
    try:
        return get_by_user_type(db=db, user_id=user_id, type_id=type_id, request=request)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error fetching info: {str(e)}")


def validate_image(file: UploadFile):
    try:
        if not file.filename.endswith((".jpg", ".jpeg", ".png")):
            raise ValueError("El archivo debe ser una imagen (JPG, JPEG o PNG)")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error validando el archivo: {str(e)}")


def create(
    db: Session,
    type_id: UUID,
    user_id: UUID,
    info: InfoBase,
    file: UploadFile = None  # Asegurar que puede ser None
):
    if file:
        validate_image(file)  # Validar solo si hay archivo
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        filename = file.filename
        filepath = f"/static/{file.filename}"
    else:
        filename = None
        filepath = None

    return create_info(
        db=db,
        user_id=user_id,
        type_id=type_id,
        info=info,
        filename=filename,
        filepath=filepath
    )



def get_id(db: Session, info_id: UUID):
    try:
        info = get_by_id(db, info_id)
        if not info:
            raise ValueError("Info no encontrada")
        return info
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error fetching info: {str(e)}")

def get(request:Request, db: Session):
    try:
        info = get_all(request, db)
        if not info:
            raise ValueError("Info no encontrada")
        return info
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error fetching info: {str(e)}")

def get_all_videos(request: Request, db: Session):
    try:
        videos = get_videos(db, request)
        if not videos:
            raise ValueError("No se encontraron videos")
        return videos
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error fetching videos: {str(e)}")
    

def delete_service(db: Session, info_id: UUID):
    try:
        deleted_info = delete(db, info_id)
        if not deleted_info:
            raise HTTPException(status_code=404, detail="Info not found")
        return {"message": "Deleted successfully", "id": str(info_id)}
    except HTTPException as http_exc:
        raise http_exc  # Re-raise si ya es una HTTPException como 404
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error deleting info: {str(e)}")
    
    
def update_service(
    db: Session,
    info_id: UUID,
    user_id: UUID,
    type_id: UUID,
    info: InfoBase,
):
    try:
        existing_info = get_by_id(db, info_id)
        if not existing_info:
            raise HTTPException(status_code=404, detail="Info not found")

        filename = existing_info.filename
        filepath = existing_info.filepath

        updated_info = update_info(
            db=db,
            info_id=info_id,
            info=info,
            type_id=type_id,
            filename=filename,
            filepath=filepath
        )
        return updated_info
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error updating info: {str(e)}")