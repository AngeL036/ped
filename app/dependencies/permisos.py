# app/dependencies/permisos.py
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.negocio import Negocio


def get_negocio_activo(
    negocio_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Negocio:
    negocio = db.query(Negocio).filter(
        Negocio.id == negocio_id,
        Negocio.activo == True
    ).first()
    if not negocio:
        raise HTTPException(status_code=404, detail="Negocio no encontrado")
    return negocio


def require_owner_or_admin(
    negocio: Negocio = Depends(get_negocio_activo),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> User:
    if negocio.owner_id == current_user.id:
        return current_user

    from app.models.empleado import Empleado
    empleado = db.query(Empleado).filter(
        Empleado.user_id    == current_user.id,
        Empleado.negocio_id == negocio.id,
        Empleado.rol        == "admin",
        Empleado.activo     == True,
    ).first()
    if not empleado:
        raise HTTPException(status_code=403, detail="No tienes permiso para esta acción")

    return current_user