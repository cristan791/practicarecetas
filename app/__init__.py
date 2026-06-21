from flask import Flask
from .extensions import appbuilder, db


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object("config")
    db.init_app(app)
    with app.app_context():
        appbuilder.init_app(app, db.session)
        # from app.models import Categoria, Ingrediente
        from app.models.categoria import Categoria
        from app.models.ingrediente import Ingrediente
        from app.models.receta import Receta
        from app.models.receta_ingrediente import RecetaIngrediente

        db.create_all()
        from app.views.reporte_graficas import ReporteCategoriaView
        from app.views import CategoriaView, IngredienteView
        from app.views.receta_view import RecetaModelView, RecetaIngredienteView
        from app.views.reportes import ReporteSimpleView
        appbuilder.add_view(
                CategoriaView, 
                "Categorías", 
                icon="fa-folder-open-o", 
                category="Recetas")
        
        appbuilder.add_view(
            IngredienteView, 
            "Ingredientes", 
            icon="fa-lemon-o", 
            category="Recetas")
        
        appbuilder.add_view(
            RecetaModelView, 
            "Recetas", 
            icon="fa-lemon-o", 
            category="Recetas")
        
        appbuilder.add_view(
            RecetaIngredienteView, 
            "Ingredientes por Receta", 
            icon="fa-list", 
            category="Recetas")
        
        appbuilder.add_view(
            ReporteSimpleView, 
            "Reportes de recetas por categoria", 
            icon="fa-lemon-o", 
            category="Reportes")
        
        appbuilder.add_view(
            ReporteCategoriaView, 
            "Graficas por categoria", 
            icon="fa-bar-chart", 
            category="Reportes")
    return app
