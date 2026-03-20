from pydantic import BaseModel, Field, model_validator
from typing import Optional
from datetime import datetime


# ─── Base ───────────────────────────────────────────────
class ProductoBase(BaseModel):
    nombre:       str         = Field(..., min_length=1, max_length=100)
    unidad:       str         = Field(..., examples=["pieza", "kg", "lt", "caja"])
    codigo:       Optional[str] = Field(None, max_length=30)
    categoria_id: Optional[int] = None
    stock_minimo: int         = Field(default=3, ge=0)
    activo:       bool        = True


# ─── Crear producto ─────────────────────────────────────
class ProductoCreate(ProductoBase):
    pass  # solo datos del producto, precios van en inventario


# ─── Editar producto ─────────────────────────────────────
class ProductoUpdate(BaseModel):
    nombre:       Optional[str] = Field(None, min_length=1, max_length=100)
    unidad:       Optional[str] = None
    codigo:       Optional[str] = Field(None, max_length=30)
    categoria_id: Optional[int] = None
    stock_minimo: Optional[int] = Field(None, ge=0)
    activo:       Optional[bool] = None


# ─── Respuesta ───────────────────────────────────────────
class ProductoResponse(ProductoBase):
    id:              int
    negocio_id:      int
    cantidad_actual: int
    precio_compra:   Optional[float] = None   # viene del último inventario
    precio_venta:    Optional[float] = None
    estado_stock:    Optional[str]   = None   # ✅ OK / 🔸 BAJO / ⚠️ REPONER
    created_at:      datetime

    model_config = {"from_attributes": True}