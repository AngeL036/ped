from fastapi import APIRouter, Depends, HTTPException
from requests import Session
from app.core.roles import require_roles, Roles
from app.models.user import User
from app.dependencies import get_db
from app.modules.pago.schemas import PagoCreateProducto, PagoResponseProducto
from app.modules.ticket.schemas import TicketCorreoRequest, TicketWhatsAppRequest
from app.modules.ventas import crud
from app.modules.ventas.schemes import VentaCreate



router = APIRouter(prefix="/ventas", tags=["Ventas"])

_ROL_CAJA = Depends(require_roles(Roles.ADMIN, Roles.OWNER, Roles.CAJA, Roles.VENDEDOR))
_ROL_ADMIN = Depends(require_roles(Roles.ADMIN, Roles.OWNER))


@router.post("/")
def crear_venta(
    item_in:VentaCreate,
    db:Session = Depends(get_db),
    current_user: User = _ROL_CAJA,
    
):
    """Crea la venta y descuento stock. Retorna venta_id y total."""
    return crud.venta(db,current_user.negocio_id,current_user,item_in)

#--- POST /ventas/{venta_id}/pago-------------------------

@router.post("/{venta_id}/pago", response_model=PagoResponseProducto)
def registrar_pago(
    venta_id: int,
    pago_in: PagoCreateProducto,
    db:Session = Depends(get_db),
    current_user: User = _ROL_CAJA,
):
    """
    Registra el pago de una venta.
    Valida que el monto_pagado >= total y devuelve el cambio.
    """
    return crud.registrar_pago(db, venta_id, current_user.negocio_id, pago_in)

#-----POST /ventas/{venta_id}/ticket/correo-----------------------------
@router.post("/{venta_id}/ticket/correo")
def enviar_ticket_por_correo(
    venta_id: int,
    body: TicketCorreoRequest,
    db:Session = Depends(get_db),
    current_user: User = _ROL_CAJA,
):
    """
    Envia el ticket de la venta al correo del cliente.
    """
    return crud.enviar_ticket_por_correo(db, venta_id, current_user.negocio_id, body.correo)
#------POST /ventas/{venta_id}/ticket/whatsapp-----------------------------
@router.post("/{venta_id}/ticket/whatsapp")
def enviar_ticket_por_whatsapp(
    venta_id: int,
    body: TicketWhatsAppRequest,
    db:Session = Depends(get_db),
    current_user: User = _ROL_CAJA,
):
    """
    Envia el ticket de la venta al numero de whatsapp del cliente.
    """
    return crud.enviar_ticket_por_whatsapp(db, venta_id, current_user.negocio_id, body.numero)



#-----POST /ventas/obtener-datos-----------------------------
@router.get("/obtener-datos")
def obtener_mesas_ocupadas(
    db: Session = Depends(get_db),
    current_user: User = _ROL_ADMIN
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