from sqlalchemy import Column, Integer,String, Boolean, DateTime
from app.database import Base
from datetime import datetime, timezone
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password = Column(String(255), nullable=False)
    role = Column(String(50), default="owner")  # owner, admin, mesero, cocina
    is_active = Column(Boolean, default=True)
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )

    negocios = relationship("Negocio", back_populates="owner")
    empleado = relationship("Empleado", back_populates="user", uselist=False)
