from pydantic import BaseModel, EmailStr
from pydantic import field_validator




class TicketCorreoRequest(BaseModel):
    correo: EmailStr

class TicketWhatsAppRequest(BaseModel):
    numero: str

    @field_validator("numero")
    @classmethod
    def validar_numero(cls, v:str):
        limpio = v.replace(" ", "").replace("-", "")
        if not limpio.startswith("+"):
            raise ValueError("El numero debe incluir codigo de pais, ej: +52...")
        if len(limpio) < 10:
            raise ValueError("El numero es demasiado corto")
        return limpio