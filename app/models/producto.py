from sqlalchemy import Column, DateTime, Integer, String, ForeignKey, Numeric, Boolean
from datetime import datetime, timezone
from app.database import Base
from sqlalchemy.orm import relationship

class Producto(Base):
    __tablename__ = "productos"

    id             = Column(Integer, primary_key=True, index=False)
    negocio_id     = Column(Integer, ForeignKey("negocios.id"), nullable=False)
    categoria_id   = Column(Integer,ForeignKey("categorias.id"), nullable=True)
    codigo         = Column(String(30),nullable=True)
    nombre         = Column(String(100),nullable=False)
    unidad         = Column(String(30),nullable=False)
    cantidad_actual = Column(Integer,nullable=False, default=0)
    stock_minimo   = Column(Integer, nullable=False, default=3)
    precio_compra  = Column(Numeric(10,2), nullable=False)
    precio_venta   = Column(Numeric(10,2), nullable=False)
    activo         = Column(Boolean, default=True)
    created_at     = Column(DateTime(timezone=True), default=lambda : datetime.now(timezone.utc))

    negocio         = relationship("Negocio", back_populates="productos")
    categoria       = relationship("Categoria", back_populates="productos")
    inventario      = relationship("Inventario", back_populates="producto")
    movimiento      = relationship("MovimientoInventario", back_populates="producto")