from jose import JWTError, jwt
from sqlalchemy.orm import Session
from app.modules.auth.schemas import CreateUser
from app.models.user import User
from fastapi import HTTPException
from app.core.config import settings
from app.modules.auth.services import hash_password, verify_password, generate_random_password
from app.modules.auth.auth import create_access_token, create_verification_token
from app.modules.auth.email import send_verification_email
from datetime import datetime, timezone, timedelta
from fastapi.responses import RedirectResponse
from app.models.negocio import Negocio


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
        role = user.role,
        is_verified = False,
    )
    
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    token = create_verification_token(nuevo_usuario.email)
    send_verification_email(nuevo_usuario.email, token)
    return{
        "message": "Usuario creado exitosamente. Por favor verifica tu correo electrónico para activar tu cuenta."

    }

def crear_usuario_empleado(db:Session,email:str, role:str):
    existe_user = db.query(User).filter(User.email == email).first()

    if existe_user:
        raise HTTPException(
            status_code=400,
            detail="usuario ya existe"
        )
    temporal_password = generate_random_password()
    nuevo_usuario = User(
        email= email,
        password = hash_password(temporal_password),
        must_change_password=True,
        role=role
    )
    
    db.add(nuevo_usuario)
    db.flush()
    return nuevo_usuario, temporal_password

def DetalleUser(db:Session,id:int):
    return db.query(User).filter(User.id == id).first()

def login_usuario(db:Session, email: str, password:str):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Credenciales invalidas"
        )
    if not user.is_verified:
        raise HTTPException(
            status_code=403,
            detail={
                "code": "EMAIL_NOT_VERIFIED",
                "message":"Debes verificar tu cuenta antes de iniciar sesion"
            })
    if  not verify_password(password, user.password):
        raise HTTPException(status_code=401,detail="Credenciales invalidas")
    
    token = create_access_token({"sub": str(user.id), "email":user.email, "role":user.role})
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "role" : user.role,
            "created_at": user.created_at,
        },
    }

def cambiar_password(db:Session, user:User, new_password:str):
    user = db.query(User).filter(User.id == user.id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    user.password = hash_password(new_password)
    user.must_change_password = False
    db.commit()
    db.refresh(user)
    return {
        "message": "Contraseña actualizada con éxito"
    }

def verify_email(db:Session, token:str):
    try:
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
        if payload.get("type") != "email_verification":
            return RedirectResponse(
                    url="https://agsa.website/restaurante/verificacion-error"
                    )
        email = payload.get("sub")
    except  JWTError:
        return RedirectResponse(
            url="https://agsa.website/restaurante/verificacion-error"
        )
    
    user = db.query(User).filter(User.email == email).first()

    if not user:
        return RedirectResponse(
            url="https://agsa.website/restaurante/verificacion-error"
        )
    
    if not user.is_verified:
        user.is_verified = True
    db.commit()

    return RedirectResponse(
        url="https://agsa.website/restaurante/verificacion-exitosa"
    )

def forward_email(db:Session, email:str):
    user = db.query(User).filter(User.email == email).first()

    if not user:
        return {"message": "Se ha enviado un enlace de verificacion"}
    if user.is_verified:
        return {"message": "La cuenta ya está verificada"}
    #VALIDACIÓN ANTI-SPAM
    if user.last_verification_sent and datetime.now(timezone.utc) - user.last_verification_sent < timedelta(minutes=2):
        raise HTTPException(
            status_code=429,
            detail="Debes esperar antes de solicitar otro correo"
        )
    token = create_verification_token(email)
    send_verification_email(email,token)

    user.last_verification_sent = datetime.now(timezone.utc)
    db.commit()
    
    return {"message": "Se ha reenviado el correo de verificación"}

def me (db:Session, user:User):
    giro = None
    if User.negocio_id:
        negocio = db.query(Negocio).filter(Negocio.id == User.negocio_id).first()
        if negocio:
            giro = negocio.giro
    return {
        "id":user.id,
        "email":user.email,
        "negocio_id":user.negocio_id,
        "role":user.role,
        "giro": giro
    }