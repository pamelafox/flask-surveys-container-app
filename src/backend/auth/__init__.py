from flask import Blueprint

bp = Blueprint("auth", __name__, template_folder="templates")

from backend.auth import routes  # noqa

__all__ = [
    "routes",
]
