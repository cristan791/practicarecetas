from flask import flash, g
from flask_appbuilder.models.sqla.interface import SQLAInterface
from wtforms.validators import NumberRange

from app.models.ingreso import Ingreso, IngresoDetalle
from app.permissions import can_manage_catalog
from app.services.inventario_service import (
    InventarioError,
    aplicar_ingreso_detalle,
    calcular_subtotal,
    revertir_ingreso_detalle,
)
from app.views.base import AuditModelView


class IngresoModelView(AuditModelView):
    datamodel = SQLAInterface(Ingreso)

    list_title = "Ingresos de productos"
    show_title = "Detalle de ingreso"
    add_title = "Nuevo ingreso"
    edit_title = "Editar ingreso"

    list_columns = ["id", "fecha", "proveedor", "usuario", "observacion"]
    show_columns = list_columns + ["created_on", "changed_on"]
    add_columns = ["fecha", "proveedor", "observacion"]
    edit_columns = add_columns
    search_columns = ["proveedor", "observacion"]

    label_columns = {
        "fecha": "Fecha",
        "proveedor": "Proveedor",
        "usuario": "Registrado por",
        "observacion": "Observación",
        "created_on": "Creado",
        "changed_on": "Modificado",
    }

    def is_accessible(self):
        return can_manage_catalog()

    def pre_add(self, item):
        super().pre_add(item)
        item.usuario_id = g.user.id


class IngresoDetalleModelView(AuditModelView):
    datamodel = SQLAInterface(IngresoDetalle)
    base_permissions = ["can_list", "can_show", "can_add"]

    form_args = {
        "cantidad": {"validators": [NumberRange(min=1, message="La cantidad debe ser mayor a 0")]},
    }

    list_title = "Detalle de ingresos"
    add_title = "Agregar producto al ingreso"
    edit_title = "Editar detalle de ingreso"

    list_columns = [
        "ingreso",
        "producto",
        "cantidad",
        "precio_compra",
        "subtotal",
    ]
    add_columns = ["ingreso", "producto", "cantidad", "precio_compra"]
    edit_columns = add_columns

    label_columns = {
        "ingreso": "Ingreso",
        "producto": "Producto",
        "cantidad": "Cantidad",
        "precio_compra": "Precio de compra",
        "subtotal": "Subtotal",
    }

    def is_accessible(self):
        return can_manage_catalog()

    def pre_add(self, item):
        item.subtotal = calcular_subtotal(item.cantidad, item.precio_compra)

    def pre_update(self, item):
        item.subtotal = calcular_subtotal(item.cantidad, item.precio_compra)

    def post_add(self, item):
        try:
            aplicar_ingreso_detalle(item, g.user.id)
        except InventarioError as exc:
            flash(str(exc), "danger")
            raise

    def post_update(self, item):
        flash(
            "Para modificar cantidades de un ingreso ya aplicado, elimine y vuelva a registrar el detalle.",
            "warning",
        )

    def post_delete(self, item):
        try:
            revertir_ingreso_detalle(item, g.user.id)
        except InventarioError as exc:
            flash(str(exc), "danger")
            raise