from app.database import Base
from sqlalchemy import Integer, ForeignKey, String,Column,DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

class MovimientoInventario(Base):
    __tablename__ = "movimientos_inventario"

    id           = Column(Integer, primary_key=True)
    producto_id  = Column(Integer, ForeignKey("productos.id"), nullable=False)
    tipo         = Column(String(20), nullable=False)  # "entrada", "salida", "ajuste"
    cantidad     = Column(Integer, nullable=False)
    motivo       = Column(String(100))  # "compra", "venta", "merma", "conteo físico"
    created_at   = Column(DateTime(timezone=True),default=lambda: datetime.now(timezone.utc))

    producto     = relationship("Producto", back_populates="movimientos")