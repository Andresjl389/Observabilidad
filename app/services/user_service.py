from datetime import timedelta
from uuid import UUID
from fastapi import HTTPException, Request, status
import requests
from sqlalchemy.orm import Session
from core.security import check_password_hash, create_access_token
from repositories.user_repository import get_user_by_id, insert_user, get_user_by_email
from schemas.user_schema import GetUser, UserCreate, UserLogin
from google.oauth2 import id_token as google_id_token 
from google.auth.transport import requests as google_requests
import logging
from fastapi import Response
logger = logging.getLogger(__name__)


def create_user(db: Session, user: UserCreate):
    existing_user = get_user_by_email(db, user.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El usuario ya existe"
        )
    return insert_user(db, user)


def login_user(db: Session, user_login: UserLogin, response: Response)  -> GetUser:
    try:
        user = get_user_by_email(db, user_login.email)
        if not user or not check_password_hash(user_login.password, user.password):
            raise HTTPException(status_code=401, detail='Correo o contraseña incorrectos')
        
        token = create_access_token(data={'sub':str(user.id)}, expires_delta=timedelta(minutes=30))
        return {'access_token':token}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")


def get_user(id: UUID, db: Session, request: Request) -> GetUser:
    print('Algo algo',request.cookies.get("access_token"))
    user = get_user_by_id(db, id)
    if not user:
        raise HTTPException(status_code=401, detail='Usuario invalido')
    return user


def google_authenticate(db: Session, id_token: str):
    try:
        # Get Google's public keys to validate the token
        response = requests.get("https://www.googleapis.com/oauth2/v3/certs")
        certs = response.json()

        # Verify the id_token with Google's public keys
        payload = google_id_token.verify_oauth2_token(
            id_token,
            Request(),
            audience="your-client-id.apps.googleusercontent.com"  # Replace with your OAuth 2.0 client ID
        )
    except Exception as e:
        print("Error validating with Google:", e)
        raise HTTPException(status_code=401, detail=f"Invalid token: {e}")

    email = payload.get("email")
    name = payload.get("name")

    if not email:
        raise HTTPException(status_code=400, detail="Email not found in the token")

    user = get_user_by_email(db, email)
    if not user:
        dummy_password = "google_oauth_dummy_password"
        new_user = UserCreate(name=name, email=email, password=dummy_password)
        user = insert_user(db, new_user)

    token = create_access_token(data={"sub": str(user.id)}, expires_delta=timedelta(minutes=30))
    return {"access_token": token, "token_type": "bearer"}