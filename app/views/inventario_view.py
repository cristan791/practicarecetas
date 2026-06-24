from datetime import date, timedelta

from flask_appbuilder import BaseView, expose
from flask_appbuilder.security.decorators import has_access

from app.constants import DIAS_ALERTA_VENCIMIENTO
from app.models.producto import Producto
from app.permissions import can_manage_sales


class InventarioView(BaseView):
    route_base = "/inventario"
    default_view = "index"

    @expose("/")
    @has_access
    def index(self):
        if not can_manage_sales():
            return self.render_template(
                "403.html",
                base_template=self.appbuilder.base_template,
                appbuilder=self.appbuilder,
            )

        limite = date.today() + timedelta(days=DIAS_ALERTA_VENCIMIENTO)

        inventario = (
            Producto.query.filter(Producto.estado.is_(True))
            .order_by(Producto.nombre)
            .all()
        )
        agotados = [p for p in inventario if p.stock <= 0]
        stock_bajo = [p for p in inventario if 0 < p.stock <= p.stock_minimo]
        por_vencer = [
            p
            for p in inventario
            if p.fecha_vencimiento and p.fecha_vencimiento <= limite
        ]

        return self.render_template(
            "inventario.html",
            inventario=inventario,
            agotados=agotados,
            stock_bajo=stock_bajo,
            por_vencer=por_vencer,
            dias_alerta=DIAS_ALERTA_VENCIMIENTO,
        )
