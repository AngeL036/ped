from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.config import settings
from app.dependencies import get_db
from app.models.user import User


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def create_access_token(data:dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.jwt_expire_minutes)
    to_encode.update({"exp":expire})
    return jwt.encode(to_encode,settings.jwt_secret_key, algorithm=settings.jwt_algorithm)

def decode_access_token(token:str) -> dict:
    try:
        payload = jwt.decode(token, settings.jwt_secret_key,algorithm=[settings.jwt_algorithm])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalido o expirado",
            headers={"WWW-Authenticate": "Baerer"}
        )
    
def get_current_user(
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_db)
) -> User:
    payload = decode_access_token(token)
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Token sin subject")
    user = db.query(User).filter(User.id == int(user_id)).first()
    if not user:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")
    return user