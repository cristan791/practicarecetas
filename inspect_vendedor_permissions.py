from app import create_app
from app.extensions import db
from flask_appbuilder.security.sqla.models import Role

app = create_app()
with app.app_context():
    vendedor = db.session.query(Role).filter_by(name='Vendedor').first()
    if not vendedor:
        print('NO_ROLE')
    else:
        print('ROLE', vendedor.name)
        perms = sorted(set((perm.name, perm.view_menu.name if perm.view_menu else None) for perm in vendedor.permissions))
        for name, view in perms:
            print(f'{name} | {view}')
