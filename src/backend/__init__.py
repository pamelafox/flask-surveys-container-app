import os

from flask import Flask
from flask_alembic import Alembic
from flask_sqlalchemy_lite import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

from .base_model import BaseModel

db = SQLAlchemy()
alembic = Alembic(metadatas=BaseModel.metadata)
csrf = CSRFProtect()


def create_app(config=None, testing=False):
    app = Flask(__name__)

    # If RUNNING_IN_PRODUCTION is defined, then we're running on Azure
    if "RUNNING_IN_PRODUCTION" not in os.environ:
        print("Loading settings.development and environment variables from .env")
        app.config.from_object("backend.settings.development")
    else:  # pragma: no cover
        print("Loading settings.production")
        app.config.from_object("backend.settings.production")
    database_uri = app.config.get("DATABASE_URI")
    if testing:
        # Replace the database name with a test database
        database_uri = database_uri.rsplit("/", 1)[0] + "/test"
    app.config.update(
        SQLALCHEMY_ENGINES={"default": database_uri},
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )
    if config:
        app.config.update(config)

    db.init_app(app)
    alembic.init_app(app)
    csrf.init_app(app)

    from backend.surveys import bp as surveys_bp

    app.register_blueprint(surveys_bp)

    return app
