from sqlalchemy.orm import Session
from app.models.empleado import Empleado
from app.models.user import User
from app.modules.empleado.schemes import CreateEmpleado, UpdateEmpleado
from fastapi import HTTPException
from app.modules.empleado.schemes import ResponseEmpleado
from app.modules.auth import crud_user


def crear_empleado(db: Session, empleado_data: CreateEmpleado, current_user: User):
    """Crear un nuevo empleado"""
    user, temporal_password = crud_user.crear_usuario_empleado(db, email=empleado_data.email, role=empleado_data.rol)
    user_verify = db.query(User).filter(User.email == empleado_data.email).first()
    if not user_verify:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    existe_empleado = db.query(Empleado).filter(
        Empleado.user_id == user.id
    ).first()
    if existe_empleado:
        raise HTTPException(status_code=400, detail="Este usuario ya es un empleado")
    
    nuevo_empleado = Empleado(
        nombre = empleado_data.nombre,
        apellido = empleado_data.apellido,
        edad = empleado_data.edad,
        user_id=user.id,
        negocio_id=current_user.negocio_id,
        rol=empleado_data.rol,
        activo=True
    )
    
    db.add(nuevo_empleado)
    db.commit()
    db.refresh(nuevo_empleado)
   
    return {
        "message": "Empleado creado con exito",
        "empleado": nuevo_empleado,
        "temporal_password": temporal_password
    }


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
