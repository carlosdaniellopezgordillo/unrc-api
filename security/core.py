from datetime import datetime, timedelta
from typing import Optional

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from passlib.context import CryptContext
from sqlalchemy.orm import Session

# Importar configuración centralizada
from core.config import SECRET_KEY, ALGORITHM

# Importar modelos y "base de datos" para buscar al usuario
from schemas.models import User
from db.database import get_db, User as DBUser

# --- Configuración de Hashing de Contraseñas ---
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

# --- Mecanismo de Seguridad de FastAPI ---
security = HTTPBearer()

def hash_password(password: str) -> str:
    """Hashea una contraseña en texto plano usando Argon2."""
    # Argon2 no tiene límite de longitud relevante para contraseñas
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Compara una contraseña en texto plano con su versión hasheada usando Argon2."""
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Crea un JSON Web Token (JWT) para la autenticación."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)) -> User:
    """
    Función de dependencia de FastAPI para proteger endpoints.
    1. Extrae el token usando `HTTPBearer`.
    2. Decodifica y valida el token JWT.
    3. Busca al usuario en la base de datos por el email contenido en el token.
    4. Devuelve el objeto de usuario o lanza una excepción si algo falla.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciales inválidas",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Decodificar el token para obtener el "payload" (los datos)
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except (jwt.PyJWTError, jwt.ExpiredSignatureError): # Captura errores de token inválido o expirado
        raise credentials_exception
    
    # Buscar al usuario en la base de datos
    usuario = db.query(DBUser).filter(DBUser.email == email).first()
    if usuario is None:
        raise credentials_exception
        
    return usuario
