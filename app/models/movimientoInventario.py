from app.database import Base
from sqlalchemy import Integer, ForeignKey, String,Column,DateTime,Numeric, Enum as SAEnum
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
import enum

class TipoMovimiento(str, enum.Enum):
    entrada = "entrada"
    salida  = "salida"
    ajuste  = "ajuste"

class MotivoMovimiento(str, enum.Enum):
    compra = "compra"
    venta = "venta"
    merma = "merma"
    conteo_fisico = "conteo_fisico"
    devolucion = "devolucion"

class MovimientoInventario(Base):
    __tablename__ = "movimientos_inventario"

    id           = Column(Integer, primary_key=True)
    producto_id  = Column(Integer, ForeignKey("productos.id"), nullable=False)
    tipo         = Column(SAEnum(TipoMovimiento), nullable=False)  
    cantidad     = Column(Numeric(10,2), nullable=False)
    motivo       = Column(SAEnum(MotivoMovimiento), nullable=True)  
    created_at   = Column(DateTime(timezone=True),default=lambda: datetime.now(timezone.utc))

    producto     = relationship("Producto", back_populates="movimientos")