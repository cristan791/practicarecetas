from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface
from app.models.ingrediente import Ingrediente

class IngredienteView(ModelView):
    datamodel = SQLAInterface(Ingrediente)
    list_columns = ['nombre', 'unidad_medida']
    add_columns = ['nombre','unidad_medida']
    edit_columns = ['nombre','unidad_medida']