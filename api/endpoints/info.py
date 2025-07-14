from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, Form, Query, File, Request, UploadFile
from fastapi.staticfiles import StaticFiles
from core.security import get_current_user
from schemas.info_schema import GetInfo, GetVideo, InfoBase
from services.info_service import create, delete_service, get, get_all_videos, get_by_filter, get_id, update_service
from core.db import get_db
from sqlalchemy.orm import Session


info_router = APIRouter(
    tags=['Info']
)

info_router.mount("/static", StaticFiles(directory="uploads"), name="static")


@info_router.get("/info-by", response_model=List[GetInfo], status_code=200, )
def get_info(
    type_id: UUID,
    request: Request,  # Agregar request para generar la URL de la imagen
    user_id: Optional[UUID] = Query(None, description="Filter by user ID"),
    db: Session = Depends(get_db),
):
    return get_by_filter(
            db=db, user_id=user_id,
            type_id=type_id,
            request=request
            )


@info_router.post("/info", status_code=201)
def create_info(
    type_id: UUID = Form(...),
    current_user: str = Depends(get_current_user),
    title: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    icon: Optional[str] = Form(None),
    link: Optional[str] = Form(None),
    file: UploadFile = File(None),
    db: Session = Depends(get_db),
):
    info = InfoBase(
        title=title,
        description=description,
        icon=icon,
        link=link
    )
    return create(db, type_id, current_user, info, file)

@info_router.get("/info/{info_id}", status_code=200, response_model=GetInfo)
def get_info_by_id(
    info_id: UUID,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    return get_id(db, info_id)

@info_router.get("/info", status_code=200, response_model=List[GetInfo])
def get_all(
    request: Request,
    db: Session = Depends(get_db),
):
    return get(request,db)

@info_router.get("/info-videos", status_code=200, response_model=List[GetVideo])
def get_videos(
    request: Request,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user) 
):
    return get_all_videos(request, db)

@info_router.delete("/info/{info_id}", status_code=200)
def delete_by_id(
    info_id: UUID,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user) 
):
    return delete_service(db, info_id)

@info_router.put('/info/{info_id}', status_code=200)
def update_info(
    info_id: UUID,
    type_id: UUID = Form(None),
    title: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    icon: Optional[str] = Form(None),
    link: Optional[str] = Form(None),
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    info = InfoBase(
        title=title,
        description=description,
        icon=icon,
        link=link
    )
    return update_service(db, info_id, current_user, type_id, info)


