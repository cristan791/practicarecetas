from sqlalchemy import (
    Boolean,
    Column,
    Date,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
)
from sqlalchemy.orm import relationship

from app.extensions import db
from app.models.mixins import AuditMixin


class Producto(db.Model, AuditMixin):
    __tablename__ = "producto"

    id = Column(Integer, primary_key=True)
    nombre = Column(String(150), nullable=False)
    descripcion = Column(Text)
    precio_compra = Column(Numeric(10, 2), default=0, nullable=False)
    precio_venta = Column(Numeric(10, 2), default=0, nullable=False)
    categoria_id = Column(Integer, ForeignKey("categoria.id"), nullable=False)
    envase_id = Column(Integer, ForeignKey("envase.id"), nullable=False)
    fecha_vencimiento = Column(Date, nullable=True)
    codigo_barras = Column(String(50), unique=True, nullable=True)
    imagen = Column(String(255), nullable=True)
    stock = Column(Integer, default=0, nullable=False)
    stock_minimo = Column(Integer, default=5, nullable=False)
    estado = Column(Boolean, default=True, nullable=False)

    categoria = relationship("Categoria", back_populates="productos")
    envase = relationship("Envase", back_populates="productos")
    movimientos = relationship("MovimientoInventario", back_populates="producto")

    def __repr__(self):
        return self.nombre

    @property
    def stock_bajo(self):
        return self.stock <= self.stock_minimo

    @property
    def agotado(self):
        return self.stock <= 0
