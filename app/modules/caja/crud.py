from app.models.user import User
from sqlalchemy.orm import Session
from app.models.corteCaja import CorteCaja
from fastapi import HTTPException
from sqlalchemy import func
from app.models.ventas import Venta
from datetime import datetime, timezone



def abrir_caja(db:Session,user:User, monto_inicial:float):
    caja_abierta = db.query(CorteCaja)\
    .filter(CorteCaja.usuario_id == user.id)\
    .filter(CorteCaja.estado == "abierto")\
    .filter(CorteCaja.negocio_id == user.negocio_id)\
    .first() 

    if caja_abierta:
        raise HTTPException(400, "Ya tienes una caja abierta")
    
    nueva = CorteCaja(
        negocio_id = user.negocio_id,
        usuario_id = user.id,
        monto_inicial = monto_inicial
    )

    db.add(nueva)
    db.commit()
    db.refresh(nueva)

    return nueva


def obtener_caja_activa(db:Session, user:User):
    return db.query(CorteCaja)\
    .filter(CorteCaja.usuario_id == user.id)\
    .filter(CorteCaja.estado == "abierto")\
    .first()

def cerrar_caja(db:Session, user:User, monto_final:float):
    
    caja = obtener_caja_activa(db,user)
    if not caja:
        raise HTTPException(404, "No hay caja abierta")
    
    total_ventas = db.query(func.sum(Venta.total))\
        .filter(Venta.vendedor ==user.id)\
        .filter(Venta.created_at >= caja.fecha_apertura)\
        .scalar() or 0
    
    caja.fecha_cierre = datetime.now(timezone.utc)
    caja.monto_final = monto_final
    caja.total_sistema = total_ventas

    esperado = caja.monto_inicial + total_ventas
    caja.diferencia = monto_final - esperado

    caja.estado = "cerrado"

    db.commit()
    db.refresh(caja)

    return {
        "mensaje":      "caja cerrada",
        "total_ventas": total_ventas,
        "esperado":     esperado,
        "diferencia":   caja.diferencia
    }