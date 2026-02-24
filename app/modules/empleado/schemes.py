from pydantic import BaseModel
from datetime import datetime


class CreateEmpleado(BaseModel):
    user_id: int
    negocio_id: int
    rol: str  # mesero, cocina, caja, admin


class UpdateEmpleado(BaseModel):
    rol: str | None = None
    activo: bool | None = None


class ResponseEmpleado(BaseModel):
    id: int
    user_id: int
    negocio_id: int
    rol: str
    activo: bool

    class Config:
        from_attributes = True


class EmpleadoConUsuario(BaseModel):
    id: int
    user_id: int
    negocio_id: int
    rol: str
    activo: bool
    user: dict

    class Config:
        from_attributes = True