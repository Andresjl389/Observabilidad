from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from core.security import get_current_user
from schemas.dashboards_schema import Dates, DynatraceResponse
from core.db import get_db
from sqlalchemy.orm import Session
from datetime import date, datetime
from services.dashboards_service import (
    data,
    apdex_metrics,
    app_version,
    disponibilidad,
    login_time_by_platform,
    session_metrics
    )


dash_router = APIRouter(
    tags=['Dash']
)
    

@dash_router.get('/apdex-metrics')
def apdex_web_superapp(
    data: Dates = Depends(),
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
    ):
    return apdex_metrics(db, data.start_date, data.end_date)

@dash_router.get('/sesiones')
def session(
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
    ):
    response_data = data(db)
    return {'sessions':response_data}

@dash_router.get('/disponibilidad')
def disponibilidad_all_services(
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
    ):
    response = disponibilidad(db)
    return response

@dash_router.get('/sesiones-totales')
def total_sessions(
    data: Dates = Depends(),
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
    ):
    return session_metrics(db, data.start_date, data.end_date)


@dash_router.get('/version-superapp')
def last_versions(
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
    ):
    return app_version(db)

@dash_router.get('/time-to-login')
def login_ios(
    data: Dates = Depends(),
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
    ):
    return login_time_by_platform(db, data.start_date, data.end_date)
