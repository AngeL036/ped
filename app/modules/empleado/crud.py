from sqlalchemy.orm import Session
from app.models.empleado import Empleado
from app.models.user import User
from app.modules.empleado.schemes import CreateEmpleado, UpdateEmpleado
from fastapi import HTTPException


def crear_empleado(db: Session, empleado_data: CreateEmpleado):
    """Crear un nuevo empleado"""
    user = db.query(User).filter(User.id == empleado_data.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    existe_empleado = db.query(Empleado).filter(
        Empleado.user_id == empleado_data.user_id
    ).first()
    if existe_empleado:
        raise HTTPException(status_code=400, detail="Este usuario ya es un empleado")
    
    nuevo_empleado = Empleado(
        user_id=empleado_data.user_id,
        negocio_id=empleado_data.negocio_id,
        rol=empleado_data.rol,
        activo=True
    )
    
    db.add(nuevo_empleado)
    db.commit()
    db.refresh(nuevo_empleado)
    return nuevo_empleado


def obtener_empleados(db: Session, negocio_id: int):
    """Obtener todos los empleados de un negocio"""
    return db.query(Empleado).filter(
        Empleado.negocio_id == negocio_id,
        Empleado.activo == True
    ).all()


def obtener_empleado(db: Session, empleado_id: int):
    """Obtener un empleado por ID"""
    empleado = db.query(Empleado).filter(Empleado.id == empleado_id).first()
    if not empleado:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")
    return empleado


def actualizar_empleado(db: Session, empleado_id: int, datos: UpdateEmpleado):
    """Actualizar datos de un empleado"""
    empleado = db.query(Empleado).filter(Empleado.id == empleado_id).first()
    if not empleado:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")
    
    if datos.rol:
        empleado.rol = datos.rol
    if datos.activo is not None:
        empleado.activo = datos.activo
    
    db.commit()
    db.refresh(empleado)
    return empleado


def desactivar_empleado(db: Session, empleado_id: int):
    """Desactivar un empleado"""
    empleado = db.query(Empleado).filter(Empleado.id == empleado_id).first()
    if not empleado:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")
    
    empleado.activo = False
    db.commit()
    db.refresh(empleado)
    return empleado
