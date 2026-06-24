from datetime import datetime

from flask import g
from sqlalchemy import Column, DateTime, Integer


class AuditMixin:
    """Registro de auditoría: quién creó o modificó el registro."""

    created_on = Column(DateTime, default=datetime.utcnow, nullable=False)
    changed_on = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )
    created_by_fk = Column(Integer, nullable=True)
    changed_by_fk = Column(Integer, nullable=True)

    def set_audit_user(self):
        user = getattr(g, "user", None)
        if user and getattr(user, "is_authenticated", False):
            if not self.created_by_fk:
                self.created_by_fk = user.id
            self.changed_by_fk = user.id
