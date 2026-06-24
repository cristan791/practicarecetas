#!/usr/bin/env python
"""Script para crear un usuario vendedor de prueba."""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.constants import ROLE_VENDEDOR
from app.extensions import db
from flask_appbuilder.security.sqla.models import User, Role


def create_vendedor():
    app = create_app()
    with app.app_context():
        # Obtener el rol Vendedor
        vendedor_role = db.session.query(Role).filter_by(name=ROLE_VENDEDOR).first()
        
        if not vendedor_role:
            print("❌ Rol 'Vendedor' no encontrado")
            return
        
        # Verificar si el usuario ya existe
        existing_user = db.session.query(User).filter_by(username="vendedor1").first()
        if existing_user:
            print("✓ Usuario 'vendedor1' ya existe")
            print(f"  Roles: {[r.name for r in existing_user.roles]}")
            return
        
        # Crear usuario usando el security manager
        from flask_appbuilder import AppBuilder
        
        sm = app.appbuilder.sm
        user = sm.add_user(
            username="vendedor1",
            first_name="Juan",
            last_name="Vendedor",
            email="vendedor@test.com",
            role=vendedor_role,
            password="vendedor123"
        )
        if not user:
            print("❌ No se pudo crear el usuario")
            return
        
        db.session.commit()
        
        print("✅ Usuario vendedor creado exitosamente")
        print(f"  Username: vendedor1")
        print(f"  Contraseña: vendedor123")
        print(f"  Rol: {ROLE_VENDEDOR}")


if __name__ == "__main__":
    create_vendedor()
