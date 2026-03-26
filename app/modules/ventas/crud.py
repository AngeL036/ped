from sqlalchemy.orm import Session
from app.models.mesa import Mesa
from app.models.pedido import Pedido
from datetime import datetime, timedelta, timezone
from sqlalchemy import func
from app.models.user import User
from app.models.negocio import Negocio
from app.models.ventas import Venta
from fastapi import HTTPException
from app.modules.ventas.schemes import VentaCreate
from app.models.producto import Producto
from app.models.detalleVenta import DetalleVenta


def venta(db:Session,negoci_id:int,user:User, venta_in:VentaCreate):
    """Registrar una venta"""
    negocio = db.query(Negocio).filter(Negocio.id == negoci_id).first()
    if not negocio:
        raise HTTPException(404,"Negocio no registrado")
    
    nueva_venta = Venta(
        negocio_id = negoci_id,
        vendedor = user.id,
        total = 0
    )
    db.add(nueva_venta)
    db.flush()

    for it in venta_in.items:
        producto = db.query(Producto).filter(Producto.id == it.producto_id).first()
        if not producto:
            raise HTTPException(status_code=404,detail=f"Producto {it.producto_id} no existe")
        precio = it.cantidad * producto.precio_venta
        total = total + precio
        sub_total = it.cantidad * producto.precio_venta
        detalle_venta = DetalleVenta(
            venta_id        = nueva_venta.id,
            producto_id     = it.producto_id,
            cantidad        = it.cantidad,
            precio_unitario = producto.precio_venta,
            sub_total       = sub_total,
        )
        db.add(detalle_venta)
    nueva_venta.total = total
    db.commit()
    db.refresh()
    return {
        "mensaje":"Venta confirmada"
    }
        

def obtener_mesas_ocupadas(db:Session, negocio_id: int):
    """Obtener mesas ocupadas en un negocio"""
    mesas_ocupadas = db.query(Mesa).filter(
        Mesa.negocio_id == negocio_id,
        Mesa.estado == 'ocupado'
    ).count()
    return mesas_ocupadas

def obtener_pedidos_activos(db:Session, negocio_id: int):
    """Obtener pedidos activos en un negocio"""
    pedidos_activos = db.query(Pedido).join(Mesa).filter(
        Mesa.negocio_id == negocio_id,
        Pedido.estado.in_(["pendiente", "en preparación"])
    ).count()
    return pedidos_activos

def  obtener_ventas_totales(db:Session, negocio_id: int,fecha:datetime = None):
    """Obtener ventas totales en un negocio"""
    fecha = fecha or datetime.now(timezone.utc)
    inicio = fecha.replace(hour=0, minute=0, second=0, microsecond=0)
    fin = inicio + timedelta(days=1)
    total = db.query(func.sum(Pedido.total)).join(Mesa).filter(
        Mesa.negocio_id ==negocio_id,
        Pedido.estado == "cerrado",
        Pedido.created_at >= inicio,
        Pedido.created_at < fin
    ).scalar()
    return float(total) if total else 0.0

def obtener_ticket_promedio(db:Session, negocio_id:int):
    """Obtener ticket promedio en un negocio"""
    total_ventas = obtener_ventas_totales(db, negocio_id)
    pedidos_cerrados = db.query(Pedido).join(Mesa).filter(
        Mesa.negocio_id == negocio_id,
        Pedido.estado == "cerrado"
    ).count()
    if pedidos_cerrados == 0:
        return 0.0
    return total_ventas / pedidos_cerrados