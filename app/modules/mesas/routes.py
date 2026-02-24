from fastapi import APIRouter,Depends, HTTPException
from app.modules.auth.auth import get_current_user
from app.modules.mesas import crud
from app.modules.mesas.schemas import ResponseMesa, createMesa, UpdateMesa
from app.dependencies import get_db
from sqlalchemy.orm import Session


router = APIRouter(prefix="/mesas", tags=["Mesas"])


@router.get("/", response_model=list[ResponseMesa])
def list_mesas(db:Session = Depends(get_db), current_user = Depends(get_current_user)):
    """Obtener todas las mesas"""
    negocio_id = current_user.negocio_id
    if negocio_id is None:
        raise HTTPException(status_code=403, detail="Usuario no asociado a ningún negocio")
    return crud.get_mesas(db, negocio_id)


@router.get("/{mesa_id}", response_model=ResponseMesa)
def obtener_mesa(mesa_id:int, db:Session = Depends(get_db), current_user = Depends(get_current_user)):
    """Obtener una mesa específica"""
    negocio_id = current_user.negocio_id
    if negocio_id is None:
        raise HTTPException(status_code=403, detail="Usuario no asociado a ningún negocio")
    return crud.get_mesa(db, mesa_id, negocio_id)


@router.post("/",response_model=ResponseMesa, status_code=201)
def crear_mesa(mesa:createMesa, db:Session = Depends(get_db)):
    """Crear una nueva mesa"""
    return crud.create_mesa(db, mesa)


@router.put("/{mesa_id}", response_model=ResponseMesa)
def actualizar_mesa(
    mesa_id: int,
    datos: UpdateMesa,
    db:Session = Depends(get_db)
):
    """Actualizar datos de una mesa"""
    return crud.update_mesa(db, mesa_id, datos)


@router.delete("/{mesa_id}", status_code=200)
def eliminar_mesa(mesa_id:int, db:Session = Depends(get_db)):
    """Eliminar una mesa"""
    return crud.delete_mesa(db, mesa_id)

