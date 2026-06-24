#!/usr/bin/env python
"""Script para cargar datos iniciales completos en la BD."""
import sys
import os
from datetime import datetime, timedelta

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.constants import ROLE_ADMIN, ROLE_SUPER_ADMIN, ROLE_VENDEDOR
from app.extensions import appbuilder, db
from app.models.categoria import Categoria
from app.models.envase import Envase
from app.models.producto import Producto
from app.models.cliente import Cliente
from app.models.ingreso import Ingreso, IngresoDetalle
from app.models.salida import Salida, SalidaDetalle
from app.models.movimiento import MovimientoInventario


def seed():
    app = create_app()
    with app.app_context():
        print("=" * 60)
        print("CARGANDO DATOS INICIALES")
        print("=" * 60)

        # ─── 1. ROLES ───────────────────────────────────────────────
        print("\n📋 Sincronizando roles...")
        for role_name in [ROLE_SUPER_ADMIN, ROLE_ADMIN, ROLE_VENDEDOR]:
            if not appbuilder.sm.find_role(role_name):
                appbuilder.sm.add_role(role_name)
                print(f"  ✓ Rol '{role_name}' creado")
            else:
                print(f"  ✓ Rol '{role_name}' ya existe")

        # ─── 2. USUARIOS ────────────────────────────────────────────
        print("\n👤 Creando usuarios...")
        sm = appbuilder.sm

        admin_role = sm.find_role(ROLE_ADMIN)
        vendedor_role = sm.find_role(ROLE_VENDEDOR)

        users_data = [
            ("admin", "Admin", "Principal", "admin@lacteos.com", admin_role, "admin123"),
            ("vendedor1", "Juan", "Vendedor", "vendedor@test.com", vendedor_role, "vendedor123"),
            ("vendedor2", "María", "Ventas", "maria@test.com", vendedor_role, "vendedor123"),
        ]

        created_users = {}
        for username, first_name, last_name, email, role, password in users_data:
            existing = sm.find_user(username=username)
            if not existing:
                user = sm.add_user(
                    username=username,
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    role=role,
                    password=password,
                )
                if user:
                    created_users[username] = user
                    print(f"  ✓ Usuario '{username}' creado ({password})")
            else:
                created_users[username] = existing
                print(f"  ✓ Usuario '{username}' ya existe")

        # ─── 3. CATEGORÍAS ──────────────────────────────────────────
        print("\n📦 Cargando categorías...")
        categorias_data = [
            ("Leche", "Productos derivados de leche líquida"),
            ("Yogur", "Yogures y fermentados"),
            ("Quesos", "Quesos frescos y madurados"),
            ("Mantequilla", "Mantequilla y margarina"),
            ("Bebidas lácteas", "Bebidas con base láctea"),
        ]
        created_categorias = {}
        for nombre, descripcion in categorias_data:
            cat = Categoria.query.filter_by(nombre=nombre).first()
            if not cat:
                cat = Categoria(nombre=nombre, descripcion=descripcion, estado=True)
                db.session.add(cat)
                db.session.flush()
                print(f"  ✓ Categoría '{nombre}' creada")
            else:
                print(f"  ✓ Categoría '{nombre}' ya existe")
            created_categorias[nombre] = cat

        # ─── 4. ENVASES ─────────────────────────────────────────────
        print("\n🧴 Cargando envases...")
        envases_data = [
            ("Bolsa", "Envase flexible"),
            ("Botella", "Envase de vidrio o plástico"),
            ("Caja", "Envase de cartón"),
            ("Bidón", "Envase de gran volumen"),
            ("Vaso", "Envase individual"),
        ]
        created_envases = {}
        for nombre, descripcion in envases_data:
            env = Envase.query.filter_by(nombre=nombre).first()
            if not env:
                env = Envase(nombre=nombre, descripcion=descripcion, estado=True)
                db.session.add(env)
                db.session.flush()
                print(f"  ✓ Envase '{nombre}' creado")
            else:
                print(f"  ✓ Envase '{nombre}' ya existe")
            created_envases[nombre] = env

        # ─── 5. PRODUCTOS ───────────────────────────────────────────
        print("\n🥛 Cargando productos...")
        productos_data = [
            ("Leche Integral 1L", "Leche fresca integral", "Leche", "Botella", 50, 10, 8.50, 15.00),
            ("Leche Deslactosada 1L", "Leche sin lactosa", "Leche", "Botella", 30, 5, 9.00, 16.00),
            ("Yogur Natural 500g", "Yogur natural sin azúcar", "Yogur", "Vaso", 40, 5, 5.00, 10.00),
            ("Yogur Frutilla 500g", "Yogur sabor frutilla", "Yogur", "Vaso", 35, 5, 5.50, 11.00),
            ("Queso Fresco 500g", "Queso fresco artesanal", "Quesos", "Caja", 20, 5, 12.00, 20.00),
            ("Queso Mozzarella 500g", "Queso mozzarella", "Quesos", "Caja", 15, 3, 14.00, 24.00),
            ("Mantequilla 200g", "Mantequilla sin sal", "Mantequilla", "Bolsa", 25, 5, 6.00, 12.00),
            ("Mantequilla Light 200g", "Mantequilla baja en grasa", "Mantequilla", "Bolsa", 20, 3, 6.50, 13.00),
            ("Bebida Láctea Chocolate 1L", "Bebida de chocolate", "Bebidas lácteas", "Botella", 40, 8, 7.00, 14.00),
            ("Bebida Láctea Vainilla 1L", "Bebida de vainilla", "Bebidas lácteas", "Botella", 35, 5, 7.00, 14.00),
        ]
        created_productos = {}
        for nombre, descripcion, cat_nombre, env_nombre, stock, stock_min, p_compra, p_venta in productos_data:
            prod = Producto.query.filter_by(nombre=nombre).first()
            if not prod:
                prod = Producto(
                    nombre=nombre,
                    descripcion=descripcion,
                    categoria_id=created_categorias[cat_nombre].id,
                    envase_id=created_envases[env_nombre].id,
                    stock=stock,
                    stock_minimo=stock_min,
                    precio_compra=p_compra,
                    precio_venta=p_venta,
                    estado=True,
                )
                db.session.add(prod)
                db.session.flush()
                print(f"  ✓ Producto '{nombre}' creado (stock: {stock})")
            else:
                print(f"  ✓ Producto '{nombre}' ya existe (stock: {prod.stock})")
            created_productos[nombre] = prod

        # ─── 6. CLIENTES ────────────────────────────────────────────
        print("\n👥 Cargando clientes...")
        clientes_data = [
            ("Carlos López", "1234567", "777-12345", "Calle Bolívar #123", "carlos@email.com"),
            ("Ana Martínez", "7654321", "777-67890", "Av. 16 de Julio #456", "ana@email.com"),
            ("Pedro Rodríguez", "1112233", "777-11122", "Calle Potosí #789", "pedro@email.com"),
            ("Lucía Fernández", "4455667", "777-33445", "Av. Arce #101", "lucia@email.com"),
            ("Miguel Ángel", "9988776", "777-55667", "Calle Linares #202", "miguel@email.com"),
        ]
        created_clientes = {}
        for nombre, ci, telefono, direccion, correo in clientes_data:
            cli = Cliente.query.filter_by(nombre_completo=nombre).first()
            if not cli:
                cli = Cliente(
                    nombre_completo=nombre,
                    ci_nit=ci,
                    telefono=telefono,
                    direccion=direccion,
                    correo=correo,
                    estado=True,
                )
                db.session.add(cli)
                db.session.flush()
                print(f"  ✓ Cliente '{nombre}' creado")
            else:
                print(f"  ✓ Cliente '{nombre}' ya existe")
            created_clientes[nombre] = cli

        db.session.commit()

        # ─── 7. INGRESOS (compras a proveedores) ────────────────────
        print("\n📥 Cargando ingresos (compras)...")
        admin_user = created_users.get("admin")
        admin_id = admin_user.id if admin_user else 1

        ingresos_data = [
            {
                "fecha": datetime.utcnow() - timedelta(days=10),
                "proveedor": "Distribuidora Láctea SRL",
                "detalles": [
                    ("Leche Integral 1L", 30, 8.00),
                    ("Leche Deslactosada 1L", 20, 8.50),
                    ("Yogur Natural 500g", 25, 4.50),
                ],
            },
            {
                "fecha": datetime.utcnow() - timedelta(days=7),
                "proveedor": "Quesería Artesanal Bolivia",
                "detalles": [
                    ("Queso Fresco 500g", 15, 11.00),
                    ("Queso Mozzarella 500g", 10, 13.00),
                    ("Mantequilla 200g", 20, 5.50),
                ],
            },
            {
                "fecha": datetime.utcnow() - timedelta(days=5),
                "proveedor": "Lácteos del Valle",
                "detalles": [
                    ("Bebida Láctea Chocolate 1L", 25, 6.50),
                    ("Bebida Láctea Vainilla 1L", 20, 6.50),
                    ("Yogur Frutilla 500g", 20, 5.00),
                    ("Mantequilla Light 200g", 15, 6.00),
                ],
            },
            {
                "fecha": datetime.utcnow() - timedelta(days=2),
                "proveedor": "Distribuidora Láctea SRL",
                "detalles": [
                    ("Leche Integral 1L", 40, 8.00),
                    ("Yogur Natural 500g", 20, 4.50),
                    ("Queso Fresco 500g", 10, 11.00),
                ],
            },
        ]

        for ing_data in ingresos_data:
            ingreso = Ingreso(
                fecha=ing_data["fecha"],
                proveedor=ing_data["proveedor"],
                usuario_id=admin_id,
            )
            db.session.add(ingreso)
            db.session.flush()

            for prod_nombre, cantidad, precio in ing_data["detalles"]:
                producto = created_productos.get(prod_nombre)
                if not producto:
                    continue
                subtotal = cantidad * precio
                detalle = IngresoDetalle(
                    ingreso_id=ingreso.id,
                    producto_id=producto.id,
                    cantidad=cantidad,
                    precio_compra=precio,
                    subtotal=subtotal,
                )
                db.session.add(detalle)

                # Actualizar stock
                stock_anterior = producto.stock
                producto.stock = stock_anterior + cantidad
                producto.precio_compra = precio

                # Registrar movimiento
                mov = MovimientoInventario(
                    producto_id=producto.id,
                    tipo="INGRESO",
                    cantidad=cantidad,
                    stock_anterior=stock_anterior,
                    stock_nuevo=producto.stock,
                    referencia_tipo="ingreso",
                    referencia_id=ingreso.id,
                    usuario_id=admin_id,
                    observacion=f"Ingreso #{ingreso.id} - {ing_data['proveedor']}",
                )
                db.session.add(mov)

            print(f"  ✓ Ingreso #{ingreso.id} - {ing_data['proveedor']} ({len(ing_data['detalles'])} productos)")

        db.session.commit()

        # ─── 8. SALIDAS (ventas a clientes) ─────────────────────────
        print("\n📤 Cargando salidas (ventas)...")
        vendedor1 = created_users.get("vendedor1")
        vendedor2 = created_users.get("vendedor2")
        vendedor1_id = vendedor1.id if vendedor1 else 2
        vendedor2_id = vendedor2.id if vendedor2 else 3

        salidas_data = [
            {
                "fecha": datetime.utcnow() - timedelta(days=8),
                "cliente": "Carlos López",
                "vendedor_id": vendedor1_id,
                "detalles": [
                    ("Leche Integral 1L", 3, 15.00),
                    ("Yogur Natural 500g", 2, 10.00),
                    ("Queso Fresco 500g", 1, 20.00),
                ],
            },
            {
                "fecha": datetime.utcnow() - timedelta(days=6),
                "cliente": "Ana Martínez",
                "vendedor_id": vendedor2_id,
                "detalles": [
                    ("Mantequilla 200g", 2, 12.00),
                    ("Bebida Láctea Chocolate 1L", 4, 14.00),
                    ("Yogur Frutilla 500g", 3, 11.00),
                ],
            },
            {
                "fecha": datetime.utcnow() - timedelta(days=4),
                "cliente": "Pedro Rodríguez",
                "vendedor_id": vendedor1_id,
                "detalles": [
                    ("Leche Integral 1L", 6, 15.00),
                    ("Leche Deslactosada 1L", 2, 16.00),
                    ("Queso Mozzarella 500g", 1, 24.00),
                    ("Mantequilla Light 200g", 1, 13.00),
                ],
            },
            {
                "fecha": datetime.utcnow() - timedelta(days=3),
                "cliente": "Lucía Fernández",
                "vendedor_id": vendedor2_id,
                "detalles": [
                    ("Yogur Natural 500g", 4, 10.00),
                    ("Yogur Frutilla 500g", 2, 11.00),
                    ("Bebida Láctea Vainilla 1L", 3, 14.00),
                ],
            },
            {
                "fecha": datetime.utcnow() - timedelta(days=1),
                "cliente": "Miguel Ángel",
                "vendedor_id": vendedor1_id,
                "detalles": [
                    ("Leche Integral 1L", 2, 15.00),
                    ("Queso Fresco 500g", 2, 20.00),
                    ("Mantequilla 200g", 3, 12.00),
                    ("Bebida Láctea Chocolate 1L", 2, 14.00),
                ],
            },
        ]

        for sal_data in salidas_data:
            cliente = created_clientes.get(sal_data["cliente"])
            if not cliente:
                continue

            salida = Salida(
                fecha=sal_data["fecha"],
                cliente_id=cliente.id,
                vendedor_id=sal_data["vendedor_id"],
                total=0,
            )
            db.session.add(salida)
            db.session.flush()

            total = 0
            for prod_nombre, cantidad, precio in sal_data["detalles"]:
                producto = created_productos.get(prod_nombre)
                if not producto:
                    continue

                # Verificar stock
                if producto.stock < cantidad:
                    print(f"  ⚠ Stock insuficiente para '{prod_nombre}': disponible {producto.stock}, solicitado {cantidad}")
                    continue

                subtotal = cantidad * precio
                total += subtotal

                detalle = SalidaDetalle(
                    salida_id=salida.id,
                    producto_id=producto.id,
                    cantidad=cantidad,
                    precio=precio,
                    subtotal=subtotal,
                )
                db.session.add(detalle)

                # Actualizar stock
                stock_anterior = producto.stock
                producto.stock = stock_anterior - cantidad

                # Registrar movimiento
                mov = MovimientoInventario(
                    producto_id=producto.id,
                    tipo="SALIDA",
                    cantidad=cantidad,
                    stock_anterior=stock_anterior,
                    stock_nuevo=producto.stock,
                    referencia_tipo="salida",
                    referencia_id=salida.id,
                    usuario_id=sal_data["vendedor_id"],
                    observacion=f"Venta #{salida.id} - {sal_data['cliente']}",
                )
                db.session.add(mov)

            salida.total = total
            print(f"  ✓ Venta #{salida.id} - {sal_data['cliente']} (Bs. {total:.2f})")

        db.session.commit()

        # ─── RESUMEN ────────────────────────────────────────────────
        print("\n" + "=" * 60)
        print("✅ CARGA DE DATOS COMPLETADA")
        print("=" * 60)
        print(f"\n  Usuarios:")
        print(f"    • admin / admin123 (Administrador)")
        print(f"    • vendedor1 / vendedor123 (Vendedor)")
        print(f"    • vendedor2 / vendedor123 (Vendedor)")
        print(f"\n  Categorías: {Categoria.query.count()}")
        print(f"  Envases: {Envase.query.count()}")
        print(f"  Productos: {Producto.query.count()}")
        print(f"  Clientes: {Cliente.query.count()}")
        print(f"  Ingresos: {Ingreso.query.count()}")
        print(f"  Salidas: {Salida.query.count()}")
        print(f"  Movimientos: {MovimientoInventario.query.count()}")
        print("=" * 60)


if __name__ == "__main__":
    seed()