from fastapi import APIRouter, Depends
from core.security import get_current_user
from schemas.dashboards_schema import Dates
from core.db import get_db
from sqlalchemy.orm import Session
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
    is_davicom: bool = False,
    data: Dates = Depends(),
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
    ):
    return apdex_metrics(is_davicom,db, data.start_date, data.end_date)

@dash_router.get('/sesiones')
def session(
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
    ):
    response_data = data(db)
    return {'sessions':response_data}

@dash_router.get('/disponibilidad')
def disponibilidad_all_services(
    year: int,
    is_davicom: bool = False,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
    ):
    response = disponibilidad(is_davicom, db, year)
    return response

@dash_router.get('/sesiones-totales')
def total_sessions(
    is_davicom: bool = False,
    data: Dates = Depends(),
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
    ):
    return session_metrics(is_davicom, db, data.start_date, data.end_date)


@dash_router.get('/version-superapp')
def last_versions(
    data: Dates = Depends(),
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
    ):
    return app_version(db, data.start_date, data.end_date)

@dash_router.get('/time-to-login')
def login_ios(
    is_davicom: bool = False,
    data: Dates = Depends(),
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
    ):
    return login_time_by_platform(is_davicom, db, data.start_date, data.end_date)
