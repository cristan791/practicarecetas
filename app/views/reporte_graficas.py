from flask import request
from sqlalchemy import func
from app.extensions import db
from flask_appbuilder import BaseView, expose
from app.models.categoria import Categoria
from app.models.receta import Receta
class ReporteCategoriaView(BaseView):
    
    @expose("/")
    def list(self):
        datos = (
            db.session.query(
                Categoria.nombre,
                func.count(Receta.id)
            )
            .join(Receta, Receta.categoria_id == Categoria.id)
            .group_by(Categoria.nombre)
            .all()
        )
        categorias = [d[0] for d in datos]  
        cantidades  = [d[1] for d in datos]  
        return self.render_template(
            "grafica_categoria.html",
            categorias = categorias,
            cantidades = cantidades
        )