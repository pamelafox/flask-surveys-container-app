from flask import Blueprint

bp = Blueprint("surveys", __name__)

from backend.surveys import routes  # noqa

__all__ = [
    "routes",
]
