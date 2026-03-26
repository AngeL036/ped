from app.database import Base
from sqlalchemy import Column,ForeignKey, DateTime,Numeric, Integer
from sqlalchemy.orm import relationship
from datetime import datetime,timezone
class CorteCaja(Base):
    __tablename__ = "cortes_caja"

    id = Column(Integer,primary_key=True)
    negocio_id = Column(Integer, ForeignKey("negocios.id"), nullable=False)
    usuario_id = Column(Integer, ForeignKey("empleados.id"), nullable=False)
    fecha_apertura = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    fecha_cierre = Column(DateTime(timezone=True), nullable=True)
    monto_inicial = Column(Numeric(10, 2), nullable=False)
    monto_final = Column(Numeric(10, 2), nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    
    ventas = relationship("Venta", back_populates="corte_caja")
