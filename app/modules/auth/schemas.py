from pydantic import BaseModel,EmailStr, field_validator
from datetime import datetime
import re
class CreateUser(BaseModel):
    email:EmailStr
    password:str
    role:str = "owner"  # Default role

    @field_validator("password")
    @classmethod
    def validar_password(cls, v:str) -> str:
        if len(v) < 8:
            raise ValueError("La contraseña debe tener al menos 8 caracteres")
        if not re.search(r"[a-zA-Z]", v):
            raise ValueError("La contraseña debe contener al menos una letra")
        if not re.search(r"\d", v):
            raise ValueError("La contraseña debe contener al menos un número")
        if not re.search(r"[!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>\/?]", v):
            raise ValueError("La contraseña debe contener al menos un carácter especial")
        return v

class UserLogin(BaseModel):
    email:EmailStr
    password:str


#Respuesta Api
class UserResponse(BaseModel):
    id:int
    email:EmailStr
    role:str
    is_active:bool
    
    class Config:
        from_attributes = True

class DetalleUser(BaseModel):
    id:int
    email:EmailStr
    role:str
    created_at:datetime

class LoginUserResponse(BaseModel):
    access_token: str
    token_type: str
    user: DetalleUser

class EmailRequest(BaseModel):
    email:EmailStr