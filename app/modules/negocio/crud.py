from sqlalchemy.orm import Session
from app.models.negocio import Negocio
from app.models.user import User
from app.modules.negocio.schemas import CreateNegocio, UpdateNegocio
from fastapi import HTTPException


def crear_negocio(db: Session, negocio_data: CreateNegocio, owner_id: int):
    """Crear un nuevo negocio"""
    owner = db.query(User).filter(User.id == owner_id).first()
    if not owner:
        raise HTTPException(status_code=404, detail="Usuario propietario no encontrado")
    
    nuevo_negocio = Negocio(
        owner_id=owner_id,
        nombre=negocio_data.nombre,
        direccion=negocio_data.direccion,
        telefono=negocio_data.telefono,
        activo=True
    )
    
    db.add(nuevo_negocio)
    db.commit()
    db.refresh(nuevo_negocio)
    return nuevo_negocio


def obtener_negocios(db: Session):
    """Obtener todos los negocios activos"""
    return db.query(Negocio).filter(Negocio.activo == True).all()


def obtener_negocio(db: Session, negocio_id: int):
    """Obtener un negocio por ID"""
    negocio = db.query(Negocio).filter(Negocio.id == negocio_id).first()
    if not negocio:
        raise HTTPException(status_code=404, detail="Negocio no encontrado")
    return negocio


def obtener_negocios_owner(db: Session, owner_id: int):
    """Obtener todos los negocios de un propietario"""
    negocios = db.query(Negocio).filter(
        Negocio.owner_id == owner_id,
        Negocio.activo == True
    ).all()
    return negocios


def actualizar_negocio(db: Session, negocio_id: int, datos: UpdateNegocio):
    """Actualizar datos de un negocio"""
    negocio = db.query(Negocio).filter(Negocio.id == negocio_id).first()
    if not negocio:
        raise HTTPException(status_code=404, detail="Negocio no encontrado")
    
    if datos.nombre:
        negocio.nombre = datos.nombre
    if datos.direccion:
        negocio.direccion = datos.direccion
    if datos.telefono:
        negocio.telefono = datos.telefono
    
    db.commit()
    db.refresh(negocio)
    return negocio


def desactivar_negocio(db: Session, negocio_id: int):
    """Desactivar un negocio"""
    negocio = db.query(Negocio).filter(Negocio.id == negocio_id).first()
    if not negocio:
        raise HTTPException(status_code=404, detail="Negocio no encontrado")
    
    negocio.activo = False
    db.commit()
    db.refresh(negocio)
    return negocio
