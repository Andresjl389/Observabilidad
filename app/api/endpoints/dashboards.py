from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from core.security import get_current_user
from schemas.dashboards_schema import DynatraceResponse
from services.dashboards_service import adpex, data, disponibilidad
from core.db import get_db
from sqlalchemy.orm import Session


dash_router = APIRouter(
    tags=['Dash']
)

@dash_router.get('/apdex')
def apdex(db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    response_data = adpex(db)
    try:
        parsed = DynatraceResponse(**response_data)
        if not parsed.result or not parsed.result[0].data or not parsed.result[0].data[0].values:
            return JSONResponse(
                status_code=204,
                content={"message": "No se encontraron datos de Apdex en la respuesta."}
            )

        values = parsed.result[0].data[0].values
        return {"values": values}

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


@dash_router.get('/sesiones')
def session(db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    response_data = data(db)
    return {'sessions':response_data}


@dash_router.get('/disponibilidad')
def disponibilidad_all_services(db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    response = disponibilidad(db)
    return JSONResponse(content=jsonable_encoder({'message':response}))

