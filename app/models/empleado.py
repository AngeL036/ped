from sqlalchemy import Column, Integer,String, Boolean, ForeignKey
from app.database import Base
from sqlalchemy.orm import relationship


class Empleado(Base):
    __tablename__ = "empleados"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    negocio_id = Column(Integer, ForeignKey("negocios.id"), nullable=False)
    rol = Column(String(50))  # mesero, cocina, caja, admin
    activo = Column(Boolean, default=True)

    user = relationship("User", back_populates="empleado")
    negocio = relationship("Negocio", back_populates="empleados")
    pedidos = relationship("Pedido", back_populates="mesero")
