from sqlalchemy import Boolean, Column, Integer, String, Text
from sqlalchemy.orm import relationship

from app.extensions import db
from app.models.mixins import AuditMixin


class Envase(db.Model, AuditMixin):
    __tablename__ = "envase"

    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False, unique=True)
    descripcion = Column(Text)
    estado = Column(Boolean, default=True, nullable=False)

    productos = relationship("Producto", back_populates="envase")

    def __repr__(self):
        return self.nombre
