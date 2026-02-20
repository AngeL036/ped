from sqlalchemy import Column, Integer,String, Boolean, Numeric, ForeignKey
from app.database import Base
from sqlalchemy.orm import relationship


class Plato(Base):
    __tablename__ = "platos"

    id = Column(Integer, primary_key=True, index=True)
    negocio_id = Column(Integer, ForeignKey("negocios.id"), nullable=False)
    categoria_id = Column(Integer, ForeignKey("categorias.id"))
    nombre = Column(String(150), nullable=False)
    precio = Column(Numeric(10, 2), nullable=False)
    descripcion = Column(String(255))
    activo = Column(Boolean, default=True)

    negocio = relationship("Negocio", back_populates="platos")
    categoria = relationship("Categoria", back_populates="platos")
    detalles = relationship("DetallePedido", back_populates="plato")
