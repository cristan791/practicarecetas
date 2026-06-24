from flask_appbuilder.models.sqla.interface import SQLAInterface

from app.models.cliente import Cliente
from app.permissions import can_manage_sales
from app.views.base import AuditModelView


class ClienteModelView(AuditModelView):
    datamodel = SQLAInterface(Cliente)

    list_title = "Clientes"
    show_title = "Detalle de cliente"
    add_title = "Nuevo cliente"
    edit_title = "Editar cliente"

    list_columns = [
        "nombre_completo",
        "ci_nit",
        "telefono",
        "correo",
        "estado",
    ]
    show_columns = list_columns + ["direccion", "created_on", "changed_on"]
    add_columns = [
        "nombre_completo",
        "ci_nit",
        "telefono",
        "direccion",
        "correo",
        "estado",
    ]
    edit_columns = add_columns
    search_columns = ["nombre_completo", "ci_nit", "telefono", "correo"]

    label_columns = {
        "nombre_completo": "Nombre completo",
        "ci_nit": "CI/NIT",
        "telefono": "Teléfono",
        "direccion": "Dirección",
        "correo": "Correo electrónico",
        "estado": "Activo",
        "created_on": "Creado",
        "changed_on": "Modificado",
    }

    def is_accessible(self):
        return can_manage_sales()
