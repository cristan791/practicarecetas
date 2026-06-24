from flask_appbuilder.models.sqla.interface import SQLAInterface

from app.models.envase import Envase
from app.permissions import can_manage_catalog
from app.views.base import AuditModelView


class EnvaseModelView(AuditModelView):
    datamodel = SQLAInterface(Envase)

    list_title = "Envases"
    show_title = "Detalle de envase"
    add_title = "Nuevo envase"
    edit_title = "Editar envase"

    list_columns = ["nombre", "descripcion", "estado", "created_on"]
    show_columns = list_columns + ["changed_on"]
    add_columns = ["nombre", "descripcion", "estado"]
    edit_columns = add_columns
    search_columns = ["nombre", "descripcion"]

    label_columns = {
        "nombre": "Nombre",
        "descripcion": "Descripción",
        "estado": "Activo",
        "created_on": "Creado",
        "changed_on": "Modificado",
    }

    def is_accessible(self):
        return can_manage_catalog()
