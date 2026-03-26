from sqlalchemy import Column, Integer,String, Boolean, DateTime, ForeignKey, Numeric, Enum as SAEnum
from app.database import Base
from datetime import datetime, timezone
from sqlalchemy.orm import relationship
import enum


class Venta(Base):
    __tablename__ = "ventas"

    id = Column(Integer, primary_key=True, index=True)
    negocio_id = Column(Integer, ForeignKey("negocios.id"), nullable=False)
    vendedor = Column(Integer, ForeignKey("empleados.id"), nullable=False)
    corte_caja_id = Column(Integer, ForeignKey("cortes_caja.id"), nullable=True)
    total = Column(Numeric(10,2))

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    detalles = relationship("DetalleVenta", back_populates="venta", cascade="all, delete")
    pagos    = relationship("Pago", back_populates="venta", cascade="all, delete")
    corte_caja = relationship("CorteCaja", back_populates="ventas")
