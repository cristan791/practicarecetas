from flask import g

from app.constants import ROLE_ADMIN, ROLE_SUPER_ADMIN, ROLE_VENDEDOR
from app.security import user_is_admin, user_is_super_admin, user_is_vendedor


def can_manage_catalog() -> bool:
    user = getattr(g, "user", None)
    return (
        user_is_admin(user)
        or user_is_super_admin(user)
        or user_is_vendedor(user)
    )


def can_manage_sales() -> bool:
    user = getattr(g, "user", None)
    return (
        user_is_admin(user)
        or user_is_super_admin(user)
        or user_is_vendedor(user)
    )


def can_view_inventory() -> bool:
    user = getattr(g, "user", None)
    return (
        user_is_admin(user)
        or user_is_super_admin(user)
        or user_is_vendedor(user)
    )


def can_view_dashboard() -> bool:
    user = getattr(g, "user", None)
    return (
        user_is_admin(user)
        or user_is_super_admin(user)
        or user_is_vendedor(user)
    )


def can_view_reports() -> bool:
    user = getattr(g, "user", None)
    return user_is_admin(user) or user_is_super_admin(user)


def can_manage_users() -> bool:
    return user_is_super_admin(getattr(g, "user", None))