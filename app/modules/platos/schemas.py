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

class UpdatePlato(BaseModel):
    nombre: str | None = None
    precio: Decimal | None = None
    descripcion: str | None = None
    cantidad: int | None = None

class ResponsePlato(BaseModel):
    id:int
    nombre:str
    precio:Decimal
    descripcion:str
    activo:bool
    class Config:
        orm_mode = True

class ResponsePlatos(BaseModel):
    id:int
    nombre:str
    precio:Decimal
    descripcion:str
    
    activo:bool
    class Config:
        orm_mode = True

class ActivoUpdate(BaseModel):
    activo:bool