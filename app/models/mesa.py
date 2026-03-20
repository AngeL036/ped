from sqlalchemy import Column, Integer,String, ForeignKey, Enum as SAEnum
from app.database import Base
from sqlalchemy.orm import relationship
import enum

class EstadoMesa(str, enum.Enum):
    libre     = "libre"
    ocupada   = "ocupada"
    reservada = "reservada"

class Mesa(Base):
    __tablename__ = "mesas"

    id         = Column(Integer, primary_key=True, index=True)
    negocio_id = Column(Integer, ForeignKey("negocios.id"), nullable=False)
    numero     = Column(Integer, nullable=False)
    capacidad  = Column(Integer)
    estado     = Column(SAEnum(EstadoMesa),default=EstadoMesa.libre, nullable=False ) 

    negocio = relationship("Negocio", back_populates="mesas")
    pedidos = relationship("Pedido", back_populates="mesa")
