from sqlalchemy import Column, DateTime, Integer, String, ForeignKey
from datetime import datetime
from app.database import Base


class Producto(Base):
    __tablename__ = "producto"

    id             = Column(Integer, primary_key=True, index=False)
    codigo         = Column(String(30),nullable=True)
    nombre         = Column(String(40),nullable=False)
    categoria_id   = Column(Integer,ForeignKey("categorias.id"))
    unidad         = Column(String(30),nullable=False)
    cantidadActual = Column(Integer,nullable=False)
