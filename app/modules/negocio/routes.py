from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.modules.negocio import crud
from app.modules.negocio.schemas import CreateNegocio, UpdateNegocio, ResponseNegocio
from app.modules.auth.auth import get_current_user
from app.models.user import User


router = APIRouter(prefix="/negocios", tags=["Negocios"])


@router.get("/", response_model=list[ResponseNegocio])
def obtener_negocios(db: Session = Depends(get_db)):
    """Obtener todos los negocios activos"""
    return crud.obtener_negocios(db)


@router.get("/mis-negocios", response_model=list[ResponseNegocio])
def obtener_mis_negocios(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Obtener todos los negocios del usuario actual"""
    return crud.obtener_negocios_owner(db, current_user.id)


@router.post("/", response_model=ResponseNegocio, status_code=201)
def crear_negocio(
    negocio: CreateNegocio,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Crear un nuevo negocio (solo para usuarios con rol owner)"""
    if current_user.role != "owner":
        raise HTTPException(status_code=403, detail="Solo los dueños pueden crear negocios")
    
    return crud.crear_negocio(db, negocio, current_user.id)


@router.get("/{negocio_id}", response_model=ResponseNegocio)
def obtener_negocio(negocio_id: int, db: Session = Depends(get_db)):
    """Obtener detalles de un negocio"""
    return crud.obtener_negocio(db, negocio_id)


@router.put("/{negocio_id}", response_model=ResponseNegocio)
def actualizar_negocio(
    negocio_id: int,
    datos: UpdateNegocio,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Actualizar datos de un negocio"""
    negocio = crud.obtener_negocio(db, negocio_id)
    if negocio.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="No tienes permiso para actualizar este negocio")
    
    return crud.actualizar_negocio(db, negocio_id, datos)


@router.delete("/{negocio_id}", status_code=200)
def desactivar_negocio(
    negocio_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Desactivar un negocio"""
    negocio = crud.obtener_negocio(db, negocio_id)
    if negocio.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="No tienes permiso para desactivar este negocio")
    
    crud.desactivar_negocio(db, negocio_id)
    return {"message": "Negocio desactivado"}
