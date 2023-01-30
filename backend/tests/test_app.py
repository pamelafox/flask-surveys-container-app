# Test the routes in routes.py using pytest
import pytest

import backend.surveys.models as models
from app import app


@pytest.fixture()
def fake_survey(session):
    survey = models.Survey(
        topic="ice cream",
        question="What's your favorite flavor?",
        options="chocolate\nvanilla",
    )
    session.add(survey)
    session.commit()
    return survey


def test_index_redirect():
    with app.test_client() as client:
        resp = client.get("/")
        assert resp.status_code == 302
        assert resp.location == "/surveys"


def test_surveys_list_page(fake_survey):
    with app.test_client() as client:
        resp = client.get("/surveys")
        assert resp.status_code == 200
        assert fake_survey.topic in str(resp.data)
