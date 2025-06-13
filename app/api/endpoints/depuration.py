from fastapi import APIRouter, Depends, File, UploadFile
from fastapi.staticfiles import StaticFiles
from services.depuration_service import depuration_users
from core.security import get_current_user
from schemas.dashboards_schema import Dates
from core.db import get_db
from sqlalchemy.orm import Session


depuration_router = APIRouter(
    tags=['Depuration']
)

depuration_router.mount("/depuration-dynatrace", StaticFiles(directory="depuration-dynatrace"), name="depuration")

@depuration_router.post('/depuration')
def depuration(
    file: UploadFile = File(None),
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
    ):
    return depuration_users(file)
