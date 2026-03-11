from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException
from app.models.pago import Pago
from app.models.pedido import Pedido
from app.models.user import User
from datetime import datetime, timezone, timedelta
from app.modules.reportes.schemas import Transactions

OFFSET = timedelta(hours=-6)

def obtener_transaction(db:Session, negocio_id:int, fecha:datetime):
    """obtener datos de las transacciones """
    inicio = fecha.replace(hour=0, minute=0,second=0,microsecond=0)
    fin = inicio + timedelta(days=1)
    pedidos = (
        db.query(Pedido)
        .options(
            joinedload(Pedido.pagos),
            joinedload(Pedido.mesa),
            )
        .filter(
            Pedido.negocio_id == negocio_id,
            Pedido.created_at >= inicio,
            Pedido.created_at < fin
            )
        .order_by(Pedido.created_at.desc())
        .limit(10)
        .all()
        )
    return [
        Transactions(
            id=p.id,
            fecha=p.created_at,
            cliente=f"Mesa {p.mesa.numero}" if p.mesa else "Sin mesa",
            monto=float(p.total or 0),
            estado=p.estado,
            metodo=p.pagos[0].metodo if p.pagos else "Sin pago",
        )
        for p in pedidos
    ]