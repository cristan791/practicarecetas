from app.views.categoria_view import CategoriaModelView
from app.views.cliente_view import ClienteModelView
from app.views.dashboard_view import DashboardView
from app.views.envase_view import EnvaseModelView
from app.views.ingreso_view import IngresoDetalleModelView, IngresoModelView
from app.views.inventario_view import InventarioView
from app.views.movimiento_view import MovimientoInventarioModelView
from app.views.producto_view import ProductoModelView
from app.views.reportes_view import ReportesView
from app.views.salida_view import SalidaDetalleModelView, SalidaModelView

__all__ = [
    "CategoriaModelView",
    "EnvaseModelView",
    "ProductoModelView",
    "ClienteModelView",
    "IngresoModelView",
    "IngresoDetalleModelView",
    "SalidaModelView",
    "SalidaDetalleModelView",
    "MovimientoInventarioModelView",
    "DashboardView",
    "InventarioView",
    "ReportesView",
]
