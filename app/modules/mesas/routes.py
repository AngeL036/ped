from fastapi import APIRouter,Depends, HTTPException
from app.modules.mesas import crud
from app.modules.mesas.schemas import ResponseMesa,createMesa
from app.dependencies import get_db
from sqlalchemy.orm import Session


router = APIRouter(prefix="/mesas", tags=["Mesas"])

@router.get("/", response_model=list[ResponseMesa])
def list_mesas(db:Session = Depends(get_db)):
    return crud.get_mesas(db)

@router.get("/{mesa_id}", response_model=ResponseMesa)
def obtener_mesa(mesa_id:int, db:Session = Depends(get_db)):
    mesa = crud.get_mesa(db,mesa_id)
    if not mesa:
        raise HTTPException(status_code=400, detail="Mesa no encontrado")
    return mesa

@router.post("/",response_model=ResponseMesa, status_code=201)
def crear_mesa(mesa:createMesa, db:Session = Depends(get_db)):
    return crud.create_mesa(db,mesa)
