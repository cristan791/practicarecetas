from datetime import date, timedelta

from flask import g
from flask_appbuilder import BaseView, expose
from flask_appbuilder.security.decorators import has_access

from app.constants import DIAS_ALERTA_VENCIMIENTO
from app.extensions import db
from app.models.producto import Producto
from app.permissions import can_manage_sales


class DashboardView(BaseView):
    route_base = "/dashboard"
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

        limite_vencimiento = date.today() + timedelta(days=DIAS_ALERTA_VENCIMIENTO)

        productos_agotados = (
            Producto.query.filter(Producto.estado.is_(True), Producto.stock <= 0)
            .order_by(Producto.nombre)
            .all()
        )
        productos_stock_bajo = (
            Producto.query.filter(
                Producto.estado.is_(True),
                Producto.stock > 0,
                Producto.stock <= Producto.stock_minimo,
            )
            .order_by(Producto.nombre)
            .all()
        )
        productos_por_vencer = (
            Producto.query.filter(
                Producto.estado.is_(True),
                Producto.fecha_vencimiento.isnot(None),
                Producto.fecha_vencimiento <= limite_vencimiento,
            )
            .order_by(Producto.fecha_vencimiento)
            .all()
        )

        total_productos = Producto.query.filter(Producto.estado.is_(True)).count()
        total_stock = db.session.query(db.func.coalesce(db.func.sum(Producto.stock), 0)).scalar()

        return self.render_template(
            "dashboard.html",
            productos_agotados=productos_agotados,
            productos_stock_bajo=productos_stock_bajo,
            productos_por_vencer=productos_por_vencer,
            total_productos=total_productos,
            total_stock=total_stock,
            dias_alerta=DIAS_ALERTA_VENCIMIENTO,
            user=g.user,
        )
