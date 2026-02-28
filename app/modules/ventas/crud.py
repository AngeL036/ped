from sqlalchemy.orm import Session
from app.models.mesa import Mesa
from app.models.pedido import Pedido
from app.models.user import User


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

def obtener_ventas_totales(db:Session, negocio_id: int):
    """Obtener ventas totales en un negocio"""
    total_ventas = db.query(Pedido).join(Mesa).filter(
        Mesa.negocio_id == negocio_id,
        Pedido.estado == "cerrado"
    ).scalar() or 0.0
    return total_ventas

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