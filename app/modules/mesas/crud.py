from sqlalchemy.orm import Session
from app.models.mesa import Mesa
from app.modules.mesas.schemas import createMesa

def get_mesas(db:Session):
    return db.query(Mesa).all()

def get_mesa(db:Session, mesa_id:int):
    return db.query(Mesa).filter(Mesa.id == mesa_id).first()

def create_mesa(db:Session,mesa:createMesa):
    nueva_mesa = Mesa (
        negocio_id = mesa.negocio_id,
        numero =mesa.numero,
        capacidad = mesa.capacidad,
    )
    db.add(nueva_mesa)
    db.commit()
    db.refresh(nueva_mesa)
    return nueva_mesa