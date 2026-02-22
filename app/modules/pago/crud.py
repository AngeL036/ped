from sqlalchemy.orm import Session
from app.models.pedido import Pedido
from app.models.pago import Pago
from sqlalchemy import func
from fastapi import HTTPException


def registrar_pago(db: Session, pedido_id: int, metodo: str, monto: float):
    """Registrar un pago para un pedido"""
    pedido = db.query(Pedido).get(pedido_id)

    if not pedido:
        raise HTTPException(404, "Pedido no existe")

    pago = Pago(
        pedido_id=pedido_id,
        metodo=metodo,
        monto=monto
    )

    db.add(pago)
    db.commit()

    total_pagado = (
        db.query(func.sum(Pago.monto))
        .filter(Pago.pedido_id == pedido_id)
        .scalar() or 0
    )

    if total_pagado >= pedido.total:
        pedido.estado = "cerrado"
        db.commit()

    return {
        "total": pedido.total,
        "pagado": total_pagado,
        "faltante": max(pedido.total - total_pagado, 0)
    }


def obtener_pagos_pedido(db: Session, pedido_id: int):
    """Obtener todos los pagos de un pedido"""
    pagos = db.query(Pago).filter(Pago.pedido_id == pedido_id).all()
    if not pagos:
        raise HTTPException(404, "No hay pagos registrados para este pedido")
    return pagos


def obtener_pago(db: Session, pago_id: int):
    """Obtener un pago específico"""
    pago = db.query(Pago).filter(Pago.id == pago_id).first()
    if not pago:
        raise HTTPException(404, "Pago no encontrado")
    return pago


def obtener_resumen_pedido(db: Session, pedido_id: int):
    """Obtener resumen de pagos de un pedido"""
    pedido = db.query(Pedido).get(pedido_id)
    if not pedido:
        raise HTTPException(404, "Pedido no existe")

    total_pagado = (
        db.query(func.sum(Pago.monto))
        .filter(Pago.pedido_id == pedido_id)
        .scalar() or 0
    )

    return {
        "pedido_id": pedido_id,
        "total": float(pedido.total),
        "pagado": float(total_pagado),
        "faltante": float(max(pedido.total - total_pagado, 0)),
        "estado": pedido.estado
    }
