from pydantic import BaseModel, EmailStr
from typing import Literal
from pydantic import field_validator


class TicketEnvioRequest(BaseModel):
    medio: Literal["correo", "whatsapp", "otro"]
    valor: str  # el correo o el número de teléfono
 
    @field_validator("valor")
    @classmethod
    def validar_valor(cls, v: str, info) -> str:
        v = v.strip()
        if not v:
            raise ValueError("El valor no puede estar vacío")
        return v
 