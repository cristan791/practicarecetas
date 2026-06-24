from app import create_app
from app.extensions import appbuilder

PERMISSIONS = [
    # Dashboard
    ("can_index", "DashboardView"),
    ("menu_access", "Panel principal"),
    # Inventario / Stock
    ("can_index", "InventarioView"),
    ("menu_access", "Stock e inventario"),
    # Ventas - Salida (cabecera)
    ("can_list", "SalidaModelView"),
    ("can_show", "SalidaModelView"),
    ("can_add", "SalidaModelView"),
    ("can_edit", "SalidaModelView"),
    ("menu_access", "Ventas"),
    # Ventas - SalidaDetalle (sin eliminar)
    ("can_list", "SalidaDetalleModelView"),
    ("can_show", "SalidaDetalleModelView"),
    ("can_add", "SalidaDetalleModelView"),
    ("can_edit", "SalidaDetalleModelView"),
    # Ventas - Clientes (solo ver y crear, no eliminar/editar)
    ("can_list", "ClienteModelView"),
    ("can_show", "ClienteModelView"),
    ("can_add", "ClienteModelView"),
    ("can_edit", "ClienteModelView"),
    ("menu_access", "Clientes"),
    # Inventario - Ingresos (cabecera)
    ("can_list", "IngresoModelView"),
    ("can_show", "IngresoModelView"),
    ("can_add", "IngresoModelView"),
    ("can_edit", "IngresoModelView"),
    # Inventario - IngresoDetalle (sin eliminar)
    ("can_list", "IngresoDetalleModelView"),
    ("can_show", "IngresoDetalleModelView"),
    ("can_add", "IngresoDetalleModelView"),
    ("can_edit", "IngresoDetalleModelView"),
    # Menú Inventario
    ("menu_access", "Inventario"),
    ("menu_access", "Ingresos"),
    ("menu_access", "Detalle ingresos"),
    ("menu_access", "Ventas"),
    ("menu_access", "Detalle ventas"),
]


def get_or_create_perm_view(sm, perm_name, view_menu_name):
    perm_view = sm.find_permission_view_menu(perm_name, view_menu_name)
    if perm_view:
        return perm_view

    perm = sm.find_permission(perm_name)
    if not perm:
        perm = sm.add_permission(perm_name)

    view_menu = sm.find_view_menu(view_menu_name)
    if not view_menu:
        view_menu = sm.add_view_menu(view_menu_name)

    return sm.add_permission_view_menu(perm_name, view_menu_name)


REMOVE_PERMISSIONS = [
    # Eliminar can_delete (el vendedor NO debe eliminar)
    ("can_delete", "SalidaModelView"),
    ("can_delete", "SalidaDetalleModelView"),
    ("can_delete", "ClienteModelView"),
    ("can_delete", "IngresoModelView"),
    ("can_delete", "IngresoDetalleModelView"),
]


def assign_permissions():
    app = create_app()
    with app.app_context():
        sm = appbuilder.sm
        vendedor = sm.find_role("Vendedor")
        if not vendedor:
            print("ERROR: Rol 'Vendedor' no encontrado")
            return

        # 1. Asignar permisos nuevos
        for perm_name, view_name in PERMISSIONS:
            perm_view = get_or_create_perm_view(sm, perm_name, view_name)
            if perm_view in vendedor.permissions:
                print(f"Ya existe: {perm_name} | {view_name}")
                continue
            sm.add_permission_role(vendedor, perm_view)
            print(f"Asignado: {perm_name} | {view_name}")

        # 2. Remover permisos de eliminación
        for perm_name, view_name in REMOVE_PERMISSIONS:
            perm_view = sm.find_permission_view_menu(perm_name, view_name)
            if perm_view and perm_view in vendedor.permissions:
                sm.del_permission_role(vendedor, perm_view)
                print(f"Removido: {perm_name} | {view_name}")
            else:
                print(f"No existe: {perm_name} | {view_name}")

        print("\nPermisos actualizados correctamente para el rol 'Vendedor'.")


if __name__ == "__main__":
    assign_permissions()