from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.models.movimientoInventario import TipoMovimiento, MotivoMovimiento


class MovimientoCreate(BaseModel):
    producto_id: int
    tipo:        TipoMovimiento
    cantidad:    int            = Field(..., gt=0)
    motivo:      Optional[MotivoMovimiento] = None


class MovimientoResponse(BaseModel):
    id:          int
    producto_id: int
    tipo:        TipoMovimiento
    cantidad:    int
    motivo:      Optional[MotivoMovimiento]
    created_at:  datetime

    model_config = {"from_attributes": True}