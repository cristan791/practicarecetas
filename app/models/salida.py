from datetime import datetime

from flask import g
from flask_appbuilder.security.sqla.models import User
from sqlalchemy import Column, DateTime, ForeignKey, Integer, Numeric
from sqlalchemy.orm import relationship

from app.extensions import db
from app.models.mixins import AuditMixin


class Salida(db.Model, AuditMixin):
    __tablename__ = "salida"

    id = Column(Integer, primary_key=True)
    fecha = Column(DateTime, default=datetime.utcnow, nullable=False)
    cliente_id = Column(Integer, ForeignKey("cliente.id"), nullable=False)
    vendedor_id = Column(Integer, nullable=False)
    total = Column(Numeric(10, 2), default=0, nullable=False)

    cliente = relationship("Cliente", back_populates="ventas")
    detalles = relationship(
        "SalidaDetalle",
        back_populates="salida",
        cascade="all, delete-orphan",
    )

    @property
    def vendedor(self):
        """Obtiene el nombre del usuario vendedor."""
        try:
            user = db.session.get(User, self.vendedor_id)
            return user.get_full_name() if user else f"ID: {self.vendedor_id}"
        except Exception:
            return f"ID: {self.vendedor_id}"

    def __repr__(self):
        return f"Venta #{self.id}"


class SalidaDetalle(db.Model):
    __tablename__ = "salida_detalle"

    id = Column(Integer, primary_key=True)
    salida_id = Column(Integer, ForeignKey("salida.id"), nullable=False)
    producto_id = Column(Integer, ForeignKey("producto.id"), nullable=False)
    cantidad = Column(Integer, nullable=False)
    precio = Column(Numeric(10, 2), nullable=False)
    subtotal = Column(Numeric(10, 2), nullable=False)

    salida = relationship("Salida", back_populates="detalles")
    producto = relationship("Producto")

    def __repr__(self):
        return f"Detalle venta {self.id}"