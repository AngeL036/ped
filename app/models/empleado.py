from sqlalchemy import Column, Integer,String, Boolean, ForeignKey, DateTime
from app.database import Base
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

class Empleado(Base):
    __tablename__ = "empleados"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    apellido = Column(String(100), nullable=False)
    edad = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    negocio_id = Column(Integer, ForeignKey("negocios.id"), nullable=False)
    rol = Column(String(50))  # mesero, cocina, caja, admin
    activo = Column(Boolean, default=True)
    must_change_password = Column(Boolean, default=False)
    create_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc))

    user = relationship("User", back_populates="empleado")
    negocio = relationship("Negocio", back_populates="empleados")
    pedidos = relationship("Pedido", back_populates="mesero")
