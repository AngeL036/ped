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


def venta(db:Session,negocio_id:int,user:User, venta_in:VentaCreate):
    """Registrar una venta"""
    try:
        if not venta_in.items:
            raise HTTPException(400,"La venta no tiene productos")
        
        negocio = db.query(Negocio).filter(Negocio.id == negocio_id).first()
        if not negocio:
            raise HTTPException(404,"Negocio no registrado")
    
        nueva_venta = Venta(
            negocio_id = negocio_id,
            vendedor = user.id,
            total = 0
        )
        db.add(nueva_venta)
        db.flush()
        productos_ids = [it.producto_id for it in venta_in.items]

        productos = db.query(Producto)\
        .filter(Producto.id.in_(productos_ids))\
        .with_for_update()\
        .all()

        productos_dict = {p.id: p for p in productos}

        total = 0
        for it in venta_in.items:
            producto = productos_dict.get(it.producto_id)

            if not producto:
                raise HTTPException(status_code=404,detail=f"Producto {it.producto_id} no existe")
            
            if (producto.cantidad_actual < it.cantidad):
                raise HTTPException(status_code=409, detail="Stock induficiente")
            
            sub_total = it.cantidad * producto.precio_venta
            total += sub_total
            producto.cantidad_actual -= it.cantidad

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
        db.refresh(nueva_venta)

        return {
            "mensaje":"Venta confirmada",
            "venta_id": nueva_venta.id
        }
    except HTTPException:
        db.rollback()
        raise
    except Exception:
        db.rollback()
        raise HTTPException(500, "Error al procesar la venta")
        

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