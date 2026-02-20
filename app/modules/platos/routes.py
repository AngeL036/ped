from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.modules.platos.schemas import CreatePlato,UpdatePlato,ResponsePlato, ResponsePlatos, ActivoUpdate
from app.modules.platos import platos as crud_platos

router = APIRouter( prefix="/platos", tags=["Platos"])

@router.get("/", response_model=list[ResponsePlatos])
def lista_platos(db:Session = Depends(get_db)):
    return crud_platos.get_platos(db)

@router.get("/{plato_id}", response_model=ResponsePlato)
def obtener_plato(plato_id:int, db:Session = Depends(get_db)):
    plato = crud_platos.get_plato(db,plato_id)
    if not plato:
        raise HTTPException(status_code=400, detail="Plano no encontrado")
    return plato

@router.post("/",response_model=ResponsePlato, status_code=201)
def crear_plato(plato: CreatePlato, db:Session = Depends(get_db)):
    return crud_platos.create_plato(db,plato)

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