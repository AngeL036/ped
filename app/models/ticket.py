from sqlalchemy import Column, Integer, ForeignKey, String, DateTime
from app.database import Base
from datetime import datetime, timezone


class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True)
    venta_id = Column(Integer, ForeignKey("ventas.id"))
    folio = Column(String(50), unique=True)
    created_at = Column(DateTime(timezone=True), default=lambda : datetime.now(timezone.utc))