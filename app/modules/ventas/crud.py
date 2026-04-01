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
from app.models.pago import Pago
from app.services.Email import enviar_ticket_correo
from app.services.Whatsapp import enviar_ticket_whatsapp
from app.modules.pago.schemas import PagoCreate



def _get_venta_o_404(db:Session, venta_id:int,negocio_id:int) -> Venta:
    v = db.query(Venta).filter(
        Venta.id == venta_id,
        Venta.negocio_id == negocio_id
    ).first()
    if not v:
        raise HTTPException(404,"Venta no encontrada")
    return v

def _detalles_para_ticket(db:Session,venta_id:int) -> list[dict]:
    """Retorna los renglones del ticket listos para email y Whatsapp"""
    detalles = (db.query(DetalleVenta).filter(DetalleVenta.venta_id == venta_id).all())

    resultado = []
    for d in detalles:
        producto = db.query(Producto).filter(Producto.id == d.producto_id).first()
        resultado.append({
            "producto": producto.marca if producto else f"#{d.producto_id}",
            "cantidad": d.cantidad,
            "precio_unitario": float(d.precio_unitario),
            "subtotal": float(d.subtotal),
        })
    return resultado


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
            
        for it in venta_in.items:    
            producto = productos_dict[it.producto_id]
            sub_total = it.cantidad * producto.precio_venta
            total += sub_total
            producto.cantidad_actual -= it.cantidad

            detalle_venta = DetalleVenta(
                venta_id        = nueva_venta.id,
                producto_id     = it.producto_id,
                cantidad        = it.cantidad,
                precio_unitario = producto.precio_venta,
                subtotal       = sub_total,
            )

            db.add(detalle_venta)

        nueva_venta.total = total

        db.commit()
        db.refresh(nueva_venta)

        return {
            "mensaje":"Venta confirmada",
            "venta_id": nueva_venta.id,
            "total": float(total)
        }
    except HTTPException:
        db.rollback()
        raise
    except Exception:
        db.rollback()
        raise 


#---- Registrar pago ----------------------------------------------------------------
def registrar_pago(db:Session, venta_id:int, negocio_id:int, pago_in:PagoCreate):
    """
    Registrar el pago de una venta y calcula el cambio.
    Valida que el monto sea suficiente para cubrir el total de la venta.
    """
    v = _get_venta_o_404(db, venta_id, negocio_id)

    total = float(v.total)
    monto_pagado = float(pago_in.monto_pagado)
    
    if monto_pagado < total:
        raise HTTPException(400, f"El monto pagado es insuficiente. Total: {total:.2f}, Pagado: {monto_pagado:.2f}")
    
    cambio = round(monto_pagado - total, 2)

    pago = Pago(
        venta_id = venta_id,
        monto = monto_pagado,
        cambio = cambio,
        metodo = pago_in.metodo
    )
    db.add(pago)
    db.commit()
    db.refresh(pago)

    return {
        "venta_id": venta_id,
        "total": total,
        "monto_pagado": monto_pagado,
        "cambio": cambio,
        "metodo": pago_in.metodo
    }

#---Enviar Ticket----------------------------------------------------------------

def enviar_ticket_por_correo(db:Session, venta_id:int, negocio_id:int, email:str):
    """Envía el ticket de una venta por correo electrónico"""
    v = _get_venta_o_404(db, venta_id, negocio_id)
    detalles = _detalles_para_ticket(db, venta_id)

    try:
        enviar_ticket_correo(email,venta_id, float(v.total), detalles)
    except Exception as e:
        raise HTTPException(500, f"Error al enviar el correo: {str(e)}")
    

    return {
        "mensaje": f"Ticket enviado a {email}"
    }

def enviar_ticket_por_whatsapp(db:Session, venta_id:int, negocio_id:int, telefono:str):
    """Envía el ticket de una venta por WhatsApp"""
    v = _get_venta_o_404(db, venta_id, negocio_id)
    detalles = _detalles_para_ticket(db, venta_id)

    try:
        enviar_ticket_whatsapp(telefono, venta_id, float(v.total), detalles)
    except Exception as e:
        raise HTTPException(500, f"Error al enviar el mensaje de WhatsApp: {str(e)}")
    
    return {
        "mensaje": f"Ticket enviado a WhatsApp {telefono}"
    }
       
# ── Dashboard ───────────────────────────────────────────────────────────────

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