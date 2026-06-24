from flask import flash
from flask_appbuilder.security.sqla.manager import SecurityManager

from app.constants import (
    ALL_ROLES,
    ROLE_ADMIN,
    ROLE_SUPER_ADMIN,
    ROLE_VENDEDOR,
)


def user_has_role(user, role_name: str) -> bool:
    """Verifica si el usuario tiene un rol específico."""
    if not user or not getattr(user, "is_authenticated", False):
        return False

    return any(role.name == role_name for role in user.roles)


def user_is_super_admin(user) -> bool:
    """Verifica si el usuario es Super Administrador."""
    return user_has_role(user, ROLE_SUPER_ADMIN)


def user_is_admin(user) -> bool:
    """Verifica si el usuario es Administrador o Super Administrador."""
    return (
        user_is_super_admin(user)
        or user_has_role(user, ROLE_ADMIN)
    )


def user_is_vendedor(user) -> bool:
    """Verifica si el usuario es Vendedor."""
    return user_has_role(user, ROLE_VENDEDOR)


class LacteosSecurityManager(SecurityManager):
    """Gestor de seguridad para el sistema de productos lácteos."""

    def sync_roles(self):
        for role_name in ALL_ROLES:
            if not self.find_role(role_name):
                self.add_role(role_name)

    def has_role(self, role_name: str) -> bool:
        from flask import g
        return user_has_role(getattr(g, "user", None), role_name)

    def is_super_admin(self) -> bool:
        from flask import g
        return user_is_super_admin(getattr(g, "user", None))

    def is_business_admin(self) -> bool:
        from flask import g
        return user_is_admin(getattr(g, "user", None))

    def is_vendedor(self) -> bool:
        from flask import g
        return user_is_vendedor(getattr(g, "user", None))

    def get_user_roles(self, user):
        roles = super().get_user_roles(user)

        if user_is_super_admin(user):
            return roles

        return [
            role
            for role in roles
            if role.name != ROLE_SUPER_ADMIN
        ]

    def add_user(
        self,
        username,
        first_name,
        last_name,
        email,
        role,
        password=""
    ):
        if (
            role
            and role.name == ROLE_SUPER_ADMIN
            and not self.is_super_admin()
        ):
            flash(
                "No tiene permisos para crear Super Administradores.",
                "danger",
            )
            return False

        return super().add_user(
            username,
            first_name,
            last_name,
            email,
            role,
            password,
        )

    def edit_user(self, user):
        if (
            user_has_role(user, ROLE_SUPER_ADMIN)
            and not self.is_super_admin()
        ):
            flash(
                "No tiene permisos para editar Super Administradores.",
                "danger",
            )
            return False

        return super().edit_user(user)

    def del_user(self, user):
        if (
            user_has_role(user, ROLE_SUPER_ADMIN)
            and not self.is_super_admin()
        ):
            flash(
                "No tiene permisos para eliminar Super Administradores.",
                "danger",
            )
            return False

        return super().del_user(user)