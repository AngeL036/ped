from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from app.core.security import decode_access_token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_negocio_id(
        token: str = Depends(oauth2_scheme),
) -> int:
    payload = decode_access_token(token)
    negocio_id = payload.get("negocio_id")
    if not negocio_id:
        raise HTTPException(status_code=400, detail="Token sin negocio activo")
    return int(negocio_id)