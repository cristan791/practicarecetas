import os

basedir = os.path.abspath(os.path.dirname(__file__))

SECRET_KEY = os.environ.get("SECRET_KEY", "lacteos-dev-secret-key-change-in-production")

SQLALCHEMY_DATABASE_URI = os.environ.get(
    "DATABASE_URL",
    "mysql+pymysql://root:@localhost:3306/lacteo",
)
SQLALCHEMY_TRACK_MODIFICATIONS = False

CSRF_ENABLED = True

APP_NAME = "Sistema Lácteos"
APP_ICON = "/static/img/logo.svg"

AUTH_TYPE = 1  # AUTH_DB

BABEL_DEFAULT_LOCALE = "es"
BABEL_DEFAULT_FOLDER = "translations"
LANGUAGES = {
    "es": {"flag": "es", "name": "Español"},
}

UPLOAD_FOLDER = os.path.join(basedir, "app", "static", "uploads")
IMG_UPLOAD_FOLDER = os.path.join(basedir, "app", "static", "uploads")
IMG_UPLOAD_URL = "/static/uploads/"
IMG_SIZE = (400, 400, True)

APP_THEME = "flatly.css"

GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
