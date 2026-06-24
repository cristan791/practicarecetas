#!/usr/bin/env python
"""Script para listar usuarios y sus roles."""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.extensions import db
from flask_appbuilder.security.sqla.models import User


def list_users():
    app = create_app()
    with app.app_context():
        users = db.session.query(User).all()
        
        if not users:
            print("No hay usuarios")
            return
        
        print("Usuarios del sistema:")
        print("=" * 60)
        for user in users:
            roles = ", ".join([r.name for r in user.roles])
            print(f"  • {user.username:20} | {user.email:25} | Roles: {roles}")
            print(f"    Activo: {user.active}")


if __name__ == "__main__":
    list_users()
