from pydantic import BaseModel,EmailStr
from datetime import datetime

class CreateUser(BaseModel):
    email:EmailStr
    password:str

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
    created_at:datetime

class LoginUserResponse(BaseModel):
    access_token: str
    token_type: str
    user: DetalleUser