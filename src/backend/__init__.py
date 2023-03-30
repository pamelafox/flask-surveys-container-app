import os

import identity
import identity.web
from flask import Flask
from flask_migrate import Migrate
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from werkzeug.middleware.proxy_fix import ProxyFix

db = SQLAlchemy()
migrate = Migrate()
csrf = CSRFProtect()
session = Session()


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

    # This section is needed for url_for("foo", _external=True) to automatically
    # generate http scheme when this sample is running on localhost,
    # and to generate https scheme when it is deployed behind reversed proxy.
    # See also https://flask.palletsprojects.com/en/2.2.x/deploying/proxy_fix/
    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)
    session.init_app(app)

    app.config.update(
        AUTH=identity.web.Auth(
            session=session,
            authority=app.config.get("AUTHORITY"),
            client_id=app.config["CLIENT_ID"],
            client_credential=app.config["CLIENT_SECRET"],
        )
    )

    from backend.surveys import bp as login_bp
    from backend.surveys import bp as surveys_bp

    app.register_blueprint(surveys_bp)
    app.register_blueprint(login_bp)

    return app
