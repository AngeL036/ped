from fastapi import Depends, APIRouter, HTTPException
from app.modules.auth.auth import get_current_user
from app.core.roles import require_roles, Roles
from app.dependencies import get_db
from sqlalchemy.orm import Session
from app.models.user import User
from app.modules.pago import crud
from app.modules.pago.schemas import PagoCreate, PagoResponse, ResumenPago, pagoPedido

router = APIRouter(prefix="/pagos", tags=["Pagos"])


@router.post("/cerrar", response_model=dict)
def pagar_mesa(
    data: pagoPedido,
    current_user: User = Depends(require_roles(Roles.ADMIN, Roles.OWNER, Roles.MESERO )),
    db: Session = Depends(get_db)
):
    """Registrar un pago para el pedido activo de una mesa"""
    negocio_id = current_user.negocio_id
    if negocio_id is None:
        raise HTTPException(status_code=403, detail="Usuario no asociado a ningún negocio")
    return crud.pagar_pedido(db, data.metodo, data.monto, data.mesa_id, negocio_id)

@router.post("/pedido/{pedido_id}/pagar", response_model=dict)
def pagar(pedido_id: int, data: PagoCreate, db: Session = Depends(get_db)):
    """Registrar un nuevo pago para un pedido"""
    return crud.registrar_pago(db, pedido_id, data.metodo, data.monto)


@router.get("/pedido/{pedido_id}/listado", response_model=list[PagoResponse])
def obtener_pagos_pedido(pedido_id: int, db: Session = Depends(get_db)):
    """Obtener todos los pagos de un pedido"""
    return crud.obtener_pagos_pedido(db, pedido_id)


@router.get("/id/{pago_id}", response_model=PagoResponse)
def obtener_pago(pago_id: int, db: Session = Depends(get_db)):
    """Obtener detalles de un pago específico"""
    return crud.obtener_pago(db, pago_id)


@router.get("/pedido/{pedido_id}/resumen", response_model=ResumenPago)
def obtener_resumen_pedido(pedido_id: int, db: Session = Depends(get_db)):
    """Obtener resumen de pagos de un pedido"""
    return crud.obtener_resumen_pedido(db, pedido_id)
