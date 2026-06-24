from flask import redirect, url_for
from flask_appbuilder import BaseView, expose
from flask_appbuilder.security.decorators import has_access

from app.permissions import can_manage_sales


class IndexView(BaseView):
    route_base = "/"
    default_view = "index"

    @expose("/")
    @has_access
    def index(self):
        # Redirigir automáticamente al dashboard si el usuario tiene permisos
        if can_manage_sales():
            return redirect(url_for("DashboardView.index"))
        
        # Si no tiene permisos, mostrar una página de bienvenida simple
        return self.render_template(
            "index.html",
            base_template=self.appbuilder.base_template,
            appbuilder=self.appbuilder,
        )
