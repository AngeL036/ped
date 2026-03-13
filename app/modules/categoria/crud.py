from sqlalchemy.orm import Session
from app.models.categoria import Categoria

def get_categorias(db: Session, negocio_id: int):
    return db.query(Categoria).filter(Categoria.negocio_id == negocio_id).all()
 
def create_categoria(db: Session, negocio_id: int, nombre: str):
    categoria = Categoria(negocio_id=negocio_id, nombre=nombre)
    db.add(categoria)
    db.commit()
    db.refresh(categoria)
    return categoria