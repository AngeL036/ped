from fastapi import APIRouter, Depends, HTTPException
from app.modules.inventario.schemas import ProductoInicialResponse, ProductoInicialCreate
from app.dependencies import get_db
from sqlalchemy.orm import Session
from app.models.user import User
from app.dependencies.permisos import require_owner_or_admin
from app.modules.producto import crud


router = APIRouter(prefix="/negocios/{negocio_id}/productos", tags=["Productos"])

@router.post("/inicial", response_model=ProductoInicialResponse, status_code=201)
def crear_producto_inicial(
    negocio_id: int,
    payload: ProductoInicialCreate,
    db: Session = Depends(get_db),
    user: User = Depends(require_owner_or_admin)
):
    return crud.create_product(db,payload,negocio_id,user.negocio_id)