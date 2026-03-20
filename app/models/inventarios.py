from sqlalchemy import Column,Integer,String,DateTime
from app.database import Base
from datetime import datetime, timezone

class Inventario(Base):
    __tablename__ = "inventario"

    id = Column(Integer, primary_key=True, index=False)
    PrecioCompra = Column(Integer,)
    PrecioVenta = Column()
    Estado = Column()

    create_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc))
