from sqlalchemy import Column, Integer,String, ForeignKey
from app.database import Base
from sqlalchemy.orm import relationship


class Categoria(Base):
    __tablename__ = "categorias"

    id = Column(Integer, primary_key=True, index=True)
    negocio_id = Column(Integer, ForeignKey("negocios.id"), nullable=False)
    nombre = Column(String(100), nullable=False)

    negocio = relationship("Negocio", back_populates="categorias")
    platos = relationship("Plato", back_populates="categoria")
