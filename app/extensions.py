from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_appbuilder import AppBuilder

from app.security import LacteosSecurityManager

db = SQLAlchemy()
migrate = Migrate()
appbuilder = AppBuilder(security_manager_class=LacteosSecurityManager)
