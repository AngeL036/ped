from sqlalchemy import Column,Integer,String,DateTime, ForeignKey,Numeric
from app.database import Base
from datetime import datetime, timezone
from sqlalchemy.orm import relationship

class Inventario(Base):
    __tablename__ = "inventario"

    id               = Column(Integer, primary_key=True, index=False)
    producto_id      = Column(Integer, ForeignKey("producto.id"), nullable=False)
    PrecioCompra     = Column(Numeric(10,2), nullable=False)
    PrecioVenta      = Column(Numeric(10, 2), nullable=False)
    ganancia         = Column(Numeric(10, 2))
    valor_inventario = Column(Numeric(10,2))
    estado           = Column(String(20))
    create_at        = Column(DateTime(timezone=True),default=lambda: datetime.now(timezone.utc))

    producto = relationship("Producto", back_populates="inventario")