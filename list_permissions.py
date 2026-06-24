from app import create_app
from app.extensions import appbuilder

app = create_app()
with app.app_context():
    sm = appbuilder.sm
    print('---- VIEW MENUS ----')
    for vm in sorted(sm.get_session.query(sm.viewmenu_model).all(), key=lambda x: x.name):
        print(vm.name)
    print('\n---- PERMISSIONS ----')
    for perm in sorted(sm.get_session.query(sm.permission_model).all(), key=lambda x: x.name):
        print(perm.name)
