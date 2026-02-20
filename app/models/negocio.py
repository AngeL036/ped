from sqlalchemy import Column, Integer,String, Boolean, DateTime, ForeignKey
from app.database import Base
from datetime import datetime, timezone
from sqlalchemy.orm import relationship


class Negocio(Base):
    __tablename__ = "negocios"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    nombre = Column(String(255), nullable=False)
    direccion = Column(String(255))
    telefono = Column(String(50))
    activo = Column(Boolean, default=True)
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )

    owner = relationship("User", back_populates="negocios")
    empleados = relationship("Empleado", back_populates="negocio", cascade="all, delete")
    mesas = relationship("Mesa", back_populates="negocio", cascade="all, delete")
    categorias = relationship("Categoria", back_populates="negocio", cascade="all, delete")
    platos = relationship("Plato", back_populates="negocio", cascade="all, delete")
    pedidos = relationship("Pedido", back_populates="negocio", cascade="all, delete")
