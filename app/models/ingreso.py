from datetime import datetime

from flask_appbuilder.security.sqla.models import User
from sqlalchemy import Column, DateTime, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import relationship

from app.extensions import db
from app.models.mixins import AuditMixin


class Ingreso(db.Model, AuditMixin):
    __tablename__ = "ingreso"

    id = Column(Integer, primary_key=True)
    fecha = Column(DateTime, default=datetime.utcnow, nullable=False)
    proveedor = Column(String(200), nullable=False)
    observacion = Column(Text)
    usuario_id = Column(Integer, nullable=False)

    detalles = relationship(
        "IngresoDetalle",
        back_populates="ingreso",
        cascade="all, delete-orphan",
    )

    @property
    def usuario(self):
        """Obtiene el nombre del usuario que registró."""
        try:
            user = db.session.get(User, self.usuario_id)
            return user.get_full_name() if user else f"ID: {self.usuario_id}"
        except Exception:
            return f"ID: {self.usuario_id}"

    def __repr__(self):
        return f"Ingreso #{self.id}"


class IngresoDetalle(db.Model):
    __tablename__ = "ingreso_detalle"

    id = Column(Integer, primary_key=True)
    ingreso_id = Column(Integer, ForeignKey("ingreso.id"), nullable=False)
    producto_id = Column(Integer, ForeignKey("producto.id"), nullable=False)
    cantidad = Column(Integer, nullable=False)
    precio_compra = Column(Numeric(10, 2), nullable=False)
    subtotal = Column(Numeric(10, 2), nullable=False)

    ingreso = relationship("Ingreso", back_populates="detalles")
    producto = relationship("Producto")

    def __repr__(self):
        return f"Detalle ingreso {self.id}"