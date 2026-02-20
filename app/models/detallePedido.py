from sqlalchemy import Column, Integer, ForeignKey, Numeric
from app.database import Base
from sqlalchemy.orm import relationship



class DetallePedido(Base):
    __tablename__ = "detalle_pedidos"

    id = Column(Integer, primary_key=True, index=True)
    pedido_id = Column(Integer, ForeignKey("pedidos.id"), nullable=False)
    platillo_id = Column(Integer, ForeignKey("platos.id"), nullable=False)

    cantidad = Column(Integer, nullable=False)
    precio_unitario = Column(Numeric(10, 2), nullable=False)
    subtotal = Column(Numeric(10, 2), nullable=False)

    pedido = relationship("Pedido", back_populates="detalles")
    plato = relationship("Plato", back_populates="detalles")
