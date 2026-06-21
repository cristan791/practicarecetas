# from flask_appbuilder import Model
from sqlalchemy import Column, Integer, String
from app.extensions import db

class Categoria(db.Model):
    __tablename__ = "categoria"
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False, unique=True)
    
    def __repr__(self):
        return self.nombre