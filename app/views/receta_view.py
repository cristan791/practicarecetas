from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface
from app.models.receta import Receta
from app.models.receta_ingrediente import RecetaIngrediente

class RecetaIngredienteView(ModelView):
    datamodel = SQLAInterface(RecetaIngrediente)
    list_columns = ['receta', 'ingrediente', "cantidad"]
    add_columns = ['receta', 'ingrediente', "cantidad"]
    edit_columns = ['receta', 'ingrediente', "cantidad"]
    show_columns = ['receta', 'ingrediente', "cantidad"]

class RecetaModelView(ModelView):
    datamodel = SQLAInterface(Receta)
    related_views = [RecetaIngredienteView]
    list_columns = ['nombre', "categoria.nombre", "descripcion"]
    add_columns = ['nombre', "categoria", "descripcion", "instrucciones"]
    edit_columns = ['nombre', "categoria", "descripcion", "instrucciones"]