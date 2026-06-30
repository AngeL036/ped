from pydantic import BaseModel, Field



class Caja(BaseModel):
    usuario_id: str
    fecha_apertura : str
    fecha_cierre: str
    monto_inicial: float
    monto_final : float
    diferencia: float
    total_sistema:float
    estado:str

class AbrirCaja(BaseModel):
    monto_inicial:float

class CerrarCaja(BaseModel):
    monto_final: float = Field(...,ge=0)