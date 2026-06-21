from flask import request
from sqlalchemy import func
from app.extensions import db
from flask_appbuilder import BaseView, expose
from app.models.categoria import Categoria
from app.models.ingrediente import Ingrediente
from app.models.receta import Receta
from app.models.receta_ingrediente import RecetaIngrediente
class ReporteSimpleView(BaseView):
    
    @expose("/", methods =["GET", "POST"])
    def list(self):
        categorias = db.session.query(Categoria).all()
        categoria_seleccionada = request.form.get('cat_id')

        if categoria_seleccionada:
            ingredientes = (
                db.session.query(Ingrediente)
                .join(RecetaIngrediente, RecetaIngrediente.ingrediente_id == Ingrediente.id)
                .join(Receta, Receta.id == RecetaIngrediente.receta_id)
                .filter(Receta.categoria_id == categoria_seleccionada)
                .distinct()
                .all()
            )
        else:
            ingredientes = db.session.query(Ingrediente).all()

        return self.render_template(
            "reportes.html",
            categorias = categorias,
            id_categoria=categoria_seleccionada,
            ingredientes=ingredientes
        )