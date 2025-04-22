import bcrypt
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
from jose import JWTError, jwt

from schemas.user_schema import UserLogin

# Configuración del JWT
SECRET_KEY = 'Algo_muy_muy_secreto'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Esquema de autenticación
auth_scheme = HTTPBearer()

# Generar hash de contraseña
def get_password_hash(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    print("Password:", password)
    print("Salt:", salt)
    print("Hashed password:", hashed_password)
    return hashed_password.decode('utf-8')

# Verificar hash de contraseña
def check_password_hash(password, hashed_password):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

# Crear token JWT
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    
    print("Tiempo actual:", datetime.utcnow())
    print("Expira en:", expire)
    print("Exp timestamp:", int(expire.timestamp()))

    to_encode.update({
        'exp': expire,
    })

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Decodificar token JWT
def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print('Decode payload:', payload)
        return payload
    except JWTError as e:
        print("Excepción al decodificar token:", e)
        raise HTTPException(
            status_code=401,
            detail=f"Token inválido o expirado: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )

# Obtener el usuario actual desde el token
def get_current_user(token: str = Depends(auth_scheme)):
    print("Token recibido:", token)
    jwt_token = token.credentials
    print("Token JWT:", jwt_token)
    
    payload = decode_access_token(jwt_token)
    print("Payload decodificado:", payload)

    username = payload.get('sub')
    if not username:
        raise HTTPException(status_code=401, detail='Token inválido: no contiene el campo "sub"')
    
    return username
