from pydantic import BaseModel



class Caja(BaseModel):
    usuario_id: str
    fecha_apertura : str
    fecha_cierre: str
    monto_inicial: float
    monto_final : float
    diferencia: float
    total_sistema:float
    estado:str