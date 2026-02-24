from pydantic import BaseModel
from datetime import datetime


class CreateNegocio(BaseModel):
    nombre: str
    direccion: str | None = None
    telefono: str | None = None


class UpdateNegocio(BaseModel):
    nombre: str | None = None
    direccion: str | None = None
    telefono: str | None = None


class ResponseNegocio(BaseModel):
    id: int
    owner_id: int
    nombre: str
    direccion: str | None
    telefono: str | None
    activo: bool
    created_at: datetime

    class Config:
        from_attributes = True


class NegocioCondetalles(BaseModel):
    id: int
    owner_id: int
    nombre: str
    direccion: str | None
    telefono: str | None
    activo: bool
    created_at: datetime
    empleados_count: int | None = None
    mesas_count: int | None = None

    class Config:
        from_attributes = True
