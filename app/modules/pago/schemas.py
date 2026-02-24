from pydantic import BaseModel
from datetime import datetime


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
