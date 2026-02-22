from fastapi import Depends, APIRouter, HTTPException
from app.dependencies import get_db
from sqlalchemy.orm import Session
from app.modules.pago import crud
from app.modules.pago.schemas import PagoCreate, PagoResponse, ResumenPago

router = APIRouter(prefix="/pagos", tags=["Pagos"])


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
