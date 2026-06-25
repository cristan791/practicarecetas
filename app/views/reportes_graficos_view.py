from datetime import date, timedelta

from flask_appbuilder import BaseView, expose
from flask_appbuilder.security.decorators import has_access
from sqlalchemy import func

from app.constants import DIAS_ALERTA_VENCIMIENTO
from app.extensions import db
from app.models.cliente import Cliente
from app.models.ingreso import Ingreso, IngresoDetalle
from app.models.producto import Producto
from app.models.salida import Salida, SalidaDetalle
from app.permissions import can_view_reports


class ReportesGraficosView(BaseView):
    route_base = "/reportes-graficos"
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

        # --- Ventas por período ---
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

        # --- Productos más vendidos (top 5 para gráfico) ---
        productos_mas_vendidos = (
            db.session.query(
                Producto.nombre,
                func.sum(SalidaDetalle.cantidad).label("total_vendido"),
                func.sum(SalidaDetalle.subtotal).label("monto_total"),
            )
            .join(SalidaDetalle, SalidaDetalle.producto_id == Producto.id)
            .group_by(Producto.id, Producto.nombre)
            .order_by(func.sum(SalidaDetalle.cantidad).desc())
            .limit(5)
            .all()
        )

        # --- Clientes frecuentes (top 5 para gráfico) ---
        clientes_frecuentes = (
            db.session.query(
                Cliente.nombre_completo,
                func.count(Salida.id).label("total_compras"),
                func.coalesce(func.sum(Salida.total), 0).label("monto_total"),
            )
            .join(Salida, Salida.cliente_id == Cliente.id)
            .group_by(Cliente.id, Cliente.nombre_completo)
            .order_by(func.count(Salida.id).desc())
            .limit(5)
            .all()
        )

        # --- Ventas por día de la semana (últimos 7 días) ---
        ventas_por_dia = []
        dias_etiquetas = []
        for i in range(6, -1, -1):
            dia = hoy - timedelta(days=i)
            total = (
                db.session.query(func.coalesce(func.sum(Salida.total), 0))
                .filter(func.date(Salida.fecha) == dia)
                .scalar()
            )
            ventas_por_dia.append(float(total))
            dias_etiquetas.append(dia.strftime("%d/%m"))

        # --- Stock por categoría ---
        stock_por_categoria = (
            db.session.query(
                Producto.categoria_id,
                func.sum(Producto.stock).label("total_stock"),
            )
            .filter(Producto.estado.is_(True))
            .group_by(Producto.categoria_id)
            .all()
        )
        # Obtener nombres de categorías
        from app.models.categoria import Categoria

        categorias_dict = {c.id: c.nombre for c in Categoria.query.all()}
        categorias_labels = []
        categorias_data = []
        for row in stock_por_categoria:
            categorias_labels.append(categorias_dict.get(row.categoria_id, f"Cat #{row.categoria_id}"))
            categorias_data.append(int(row.total_stock))

        # --- Estado del inventario ---
        total_productos = Producto.query.filter(Producto.estado.is_(True)).count()
        productos_agotados = Producto.query.filter(
            Producto.estado.is_(True), Producto.stock <= 0
        ).count()
        productos_stock_bajo = Producto.query.filter(
            Producto.estado.is_(True),
            Producto.stock > 0,
            Producto.stock <= Producto.stock_minimo,
        ).count()
        productos_ok = total_productos - productos_agotados - productos_stock_bajo

        # --- Ingresos vs Ventas (últimos 6 meses) ---
        meses_etiquetas = []
        ingresos_mensuales = []
        ventas_mensuales = []
        for i in range(5, -1, -1):
            mes_inicio = (hoy.replace(day=1) - timedelta(days=30 * i)).replace(day=1)
            if mes_inicio.month == 12:
                mes_fin = mes_inicio.replace(year=mes_inicio.year + 1, month=1)
            else:
                mes_fin = mes_inicio.replace(month=mes_inicio.month + 1)

            total_ing = (
                db.session.query(func.coalesce(func.sum(IngresoDetalle.subtotal), 0))
                .select_from(Ingreso)
                .join(IngresoDetalle, IngresoDetalle.ingreso_id == Ingreso.id)
                .filter(Ingreso.fecha >= mes_inicio, Ingreso.fecha < mes_fin)
                .scalar()
            )
            total_ven = (
                db.session.query(func.coalesce(func.sum(Salida.total), 0))
                .filter(Salida.fecha >= mes_inicio, Salida.fecha < mes_fin)
                .scalar()
            )
            ingresos_mensuales.append(float(total_ing))
            ventas_mensuales.append(float(total_ven))
            meses_etiquetas.append(mes_inicio.strftime("%b %y"))

        return self.render_template(
            "reportes_graficos.html",
            ventas_dia=float(ventas_dia),
            ventas_semana=float(ventas_semana),
            ventas_mes=float(ventas_mes),
            productos_mas_vendidos=productos_mas_vendidos,
            clientes_frecuentes=clientes_frecuentes,
            ventas_por_dia=ventas_por_dia,
            dias_etiquetas=dias_etiquetas,
            categorias_labels=categorias_labels,
            categorias_data=categorias_data,
            productos_ok=productos_ok,
            productos_agotados=productos_agotados,
            productos_stock_bajo=productos_stock_bajo,
            meses_etiquetas=meses_etiquetas,
            ingresos_mensuales=ingresos_mensuales,
            ventas_mensuales=ventas_mensuales,
        )