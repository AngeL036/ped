from fastapi import Depends, HTTPException, status
from app.modules.auth.auth import get_current_user

# Enum de roles permitidos
class Roles:
    OWNER = "owner"
    ADMIN = "admin"
    MESERO = "mesero"
    COCINA = "cocina"
    CAJA = "caja"
    # Agrega más roles si es necesario


def require_roles(*roles):
    def dependency(current_user=Depends(get_current_user)):
        if current_user.role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"No tienes permisos. Roles requeridos: {roles}"
            )
        return current_user
    return dependency
