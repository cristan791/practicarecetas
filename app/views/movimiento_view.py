from flask_appbuilder.models.sqla.interface import SQLAInterface

from app.models.movimiento import MovimientoInventario
from app.permissions import can_manage_catalog, can_manage_sales, can_view_reports
from app.views.base import AuditModelView


class MovimientoInventarioModelView(AuditModelView):
    datamodel = SQLAInterface(MovimientoInventario)

    list_title = "Historial de movimientos"
    show_title = "Detalle de movimiento"

    list_columns = [
        "fecha",
        "producto",
        "tipo",
        "cantidad",
        "stock_anterior",
        "stock_nuevo",
        "referencia_tipo",
        "referencia_id",
        "usuario_id",
    ]
    show_columns = list_columns + ["observacion"]
    base_permissions = ["can_list", "can_show"]

    label_columns = {
        "fecha": "Fecha",
        "producto": "Producto",
        "tipo": "Tipo",
        "cantidad": "Cantidad",
        "stock_anterior": "Stock anterior",
        "stock_nuevo": "Stock nuevo",
        "referencia_tipo": "Referencia",
        "referencia_id": "ID referencia",
        "usuario_id": "Usuario",
        "observacion": "Observación",
    }

    def is_accessible(self):
        return can_view_reports() or can_manage_catalog() or can_manage_sales()

    @property
    def can_add(self):
        return False

    @property
    def can_edit(self):
        return False

    @property
    def can_delete(self):
        return False
