from sqlalchemy import func
from sqlalchemy.orm import Session
from app.models.mesa import Mesa
from app.modules.mesas.schemas import createMesa, UpdateMesa
from fastapi import HTTPException


def get_mesas(db:Session,negocio_id:int):
    """Obtener todas las mesas"""
    return db.query(Mesa).filter(Mesa.negocio_id == negocio_id).all()


def get_mesa(db:Session, mesa_id:int,negocio_id:int):
    """Obtener una mesa por ID"""
    mesa = db.query(Mesa).filter(Mesa.id == mesa_id, Mesa.negocio_id == negocio_id).first()
    if not mesa:
        raise HTTPException(status_code=404, detail="Mesa no encontrada")
    return mesa


def create_mesa(db:Session, negocio_id:int):
    """Crear una nueva mesa"""
    ultima_mesa = db.query(func.max(Mesa.numero)).filter(
        Mesa.negocio_id == negocio_id).scalar()
    nueva_mesa = Mesa (
        negocio_id = negocio_id,
        numero = ultima_mesa + 1 if ultima_mesa else 1,
        capacidad = 4,
    )
    db.add(nueva_mesa)
    db.commit()
    db.refresh(nueva_mesa)
    return nueva_mesa


def update_mesa(db:Session, mesa_id:int, datos:UpdateMesa):
    """Actualizar datos de una mesa"""
    mesa = db.query(Mesa).filter(Mesa.id == mesa_id).first()
    if not mesa:
        raise HTTPException(status_code=404, detail="Mesa no encontrada")
    
    if datos.numero is not None:
        mesa.numero = datos.numero
    if datos.capacidad is not None:
        mesa.capacidad = datos.capacidad
    
    db.commit()
    db.refresh(mesa)
    return mesa


def delete_mesa(db:Session, mesa_id:int):
    """Eliminar una mesa"""
    mesa = db.query(Mesa).filter(Mesa.id == mesa_id).first()
    if not mesa:
        raise HTTPException(status_code=404, detail="Mesa no encontrada")
    
    db.delete(mesa)
    db.commit()
    return {"message": "Mesa eliminada correctamente"}
