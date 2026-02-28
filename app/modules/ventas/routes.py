from fastapi import APIRouter, Depends, HTTPException
from requests import Session
from app.core.roles import require_roles, Roles
from app.models.user import User
from app.dependencies import get_db
from app.modules.ventas import crud


router = APIRouter(prefix="/ventas", tags=["Ventas"])

@router.get("/obtener-datos")
def obtener_mesas_ocupadas(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(Roles.ADMIN, Roles.OWNER))
):
    """Obtener mesas ocupadas en el negocio del usuario actual"""
    mesasOcupadas = crud.obtener_mesas_ocupadas(db, current_user.negocio_id)
    pedidosActivos = crud.obtener_pedidos_activos(db, current_user.negocio_id)
    ventasTotales = crud.obtener_ventas_totales(db, current_user.negocio_id)
    ticketPromedio = crud.obtener_ticket_promedio(db, current_user.negocio_id)
    
    return {
        "mesas_ocupadas": mesasOcupadas,
        "pedidos_activos": pedidosActivos,
        "ventas_totales": ventasTotales,
        "ticket_promedio": ticketPromedio
    }