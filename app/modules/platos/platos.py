from sqlalchemy.orm import Session
from app.models.plato import Plato
from app.models.user import User
from app.modules.platos.schemas import CreatePlato,UpdatePlato

def get_platos(db:Session):
    return db.query(Plato).all()

def get_plato(db:Session, plato_id: int):
    return db.query(Plato).filter( Plato.id == plato_id).first()

def get_plato_negocio_mesa(db:Session,plato_id:int,user:User):
    empleado = user.empleado
    if not empleado:
        return None
    return db.query(Plato).filter(
        Plato.id == plato_id,
        Plato.negocio_id == empleado.negocio_id
    ).first()

def create_plato(db:Session, plato:CreatePlato):
    #nuevo_plato = Plato(**plato.model_dump())
    nuevo_plato = Plato(
        nombre=plato.nombre,
        precio=plato.precio,
        descripcion=plato.descripcion,
       
        negocio_id=1,      # ← dato estático de prueba
        categoria_id=1     # ← dato estático de prueba
    )
    db.add(nuevo_plato)
    db.commit()
    db.refresh(nuevo_plato)
    return nuevo_plato

def update_plato(db:Session, plato_db: Plato, datos:UpdatePlato):
    for key, value in datos.model_dump(exclude_unset=True).items():
        setattr(plato_db,key, value)

    db.commit()
    db.refresh(plato_db)
    return plato_db

def delete_plato(db:Session, plato_db: Plato):
    db.delete(plato_db)
    db.commit()

def patch_activo(db:Session,plato_id:int,activo:bool):
    plato = db.query(Plato).filter(Plato.id == plato_id).first()
    
    if not plato:
        return None
    
    plato.activo = activo
    db.commit()
    db.refresh(plato)

    return plato
