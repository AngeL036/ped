# ============================================================
# ARCHIVO NUEVO: app/modules/categorias/router.py
# ============================================================

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.modules.auth.auth import get_current_user
from app.core.roles import require_roles, Roles
from app.models.user import User
from . import crud
from .schemas import CategoriaCreate, CategoriaResponse

router = APIRouter(prefix="/categorias", tags=["Categorias"])

@router.get("/", response_model=list[CategoriaResponse])
def listar_categorias(
    current_user: User = Depends(require_roles(Roles.OWNER, Roles.ADMIN, Roles.MESERO)),
    db: Session = Depends(get_db),
):
    return crud.get_categorias(db, current_user.negocio_id)

@router.post("/", response_model=CategoriaResponse, status_code=201)
def crear_categoria(
    data: CategoriaCreate,
    current_user: User = Depends(require_roles(Roles.OWNER, Roles.ADMIN)),
    db: Session = Depends(get_db),
):
    return crud.create_categoria(db, current_user.negocio_id, data.nombre)