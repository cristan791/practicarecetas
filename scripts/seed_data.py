"""Script para cargar categorías, envases y roles de ejemplo."""

from app import create_app
from app.constants import ROLE_ADMIN, ROLE_SUPER_ADMIN, ROLE_VENDEDOR
from app.extensions import appbuilder, db
from app.models.categoria import Categoria
from app.models.envase import Envase


def seed():
    app = create_app()
    with app.app_context():
        for role_name in [ROLE_SUPER_ADMIN, ROLE_ADMIN, ROLE_VENDEDOR]:
            if not appbuilder.sm.find_role(role_name):
                appbuilder.sm.add_role(role_name)

        categorias = [
            ("Leche", "Productos derivados de leche líquida"),
            ("Yogur", "Yogures y fermentados"),
            ("Quesos", "Quesos frescos y madurados"),
            ("Mantequilla", "Mantequilla y margarina"),
            ("Bebidas lácteas", "Bebidas con base láctea"),
        ]
        for nombre, descripcion in categorias:
            if not Categoria.query.filter_by(nombre=nombre).first():
                db.session.add(Categoria(nombre=nombre, descripcion=descripcion, estado=True))

        envases = [
            ("Bolsa", "Envase flexible"),
            ("Botella", "Envase de vidrio o plástico"),
            ("Caja", "Envase de cartón"),
            ("Bidón", "Envase de gran volumen"),
            ("Vaso", "Envase individual"),
        ]
        for nombre, descripcion in envases:
            if not Envase.query.filter_by(nombre=nombre).first():
                db.session.add(Envase(nombre=nombre, descripcion=descripcion, estado=True))

        db.session.commit()
        print("Datos iniciales cargados correctamente.")


if __name__ == "__main__":
    seed()
