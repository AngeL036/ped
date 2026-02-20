from pydantic import BaseModel


class createMesa(BaseModel):
    negocio_id: int
    numero: int
    capacidad: int
    
class ResponseMesa(BaseModel):
    numero : int
    capacidad: int
    estado:str

    class Config:
        from_attributes = True