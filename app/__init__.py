import os

from flask import Flask, redirect, url_for

from app.extensions import appbuilder, db, migrate


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object("config")

    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        appbuilder.init_app(app, db.session)

        from app import models  # noqa: F401
        from app.views import (
            CategoriaModelView,
            ClienteModelView,
            DashboardView,
            EnvaseModelView,
            IngresoDetalleModelView,
            IngresoModelView,
            InventarioView,
            MovimientoInventarioModelView,
            ProductoModelView,
            ReportesView,
            SalidaDetalleModelView,
            SalidaModelView,
        )

        db.create_all()
        appbuilder.sm.sync_roles()

        appbuilder.add_view(DashboardView, "Panel principal", icon="fa-dashboard")

        @app.route("/")
        def index():
            return redirect(url_for("DashboardView.index"))

        appbuilder.add_view(
            CategoriaModelView,
            "Categorías",
            icon="fa-folder-open",
            category="Catálogo",
        )
        appbuilder.add_view(
            EnvaseModelView,
            "Envases",
            icon="fa-cube",
            category="Catálogo",
        )
        appbuilder.add_view(
            ProductoModelView,
            "Productos",
            icon="fa-shopping-basket",
            category="Catálogo",
        )

        appbuilder.add_view(
            IngresoModelView,
            "Ingresos",
            icon="fa-arrow-down",
            category="Inventario",
        )
        appbuilder.add_view(
            IngresoDetalleModelView,
            "Detalle ingresos",
            icon="fa-list",
            category="Inventario",
        )
        appbuilder.add_view(
            SalidaModelView,
            "Ventas",
            icon="fa-arrow-up",
            category="Inventario",
        )
        appbuilder.add_view(
            SalidaDetalleModelView,
            "Detalle ventas",
            icon="fa-list-alt",
            category="Inventario",
        )
        appbuilder.add_view(
            InventarioView,
            "Stock e inventario",
            icon="fa-cubes",
            category="Inventario",
        )
        appbuilder.add_view(
            MovimientoInventarioModelView,
            "Historial movimientos",
            icon="fa-history",
            category="Inventario",
        )

        appbuilder.add_view(
            ClienteModelView,
            "Clientes",
            icon="fa-users",
            category="Ventas",
        )

        appbuilder.add_view(
            ReportesView,
            "Reportes",
            icon="fa-bar-chart",
            category="Reportes",
        )

        IngresoModelView.related_views = [IngresoDetalleModelView]
        IngresoDetalleModelView.related_views = [IngresoModelView]
        SalidaModelView.related_views = [SalidaDetalleModelView]
        SalidaDetalleModelView.related_views = [SalidaModelView]

    return app
