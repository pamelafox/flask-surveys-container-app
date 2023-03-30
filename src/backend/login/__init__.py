from flask import Blueprint

bp = Blueprint("login", __name__, template_folder="templates")

from backend.login import routes  # noqa

__all__ = [
    "routes",
]
