import asyncio
import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from api.endpoints.user import user_router
from api.endpoints.info import info_router
from api.endpoints.types import types_router
from fastapi.middleware.cors import CORSMiddleware

UPLOAD_DIR = os.path.abspath("uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)


routes = [
    user_router,
    info_router,
    types_router
    ]

app = FastAPI()

app.mount("/static", StaticFiles(directory=UPLOAD_DIR), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ⚠️ Puedes restringir a ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "¡Hola, FastAPI está funcionando!"}


for route in routes:
    app.include_router(route)
