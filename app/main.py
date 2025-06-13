import asyncio
import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from api.endpoints.user import user_router
from api.endpoints.info import info_router
from api.endpoints.types import types_router
from api.endpoints.dashboards import dash_router
from api.endpoints.token import token_router
from api.endpoints.depuration import depuration_router
from fastapi.middleware.cors import CORSMiddleware

from core.data_seeds import run_seeds

UPLOAD_DIR = os.path.abspath("uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

UPLOAD_DIR2 = os.path.abspath("depuration-dynatrace")
os.makedirs(UPLOAD_DIR2, exist_ok=True)

routes = [
    user_router,
    info_router,
    types_router,
    dash_router,
    token_router,
    depuration_router
    ]

app = FastAPI()

run_seeds()

app.mount("/static", StaticFiles(directory=UPLOAD_DIR), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # No uses ["*"] si usas credentials
    #allow_origins=["*"],  # No uses ["*"] si usas credentials
    allow_credentials=True,  # Habilita el envío de cookies/autenticación
    allow_methods=["*"],     # O puedes especificar ["GET", "POST", ...]
    allow_headers=["*"],     # O puedes especificar los headers necesarios
)


@app.get("/")
async def root():
    return {"message": "¡Hola, FastAPI está funcionando!"}


for route in routes:
    app.include_router(route)
