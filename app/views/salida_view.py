from flask import flash, g
from flask_appbuilder.models.sqla.interface import SQLAInterface
from wtforms.validators import NumberRange

from app.models.salida import Salida, SalidaDetalle
from app.permissions import can_manage_sales
from app.services.inventario_service import (
    InventarioError,
    aplicar_salida_detalle,
    calcular_subtotal,
    recalcular_total_salida,
    revertir_salida_detalle,
)
from app.views.base import AuditModelView
from app.constants import ROLE_VENDEDOR


class SalidaModelView(AuditModelView):
    datamodel = SQLAInterface(Salida)

    list_title = "Ventas / Salidas"
    show_title = "Detalle de venta"
    add_title = "Nueva venta"
    edit_title = "Editar venta"

    list_columns = ["id", "fecha", "cliente", "vendedor", "total"]
    show_columns = list_columns + ["created_on", "changed_on"]
    add_columns = ["fecha", "cliente"]
    edit_columns = add_columns
    search_columns = ["cliente"]

    label_columns = {
        "fecha": "Fecha",
        "cliente": "Cliente",
        "vendedor": "Vendedor",
        "total": "Total",
        "created_on": "Creado",
        "changed_on": "Modificado",
    }

    def is_accessible(self):
        return can_manage_sales()

    def pre_add(self, item):
        super().pre_add(item)
        item.vendedor_id = g.user.id
        item.total = 0


class SalidaDetalleModelView(AuditModelView):
    datamodel = SQLAInterface(SalidaDetalle)
    base_permissions = ["can_list", "can_show", "can_add", "can_edit"]

    form_args = {
        "cantidad": {"validators": [NumberRange(min=1, message="La cantidad debe ser mayor a 0")]},
    }

    list_title = "Detalle de ventas"
    add_title = "Agregar producto a la venta"
    edit_title = "Editar detalle de venta"

    list_columns = ["salida", "producto", "cantidad", "precio", "subtotal"]
    add_columns = ["salida", "producto", "cantidad", "precio"]
    edit_columns = add_columns

    label_columns = {
        "salida": "Venta",
        "producto": "Producto",
        "cantidad": "Cantidad",
        "precio": "Precio",
        "subtotal": "Subtotal",
    }

    def is_accessible(self):
        return can_manage_sales()

    def pre_add(self, item):
        if not item.precio:
            item.precio = item.producto.precio_venta
        item.subtotal = calcular_subtotal(item.cantidad, item.precio)

    def pre_update(self, item):
        item.subtotal = calcular_subtotal(item.cantidad, item.precio)

    def post_add(self, item):
        try:
            aplicar_salida_detalle(item, g.user.id)
            recalcular_total_salida(item.salida)
        except InventarioError as exc:
            flash(str(exc), "danger")
            raise

    def post_update(self, item):
        flash(
            "Para modificar cantidades vendidas, elimine el detalle y regístrelo nuevamente.",
            "warning",
        )

    def post_delete(self, item):
        salida = item.salida
        try:
            revertir_salida_detalle(item, g.user.id)
            recalcular_total_salida(salida)
        except InventarioError as exc:
            flash(str(exc), "danger")
            raise