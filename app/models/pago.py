from sqlalchemy import Column, Integer,String, Boolean, DateTime, ForeignKey, Numeric, Enum as SAEnum
from app.database import Base
from datetime import datetime, timezone
from sqlalchemy.orm import relationship
import enum

class MetodoPago(str, enum.Enum):
    efectivo      = "efectivo"
    tarjeta       = "tarjeta"
    transferencia =  "transferencia" 
    vale          = "vale"

class EstadoPago(str, enum.Enum):
    pendiente  = "pendiente"
    completado = "completado"
    reversado  = "reversado"
 
class Pago(Base):
    __tablename__ = "pagos"

    id             = Column(Integer, primary_key=True, index=True)
    pedido_id      = Column(Integer, ForeignKey("pedidos.id"), nullable=False)
    metodo         = Column(SAEnum(MetodoPago), nullable=False) 
    monto          = Column(Numeric(10, 2), nullable=False)

    monto_recibido = Column(Numeric(10, 2), nullable=True)  # lo que entregó el cliente
    cambio         = Column(Numeric(10, 2), nullable=True)  # monto_recibido - monto
    propina        = Column(Numeric(10, 2), nullable=True, default=0)
    created_at     = Column(DateTime(timezone=True),default=lambda: datetime.now(timezone.utc))
    estado         = Column(SAEnum(EstadoPago), default=EstadoPago.completado, nullable=False) 

    pedido = relationship("Pedido", back_populates="pagos")
