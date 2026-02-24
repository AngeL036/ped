from pydantic import BaseModel
from datetime import datetime


class PedidoItem(BaseModel):
    """Item de un pedido - solo necesita ID y cantidad"""
    platillo_id: int
    cantidad: int


class PedidoItemCreate(BaseModel):
    """Crear pedido con múltiples items"""
    items: list[PedidoItem]
    user_id: int


class PedidoMesa(BaseModel):
    """Crear pedido para una mesa"""
    items: list[PedidoItem]
    mesa_id: int
    

class ResponsePedido(BaseModel):
    """Respuesta de pedido completo"""
    id: int
    negocio_id: int
    mesa_id: int | None
    mesero_id: int | None
    total: float
    estado: str
    created_at: datetime

    class Config:
        from_attributes = True


class DetalleItem(BaseModel):
    """Detalle de un item en un pedido"""
    id: int
    pedido_id: int
    platillo_id: int
    cantidad: float
    precio_unitario: float
    subtotal: float

    class Config:
        from_attributes = True


class PlatilloOut(BaseModel):
    """Platillo saliente en respuestas"""
    id: int
    nombre: str
    precio: float

    class Config:
        from_attributes = True


class DetalleOut(BaseModel):
    """Detalle de pedido con información del platillo"""
    id: int
    cantidad: float
    precio_unitario: float
    platillo: PlatilloOut

    class Config:
        from_attributes = True


