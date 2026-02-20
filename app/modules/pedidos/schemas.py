from pydantic import BaseModel
from datetime import datetime

class PedidoItem(BaseModel):
    platillo_id:int
    cantidad:int
    nombre:str
    precio:float
    

class PedidoItemCreate(BaseModel):
    items:list[PedidoItem]
    total:float
    user_id:int

class PedidoMesa(BaseModel):
    items:list[PedidoItem]
    user_id:int
    mesa_id:int
    
class ResponsePedido(BaseModel):
    id:int
    negocio_id:int
    mesa_id:int
    mesero_id:int
    total:float
    estado:str
    created_at:datetime

class DetalleItem(BaseModel):
    id:int
    pedido_id:int
    platillo_id:int
    cantidad:float
    precio_unitario:float
    subtotal:float

class ResponseDetalle(BaseModel):
    items:list[DetalleItem]
    

