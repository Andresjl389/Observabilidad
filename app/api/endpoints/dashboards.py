from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, Form, Query, File, Request, UploadFile
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from schemas.dashboards_schema import DynatraceResponse
from services.dashboards_service import adpex, create_token, data, disponibilidad, query
from core.db import get_db
from sqlalchemy.orm import Session


dash_router = APIRouter(
    tags=['Dash']
)

@dash_router.get('/apdex')
def apdex(db: Session = Depends(get_db)):
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
def session(db: Session = Depends(get_db)):
    response_data = data(db)
    return {'sessions':response_data}


@dash_router.get('/disponibilidad')
def disponibilidad_all_services(db: Session = Depends(get_db)):
    response = disponibilidad(db)
    return JSONResponse(content=jsonable_encoder({'message':response}))

