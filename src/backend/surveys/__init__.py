from flask import Blueprint

bp = Blueprint("surveys", __name__, template_folder="templates")

from backend.surveys import routes  # noqa

__all__ = [
    "routes",
]
