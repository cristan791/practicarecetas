from flask import g
from flask_appbuilder.models.sqla.interface import SQLAInterface

from app.models.producto import Producto
from app.permissions import can_manage_catalog, can_manage_sales
from app.views.base import AuditModelView


class ProductoModelView(AuditModelView):
    datamodel = SQLAInterface(Producto)

    list_title = "Productos"
    show_title = "Detalle de producto"
    add_title = "Nuevo producto"
    edit_title = "Editar producto"

    list_columns = [
        "nombre",
        "categoria",
        "envase",
        "precio_compra",
        "precio_venta",
        "stock",
        "stock_minimo",
        "fecha_vencimiento",
        "estado",
    ]
    show_columns = list_columns + ["descripcion", "codigo_barras", "imagen", "created_on"]
    add_columns = [
        "nombre",
        "descripcion",
        "precio_compra",
        "precio_venta",
        "categoria",
        "envase",
        "fecha_vencimiento",
        "codigo_barras",
        "imagen",
        "stock_minimo",
        "estado",
    ]
    edit_columns = add_columns
    search_columns = ["nombre", "codigo_barras", "categoria", "envase"]

    label_columns = {
        "nombre": "Nombre",
        "descripcion": "Descripción",
        "precio_compra": "Precio compra",
        "precio_venta": "Precio venta",
        "categoria": "Categoría",
        "envase": "Envase",
        "fecha_vencimiento": "Vencimiento",
        "codigo_barras": "Código de barras",
        "imagen": "Imagen (URL/ruta)",
        "stock": "Stock actual",
        "stock_minimo": "Stock mínimo",
        "estado": "Activo",
        "created_on": "Creado",
    }

    def is_accessible(self):
        return can_manage_sales()

    @property
    def can_add(self):
        return can_manage_catalog()

    @property
    def can_edit(self):
        return can_manage_catalog()

    @property
    def can_delete(self):
        return can_manage_catalog()

    def pre_add(self, item):
        super().pre_add(item)
        item.stock = item.stock or 0
