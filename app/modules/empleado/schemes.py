from pydantic import BaseModel
from datetime import datetime


class CreateEmpleado(BaseModel):
    nombre: str
    apellido:str
    edad: int
    email: str 
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
    create_at: datetime

    class Config:
        from_attributes = True


class ResponseEmpleadoCreacion(BaseModel):
    message: str
    empleado: ResponseEmpleado
    temporal_password: str

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