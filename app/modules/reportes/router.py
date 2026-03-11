from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.modules.reportes.schemas import Transactions
from app.modules.auth.auth import get_current_user
from app.core.roles import require_roles, Roles
from app.models.user import User
from app.modules.reportes import crud
from datetime import datetime,timezone

router = APIRouter(prefix="/reportes", tags=["Reportes"])

@router.get("/transaction", response_model=list[Transactions])
def obtener_transaction(
    db:Session = Depends(get_db),
    current_user: User = Depends(require_roles(Roles.ADMIN, Roles.OWNER))
):
    """Obtener las ultimas transacciones del dia"""
    hoy = datetime.now(timezone.utc)
    return crud.obtener_transaction(db,current_user.negocio_id, hoy)