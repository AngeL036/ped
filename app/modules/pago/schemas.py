from pydantic import BaseModel, field_validator
from datetime import datetime
from decimal import Decimal
from typing import Literal

class PagoCreate(BaseModel):
    metodo: str
    monto: float

    class Config:
        json_schema_extra = {
            "example": {"metodo": "efectivo", "monto": 10.50}
        }


class PagoResponse(BaseModel):
    id: int
    pedido_id: int
    metodo: str
    monto: float
    fecha: datetime

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "pedido_id": 1,
                "metodo": "efectivo",
                "monto": 10.50,
                "fecha": "2025-02-21T10:30:00"
            }
        }


class ResumenPago(BaseModel):
    pedido_id: int
    total: float
    pagado: float
    faltante: float
    estado: str

    class Config:
        json_schema_extra = {
            "example": {
                "pedido_id": 1,
                "total": 100.00,
                "pagado": 50.00,
                "faltante": 50.00,
                "estado": "abierto"
            }
        }

class pagoPedido(BaseModel):
    metodo: str
    mesa_id: int
    monto: float


#--productos-----------------------
class PagoCreateProducto(BaseModel):
    monto_pagado: Decimal
    metodo: Literal["efectivo", "tarjeta", "transferencia"] = "efectivo"

    @field_validator("monto_pagado")
    @classmethod
    def monto_positivo(cls, v: Decimal):
        if v <= 0:
            raise ValueError("El monto pagado debe ser mayor a 0")
        return v
    
def PagoResponseProducto(BaseModel):
    venta_id: int
    total : Decimal
    monto_pagado: Decimal
    cambio: Decimal
    metodo: str
    model_config = {"from_attributes": True}