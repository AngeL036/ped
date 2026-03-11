from pydantic import BaseModel, ConfigDict
from datetime import datetime
from decimal import Decimal


class Transactions(BaseModel):
    id:int
    fecha: datetime
    cliente:str
    monto:float
    estado:str
    metodo:str

    model_config = ConfigDict(from_attributes=True)