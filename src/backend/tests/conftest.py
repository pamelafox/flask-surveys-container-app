import typing as t

import pytest
from flask import Flask
from flask.ctx import AppContext
from sqlalchemy_utils import create_database, database_exists, drop_database

from backend import create_app
from backend import db as _db
from backend.base_model import BaseModel


@pytest.fixture(scope="session", autouse=True)
def _manage_test_database():
    app = create_app(testing=True)

    with app.app_context():
        engines = _db.engines

    for engine in engines.values():
        if database_exists(engine.url):
            drop_database(engine.url)
        create_database(engine.url)

    BaseModel.metadata.create_all(engines["default"])

    yield

    for engine in engines.values():
        drop_database(engine.url)


@pytest.fixture
def app():
    app = create_app(config={"WTF_CSRF_ENABLED": False}, testing=True)

    with app.app_context():
        engines = _db.engines

    cleanup = []

    for key, engine in engines.items():
        connection = engine.connect()
        transaction = connection.begin()
        engines[key] = connection
        cleanup.append((key, engine, connection, transaction))

    yield app

    for key, engine, connection, transaction in cleanup:
        transaction.rollback()
        connection.close()
        engines[key] = engine


@pytest.fixture
def app_ctx(app: Flask) -> t.Iterator[AppContext]:
    with app.app_context() as ctx:
        yield ctx
