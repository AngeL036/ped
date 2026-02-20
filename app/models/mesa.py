from sqlalchemy import Column, Integer,String, ForeignKey
from app.database import Base
from sqlalchemy.orm import relationship


class Mesa(Base):
    __tablename__ = "mesas"

    id = Column(Integer, primary_key=True, index=True)
    negocio_id = Column(Integer, ForeignKey("negocios.id"), nullable=False)
    numero = Column(Integer, nullable=False)
    capacidad = Column(Integer)
    estado = Column(String(20), default="libre")  # libre, ocupado, reservado

    negocio = relationship("Negocio", back_populates="mesas")
    pedidos = relationship("Pedido", back_populates="mesa")
