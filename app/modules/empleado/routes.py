from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.modules.empleado import crud
from app.modules.empleado.schemes import CreateEmpleado, UpdateEmpleado, ResponseEmpleado
from app.modules.auth.auth import get_current_user
from app.models.user import User


router = APIRouter(prefix="/empleados", tags=["Empleados"])


@router.post("/", response_model=ResponseEmpleado, status_code=201)
def crear_empleado(
    empleado: CreateEmpleado,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Crear un nuevo empleado (solo admin o owner)"""
    if current_user.role not in ["admin", "owner"]:
        raise HTTPException(status_code=403, detail="No tienes permisos para crear empleados")
    
    return crud.crear_empleado(db, empleado)


@router.get("/{negocio_id}", response_model=list[ResponseEmpleado])
def obtener_empleados(
    negocio_id: int,
    db: Session = Depends(get_db)
):
    """Obtener todos los empleados de un negocio"""
    return crud.obtener_empleados(db, negocio_id)


@router.get("/detalle/{empleado_id}", response_model=ResponseEmpleado)
def obtener_empleado(
    empleado_id: int,
    db: Session = Depends(get_db)
):
    """Obtener detalles de un empleado específico"""
    return crud.obtener_empleado(db, empleado_id)


@router.put("/{empleado_id}", response_model=ResponseEmpleado)
def actualizar_empleado(
    empleado_id: int,
    datos: UpdateEmpleado,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Actualizar datos de un empleado"""
    if current_user.role not in ["admin", "owner"]:
        raise HTTPException(status_code=403, detail="No tienes permisos")
    
    return crud.actualizar_empleado(db, empleado_id, datos)


@router.delete("/{empleado_id}", status_code=200)
def desactivar_empleado(
    empleado_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Desactivar un empleado"""
    if current_user.role not in ["admin", "owner"]:
        raise HTTPException(status_code=403, detail="No tienes permisos")
    
    crud.desactivar_empleado(db, empleado_id)
    return {"message": "Empleado desactivado"}
