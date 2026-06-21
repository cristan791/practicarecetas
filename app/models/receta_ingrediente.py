from sqlalchemy import Column, Float, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import relationship
from app.extensions import db

class RecetaIngrediente (db.Model):
    __tablename__= "receta_ingrediente"
    __table_args__ = (
        UniqueConstraint("receta_id", "ingrediente_id", name="uq_receta_ingrediente"),
    )
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    receta_id = Column(Integer,  ForeignKey("receta.id"), nullable=False)
    ingrediente_id = Column(Integer,  ForeignKey("ingrediente.id"), nullable=False)
    cantidad =  Column (Float, nullable=False)
    
    receta = relationship("Receta", back_populates="ingredientes")
    ingrediente = relationship("Ingrediente")
    
    def __repr__(self):
        return f"{self.cantidad} de  {self.ingrediente.nombre}"