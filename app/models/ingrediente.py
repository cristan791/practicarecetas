# from flask_appbuilder import Model
from sqlalchemy import Column, Integer, String
from app.extensions import db
class Ingrediente(db.Model):
    __tablename__ = "ingrediente"
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False, unique=True)
    unidad_medida = Column(String(50), nullable=False)
    
    def __repr__(self):
        return self.nombre