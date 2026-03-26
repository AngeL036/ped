from app.database import Base
from sqlalchemy import Column, String,ForeignKey, DateTime,DECIMAL, Integer, Float
from datetime import datetime,timezone
class CorteCaja(Base):
    __tablename__ = "cortes_caja"

    id = Column(Integer,primary_key=True)
    negocio_id = Column(Integer)
    usuario_id = Column(Integer)
    fecha_apertura = Column(DateTime)
    fecha_cierre = Column(DateTime, nullable=True)
    monto_inicial = Column(Float)
    monto_final = Column(Float, nullable=True)