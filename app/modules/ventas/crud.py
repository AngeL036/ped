from sqlalchemy.orm import Session
from app.models.mesa import Mesa
from app.models.pedido import Pedido
from datetime import datetime, timedelta, timezone
from sqlalchemy import func

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