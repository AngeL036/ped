from fastapi import Depends,APIRouter 
from app.core.roles import require_roles, Roles
from app.models.user import User
from app.modules.caja.schemas import Caja
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.modules.caja import crud


router = APIRouter(prefix="/caja", tags=["cajas"])


@router.get("/", response_model=Caja)
def lista_cajas(db:Session = Depends(get_db), current_user: User  = Depends(require_roles(Roles.ADMIN, Roles.OWNER))):
    return crud.obtener_caja_activa(db,current_user)


