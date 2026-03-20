from sqlalchemy import Column, DateTime, Integer, String, ForeignKey
from datetime import datetime, timezone
from app.database import Base
from sqlalchemy.orm import relationship

class Producto(Base):
    __tablename__ = "producto"

    id             = Column(Integer, primary_key=True, index=False)
    negocio_id     = Column(Integer, ForeignKey("negocios.id"), nullable=False)
    codigo         = Column(String(30),nullable=True)
    nombre         = Column(String(100),nullable=False)
    categoria_id   = Column(Integer,ForeignKey("categorias.id"), nullable=True)
    unidad         = Column(String(30),nullable=False)
    cantidadActual = Column(Integer,nullable=False, default=0)
    stock_minimo   = Column(Integer, nullable=False, default=3)
    created_at     = Column(DateTime(timezone=True), default=lambda : datetime.now(timezone.utc))

    negocio         = relationship("Negocio", back_populates="productos")
    categoria       = relationship("Categoria", back_populates="productos")
    inventario      = relationship("Inventario", back_populates="producto")
