#!/usr/bin/env python
"""Script para asignar rol Super Administrador al usuario admin."""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.constants import ROLE_SUPER_ADMIN
from app.extensions import db
from flask_appbuilder.security.sqla.models import User, Role


def assign_super_admin_role():
    app = create_app()
    with app.app_context():
        # Obtener el usuario admin
        admin_user = db.session.query(User).filter_by(username="admin").first()
        
        if not admin_user:
            print("❌ Usuario 'admin' no encontrado")
            return
        
        print(f"Usuario encontrado: {admin_user.first_name} {admin_user.last_name}")
        print(f"Roles actuales: {[r.name for r in admin_user.roles]}")
        
        # Obtener el rol Super Administrador
        super_admin_role = db.session.query(Role).filter_by(name=ROLE_SUPER_ADMIN).first()
        
        if not super_admin_role:
            print("❌ Rol 'Super Administrador' no encontrado")
            return
        
        # Verificar si el usuario ya tiene el rol
        if super_admin_role in admin_user.roles:
            print(f"✓ El usuario 'admin' ya tiene el rol '{ROLE_SUPER_ADMIN}'")
            return
        
        # Asignar el rol
        admin_user.roles.append(super_admin_role)
        db.session.commit()
        
        print(f"✅ Rol '{ROLE_SUPER_ADMIN}' asignado al usuario 'admin'")
        print(f"\nRoles del usuario admin ahora:")
        for role in admin_user.roles:
            print(f"  - {role.name}")


if __name__ == "__main__":
    assign_super_admin_role()
