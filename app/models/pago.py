from sqlalchemy import Column, Integer,String, Boolean, DateTime, ForeignKey, Numeric
from app.database import Base
from datetime import datetime, timezone
from sqlalchemy.orm import relationship


class Pago(Base):
    __tablename__ = "pagos"

    id = Column(Integer, primary_key=True, index=True)
    pedido_id = Column(Integer, ForeignKey("pedidos.id"), nullable=False)
    metodo = Column(String(50))  # efectivo, tarjeta, transferencia
    monto = Column(Numeric(10, 2), nullable=False)
    fecha = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )

    pedido = relationship("Pedido", back_populates="pagos")
