from fastapi import APIRouter, Depends, HTTPException
from app.modules.inventario.schemas import ProductoInicialResponse, ProductoInicialCreate
from app.dependencies import get_db
from sqlalchemy.orm import Session
from app.models.user import User
from app.dependencies.permisos import require_owner_or_admin
from app.modules.producto import crud
from app.modules.producto.schemas import ProductoResponse


router = APIRouter(prefix="/productos", tags=["Productos"])

@router.post("/inicial", response_model=ProductoInicialResponse, status_code=201)
def crear_producto_inicial(
    payload: ProductoInicialCreate,
    db: Session = Depends(get_db),
    user: User = Depends(require_owner_or_admin)
):
    return crud.create_product(db,payload,user.negocio_id)

@router.get("/", response_model=list[ProductoResponse])
def list_product(
    db: Session = Depends(get_db),
    current_user : User = Depends(require_owner_or_admin)
):
    return crud.list_product(db,current_user.negocio_id)