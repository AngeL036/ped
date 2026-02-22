from pydantic import BaseModel


class createMesa(BaseModel):
    negocio_id: int
    numero: int
    capacidad: int


class UpdateMesa(BaseModel):
    numero: int | None = None
    capacidad: int | None = None
    

class ResponseMesa(BaseModel):
    id: int
    numero: int
    capacidad: int
    estado: str

    class Config:
        orm_mode = True
