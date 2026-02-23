from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.modules.platos.schemas import CreatePlato,UpdatePlato,ResponsePlato, ResponsePlatos, ActivoUpdate
from app.modules.platos import platos as crud_platos
from app.models.user import User
from app.modules.auth.auth import get_current_user

router = APIRouter( prefix="/platos", tags=["Platos"])

@router.get("/", response_model=list[ResponsePlatos])
def lista_platos(db:Session = Depends(get_db)):
    return crud_platos.get_platos(db)

@router.get("/activos", response_model=list[ResponsePlatos])
def lista_platos_activos(db:Session = Depends(get_db)):
    return crud_platos.get_platos_activos(db)

@router.get("/{plato_id}", response_model=ResponsePlato)
def obtener_plato(plato_id:int, db:Session = Depends(get_db)):
    plato = crud_platos.get_plato(db,plato_id)
    if not plato:
        raise HTTPException(status_code=400, detail="Plato no encontrado")
    return plato

@router.post("/",response_model=ResponsePlato, status_code=201)
def crear_plato(
    plato: CreatePlato,
    db:Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not current_user.empleado:
        raise HTTPException(status_code=403, detail="Solo los empleados pueden crear platos")
    
    negocio_id = current_user.empleado.negocio_id
    return crud_platos.create_plato(db, plato, negocio_id)

@router.put("/{plato_id}", response_model=ResponsePlato)
def actualizar_plato(
    plato_id: int,
    datos: UpdatePlato,
    db: Session = Depends(get_db)
):
    plato = crud_platos.get_plato(db, plato_id)
    if not plato:
        raise HTTPException(status_code=404, detail="Plato no encontrado")

    return crud_platos.update_plato(db, plato, datos)

@router.delete("/{plato_id}", status_code=204)
def eliminar_plato(plato_id: int, db: Session = Depends(get_db)):
    plato = crud_platos.get_plato(db, plato_id)
    if not plato:
        raise HTTPException(status_code=404, detail="Plato no encontrado")

    crud_platos.delete_plato(db, plato)

@router.patch("/{id}/activo")
def cambiar_activo(id:int, data:ActivoUpdate, db:Session = Depends(get_db)):
    plato = crud_platos.patch_activo(db,id, data.activo)

    if not plato:
        raise HTTPException(status_code=404, detail="Plato no encontrado")
    
    return {"ok":True}

@router.get("/{plato_id}/negocio",response_model=ResponsePlato)
def obtener_plato_negocio(
    plato_id:int,
    db:Session = Depends(get_db),
    current_user: User =Depends(get_current_user)
):
    plato = crud_platos.get_plato_negocio_mesa(db,plato_id,current_user)
    if not plato:
        raise HTTPException(404, "Plato no encontrado")
    return plato