from pydantic import BaseModel
from decimal import Decimal


class BasePlato(BaseModel):
    nombre: str
    precio: Decimal
    descripcion:str

class CreatePlato(BaseModel):
    nombre: str
    precio: Decimal
    descripcion:str
    categoria_id:int

class UpdatePlato(BaseModel):
    nombre: str | None = None
    precio: Decimal | None = None
    descripcion: str | None = None
    cantidad: int | None = None
    categoria_id: int | None = None

class ResponsePlato(BaseModel):
    id:int
    categoria_id:int
    nombre:str
    precio:Decimal
    descripcion:str
    activo:bool
    class Config:
        from_attributes = True

class ResponsePlatos(BaseModel):
    id:int
    categoria_id:int
    nombre:str
    precio:Decimal
    descripcion:str
    
    activo:bool
    class Config:
        from_attributes = True

class ActivoUpdate(BaseModel):
    activo:bool