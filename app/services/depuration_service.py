import os
import shutil
from fastapi import File, HTTPException, UploadFile
from fastapi.responses import JSONResponse
import requests
import csv
import time
from sqlalchemy.orm import Session

from repositories.token_repository import get_by_id


UPLOAD_DIR = os.path.join(os.getcwd(), "depuration-dynatrace")
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Variables globales para cachear el token
_token_cache = {
    "access_token": None,
    "expires_at": 0  # Timestamp en segundos
}

def read_users(filepath: str):
    with open(filepath, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        return list(reader)

def validate_file(file: UploadFile):
    try:
        if not file.filename.endswith(".csv"):
            raise ValueError("El archivo debe ser CSV")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error validando el archivo: {str(e)}")

def get_token(db: Session):
    current_time = time.time()
    token = get_by_id(db, 'c052574a-9e1f-46cf-9d6e-6f87d2138c23')
    
    if _token_cache["access_token"] and current_time < _token_cache["expires_at"]:
        return _token_cache["access_token"]

    url = 'https://sso.dynatrace.com/sso/oauth2/token'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'client_id' : 'dt0s02.IT2TODD2',
        'grant_type': 'client_credentials',
        'client_secret': f'{token.token}',
        'resource': 'urn:dtaccount:5d8555d6-ac2e-4fca-82dd-d32e718916c4'
    }

    response = requests.post(url, headers=headers, data=data)
    if response.status_code != 200:
        raise Exception(f"Error obteniendo token: {response.status_code} - {response.text}")

    token = response.json()['access_token']
    _token_cache["access_token"] = token
    _token_cache["expires_at"] = current_time + 300  # 5 minutos

    print('Token generado')
    return token

def depuration_users(db: Session, user_file: UploadFile = None):
    validate_file(user_file)
    file_path = os.path.join(UPLOAD_DIR, user_file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(user_file.file, buffer)

    users = read_users(file_path)
    eliminados = []
    errores = []

    for count, row in enumerate(users, start=1):
        user_email = row['usuarios'].strip()
        print(f'{count} Usuario a eliminar {user_email}')

        try:
            account_id = '5d8555d6-ac2e-4fca-82dd-d32e718916c4'
            token = get_token(db)
            url = f'https://api.dynatrace.com/iam/v1/accounts/{account_id}/users/{user_email}'
            headers = {
                'Authorization': f'Bearer {token}'
            }

            response = requests.delete(url, headers=headers)

            if response.status_code == 204:
                eliminados.append(user_email)
            else:
                errores.append({
                    "email": user_email,
                    "status_code": response.status_code,
                    "message": response.text
                })

        except Exception as e:
            errores.append({
                "email": user_email,
                "error": str(e)
            })

    return JSONResponse(content={
        "mensaje": "Depuración finalizada",
    })