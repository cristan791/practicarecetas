from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from app.extensions import db

class Receta(db.Model):
    __tablename__ = "receta"
    id = Column(Integer, primary_key=True)
    nombre = Column(String(150), nullable=False)
    descripcion = Column(String(500), nullable=True)
    instrucciones = Column(Text, nullable=False)
    
    categoria_id =  Column(Integer, ForeignKey("categoria.id"), nullable=False )
    # sa.Column("user_id", sa.ForeignKey(User.id), primary_key=True),
    categoria = relationship("Categoria", backref="recetas")
    # relacion muchos a muchos
    
    ingredientes = relationship("RecetaIngrediente", back_populates="receta", cascade="all")
    
    def __repr__(self):
        return self.nombre