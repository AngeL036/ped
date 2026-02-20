from sqlalchemy import Column, Integer,String, Numeric, DateTime, ForeignKey
from app.database import Base
from datetime import datetime, timezone
from sqlalchemy.orm import relationship


class Pedido(Base):
    __tablename__ = "pedidos"

    id = Column(Integer, primary_key=True, index=True)
    negocio_id = Column(Integer, ForeignKey("negocios.id"), nullable=False)
    mesa_id = Column(Integer, ForeignKey("mesas.id"), nullable=False)
    mesero_id = Column(Integer, ForeignKey("empleados.id"))

    total = Column(Numeric(10, 2), default=0)
    estado = Column(String(20), default="abierto")
    # abierto, en_cocina, servido, cerrado, cancelado

    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )

    negocio = relationship("Negocio", back_populates="pedidos")
    mesa = relationship("Mesa", back_populates="pedidos")
    mesero = relationship("Empleado", back_populates="pedidos")
    detalles = relationship("DetallePedido", back_populates="pedido", cascade="all, delete")
    pagos = relationship("Pago", back_populates="pedido", cascade="all, delete")
