from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface
from app.models.categoria import Categoria

class CategoriaView(ModelView):
    datamodel = SQLAInterface(Categoria)
    list_columns = ['nombre']
    add_columns = ['nombre']
    edit_columns = ['nombre']
