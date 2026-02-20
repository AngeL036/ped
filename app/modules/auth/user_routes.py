from app.modules.auth import crud_user
from fastapi import APIRouter, Depends
from app.modules.auth.schemas import CreateUser, DetalleUser,UserLogin, LoginUserResponse
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.modules.auth.auth import get_current_user
from app.models.user import User


router_user = APIRouter(prefix="/auth", tags=["Auth"])

@router_user.post("/", status_code=201)
def registrar_user(user:CreateUser,db:Session = Depends(get_db)):
    return crud_user.crear_usuario(db,user)


@router_user.get("/{id}", response_model=DetalleUser)
def obtenerUser(id:int,db:Session = Depends(get_db)):
    return crud_user.DetalleUser(db,id)

@router_user.post("/login",response_model=LoginUserResponse)
def login(user:UserLogin, db:Session = Depends(get_db)):
    return crud_user.login_usuario(db,user.email, user.password)

@router_user.get("/me")
def me(current_user:User = Depends(get_current_user)):
    return {"id": current_user.id, "email":current_user.email, "role":current_user.role}
