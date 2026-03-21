from pydantic import BaseModel, Field, model_validator
from typing import Optional
from datetime import datetime
from app.modules.producto.schemas import ProductoCreate, ProductoResponse

# ─── Primer conteo / ajuste manual ──────────────────────
class InventarioCreate(BaseModel):
    producto_id:  int
    cantidad:     int   = Field(..., ge=0)
    motivo:       Optional[str] = Field(None, examples=["conteo inicial", "ajuste manual"])


class InventarioResponse(BaseModel):
    id:          int
    producto_id: int
    cantidad:    int
    motivo:      Optional[str]
    created_at:  datetime

    model_config = {"from_attributes": True}


# ─── Registrar precios (va junto al primer inventario) ──
class PreciosCreate(BaseModel):
    precio_compra: float = Field(..., gt=0)
    precio_venta:  float = Field(..., gt=0)

    @model_validator(mode="after")
    def venta_mayor_que_compra(self):
        if self.precio_venta <= self.precio_compra:
            raise ValueError("El precio de venta debe ser mayor al de compra")
        return self


# ─── Payload completo: producto + precios + stock inicial ─
class ProductoInicialCreate(BaseModel):
    producto:  ProductoCreate     # noqa: F821 — importado en el router
    precios:   PreciosCreate
    inventario: InventarioCreate


# ─── Respuesta combinada ─────────────────────────────────
class ProductoInicialResponse(BaseModel):
    producto:  ProductoResponse  # noqa: F821
    inventario: InventarioResponse

    model_config = {"from_attributes": True}