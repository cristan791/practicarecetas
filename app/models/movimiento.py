from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.extensions import db


class MovimientoInventario(db.Model):
    __tablename__ = "movimiento_inventario"

    id = Column(Integer, primary_key=True)
    fecha = Column(DateTime, default=datetime.utcnow, nullable=False)
    producto_id = Column(Integer, ForeignKey("producto.id"), nullable=False)
    tipo = Column(String(20), nullable=False)
    cantidad = Column(Integer, nullable=False)
    stock_anterior = Column(Integer, nullable=False)
    stock_nuevo = Column(Integer, nullable=False)
    referencia_tipo = Column(String(30), nullable=False)
    referencia_id = Column(Integer, nullable=False)
    usuario_id = Column(Integer, nullable=False)
    observacion = Column(Text)

    producto = relationship("Producto", back_populates="movimientos")

    def __repr__(self):
        return f"{self.tipo} - {self.producto_id}"
