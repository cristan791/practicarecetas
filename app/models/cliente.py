from sqlalchemy import Boolean, Column, Integer, String, Text
from sqlalchemy.orm import relationship

from app.extensions import db
from app.models.mixins import AuditMixin


class Cliente(db.Model, AuditMixin):
    __tablename__ = "cliente"

    id = Column(Integer, primary_key=True)
    nombre_completo = Column(String(200), nullable=False)
    ci_nit = Column(String(50), nullable=True)
    telefono = Column(String(50), nullable=True)
    direccion = Column(String(255), nullable=True)
    correo = Column(String(120), nullable=True)
    estado = Column(Boolean, default=True, nullable=False)

    ventas = relationship("Salida", back_populates="cliente")

    def __repr__(self):
        return self.nombre_completo
