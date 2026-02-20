from sqlalchemy.orm import Session
from app.modules.auth.schemas import CreateUser
from app.models.user import User
from fastapi import HTTPException
from app.modules.auth.services import hash_password, verify_password
from app.modules.auth.auth import create_access_token


def crear_usuario(db:Session,user:CreateUser):
    existe_user = db.query(User).filter(User.email == user.email).first()

    if existe_user:
        raise HTTPException(
            status_code=400,
            detail="usuario ya existe"
        )
    nuevo_usuario = User(
        email= user.email,
        password = hash_password(user.password),
    )
    
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return{
        "message": "Usuario registrado con exito"

    }

def DetalleUser(db:Session,id:int):
    return db.query(User).filter(User.id == id).first()

def login_usuario(db:Session, email: str, password:str):
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.password):
        raise HTTPException(status_code=401,detail="Credenciales invalidas")
    
    token = create_access_token({"sub": str(user.id), "email":user.email, "role":user.role})
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "created_at": user.created_at,
        },
    }
