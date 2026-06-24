from flask_appbuilder import ModelView


class AuditModelView(ModelView):
    """Vista base con auditoría automática en altas y modificaciones."""

    def pre_add(self, item):
        if hasattr(item, "set_audit_user"):
            item.set_audit_user()

    def pre_update(self, item):
        if hasattr(item, "set_audit_user"):
            item.set_audit_user()
