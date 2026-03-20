from sqlalchemy import Column,Integer,String,DateTime, ForeignKey,Numeric
from app.database import Base
from datetime import datetime, timezone
from sqlalchemy.orm import relationship

class Inventario(Base):
    __tablename__ = "inventario"

    id                = Column(Integer, primary_key=True, index=False)
    producto_id       = Column(Integer, ForeignKey("productos.id"), nullable=False)
    cantidad          = Column(Integer, nullable=False)
    motivo            = Column(String(100))
    created_at        = Column(DateTime(timezone=True),default=lambda: datetime.now(timezone.utc))

    producto = relationship("Producto", back_populates="inventario")