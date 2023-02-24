import os

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

db = SQLAlchemy()
migrate = Migrate()
csrf = CSRFProtect()


def create_app(config=None):
    app = Flask(__name__)

    # If RUNNING_IN_PRODUCTION is defined, then we're running on Azure
    if "RUNNING_IN_PRODUCTION" not in os.environ:
        print("Loading settings.development and environment variables from .env")
        app.config.from_object("backend.settings.development")
    else:  # pragma: no cover
        print("Loading settings.production")
        app.config.from_object("backend.settings.production")
    app.config.update(
        SQLALCHEMY_DATABASE_URI=app.config.get("DATABASE_URI"),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )
    if config:
        app.config.update(config)

    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)

    from backend.surveys import bp as surveys_bp

    app.register_blueprint(surveys_bp)

    return app
