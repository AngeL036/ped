from fastapi import Depends,APIRouter 
from app.core.roles import require_roles, Roles
from app.models.user import User
from app.modules.caja.schemas import Caja
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.modules.caja import crud
from app.modules.caja.schemas import AbrirCaja

router = APIRouter(prefix="/caja", tags=["cajas"])



@router.get("/cajaActiva")
def caja_activa(db:Session = Depends(get_db), current_user: User = Depends(require_roles(Roles.ADMIN, Roles.OWNER, Roles.CAJA))):
    return crud.obtener_caja_activa(db,current_user)

@router.post("/abrirCaja")
def abrir_caja(
    body:AbrirCaja,
    db:Session = Depends(get_db),
    current_user: User = Depends(require_roles(Roles.ADMIN, Roles.OWNER, Roles.CAJA))
    ):
    return crud.abrir_caja(db,current_user,body.monto_inicial)

