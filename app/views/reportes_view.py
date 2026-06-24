from datetime import date, timedelta

from flask_appbuilder import BaseView, expose
from flask_appbuilder.security.decorators import has_access
from sqlalchemy import func

from app.constants import DIAS_ALERTA_VENCIMIENTO
from app.extensions import db
from app.models.cliente import Cliente
from app.models.ingreso import Ingreso
from app.models.producto import Producto
from app.models.salida import Salida, SalidaDetalle
from app.permissions import can_view_reports


class ReportesView(BaseView):
    route_base = "/reportes"
    default_view = "index"

    @expose("/")
    @has_access
    def index(self):
        if not can_view_reports():
            return self.render_template(
                "403.html",
                base_template=self.appbuilder.base_template,
                appbuilder=self.appbuilder,
            )

        hoy = date.today()
        inicio_semana = hoy - timedelta(days=hoy.weekday())
        inicio_mes = hoy.replace(day=1)
        limite_vencimiento = hoy + timedelta(days=DIAS_ALERTA_VENCIMIENTO)

        productos_mas_vendidos = (
            db.session.query(
                Producto.nombre,
                func.sum(SalidaDetalle.cantidad).label("total_vendido"),
                func.sum(SalidaDetalle.subtotal).label("monto_total"),
            )
            .join(SalidaDetalle, SalidaDetalle.producto_id == Producto.id)
            .group_by(Producto.id, Producto.nombre)
            .order_by(func.sum(SalidaDetalle.cantidad).desc())
            .limit(10)
            .all()
        )

        ventas_dia = (
            db.session.query(func.coalesce(func.sum(Salida.total), 0))
            .filter(func.date(Salida.fecha) == hoy)
            .scalar()
        )
        ventas_semana = (
            db.session.query(func.coalesce(func.sum(Salida.total), 0))
            .filter(Salida.fecha >= inicio_semana)
            .scalar()
        )
        ventas_mes = (
            db.session.query(func.coalesce(func.sum(Salida.total), 0))
            .filter(Salida.fecha >= inicio_mes)
            .scalar()
        )

        total_ingresos = Ingreso.query.count()
        inventario_actual = (
            db.session.query(
                Producto.nombre,
                Producto.stock,
                Producto.stock_minimo,
                Producto.fecha_vencimiento,
            )
            .filter(Producto.estado.is_(True))
            .order_by(Producto.nombre)
            .all()
        )
        proximos_vencer = (
            Producto.query.filter(
                Producto.estado.is_(True),
                Producto.fecha_vencimiento.isnot(None),
                Producto.fecha_vencimiento <= limite_vencimiento,
            )
            .order_by(Producto.fecha_vencimiento)
            .all()
        )

        clientes_frecuentes = (
            db.session.query(
                Cliente.nombre_completo,
                func.count(Salida.id).label("total_compras"),
                func.coalesce(func.sum(Salida.total), 0).label("monto_total"),
            )
            .join(Salida, Salida.cliente_id == Cliente.id)
            .group_by(Cliente.id, Cliente.nombre_completo)
            .order_by(func.count(Salida.id).desc())
            .limit(10)
            .all()
        )

        return self.render_template(
            "reportes.html",
            productos_mas_vendidos=productos_mas_vendidos,
            ventas_dia=ventas_dia,
            ventas_semana=ventas_semana,
            ventas_mes=ventas_mes,
            total_ingresos=total_ingresos,
            inventario_actual=inventario_actual,
            proximos_vencer=proximos_vencer,
            clientes_frecuentes=clientes_frecuentes,
        )
