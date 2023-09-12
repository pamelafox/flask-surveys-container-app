# Test the routes in routes.py using pytest
import pytest
from sqlalchemy import func, select
from werkzeug.datastructures import ImmutableMultiDict

import backend.surveys.models as models


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


@pytest.fixture()
def client(app):
    return app.test_client()


def test_index_redirect(client):
    resp = client.get("/")
    assert resp.status_code == 302
    assert resp.location == "/surveys"


def test_surveys_list_page(client, fake_survey):
    resp = client.get("/surveys")
    assert resp.status_code == 200
    assert fake_survey.topic in str(resp.data)


def test_surveys_create_page(client):
    resp = client.get("/surveys/new")
    assert resp.status_code == 200
    assert b"Create New Survey" in resp.data


def test_surveys_create_handler(client, session):
    resp = client.post(
        "/surveys",
        data={
            "survey_question": "What's your favorite color?",
            "survey_topic": "colors",
            "survey_options": "red\nblue\nyellow",
        },
    )
    # Find the created survey in the database
    survey = session.scalars(select(models.Survey).filter_by(topic="colors").limit(1)).first()
    # Make sure it redirected to that survey
    assert resp.status_code == 302
    assert resp.location == f"/surveys/{survey.id}"


def test_survey_page(client, fake_survey):
    resp = client.get(f"/surveys/{fake_survey.id}")
    assert resp.status_code == 200
    assert fake_survey.topic in str(resp.data)


def test_answers_create_handler_first(client, session, fake_survey):
    resp = client.post(f"/surveys/{fake_survey.id}/answers", data={"option": " chocolate\n"})
    # Find the created answer in the database
    answer = session.scalars(select(models.Answer).filter_by(survey=fake_survey.id).limit(1)).first()
    # Make sure it stripped the whitespace
    assert answer.selected_option == "chocolate"
    # Make sure it redirected to the associated survey
    assert resp.status_code == 302
    assert resp.location == f"/surveys/{fake_survey.id}"
    # Make sure it set a cookie
    assert models.Survey.cookie_for_id(fake_survey.id) in resp.headers["Set-Cookie"]


def test_answers_create_handler_second(client, session, fake_survey):
    # Post the form data along with survey_id cookie
    client.set_cookie(models.Survey.cookie_for_id(fake_survey.id), "answered")
    resp = client.post(f"/surveys/{fake_survey.id}/answers", data={"option": "strawberry"})
    # Count matching answers in the database
    answer_count = session.scalar(
        select(func.count()).select_from(select(models.Answer).filter_by(selected_option="strawberry"))
    )
    # Make sure that no answer was made
    assert answer_count == 0
    # Make sure it redirects to the associated survey
    assert resp.status_code == 302
    assert resp.location == f"/surveys/{fake_survey.id}"


def test_surveys_multiple_allowed(client, session):
    resp = client.post(
        "/surveys",
        data={
            "survey_question": "What pets do you have?",
            "survey_topic": "pets",
            "survey_options": "zebra\horse\dog",
            "survey_multiple_allowed": "on",
        },
    )
    # Find the created survey in the database
    survey = session.scalars(select(models.Survey).filter_by(topic="pets").limit(1)).first()
    # Make sure it redirected to that survey
    assert resp.status_code == 302
    assert resp.location == f"/surveys/{survey.id}"
    assert survey.multiple_allowed is True
    # Now answer the survey
    resp = client.post(
        f"/surveys/{survey.id}/answers", data=ImmutableMultiDict([("option", "zebra"), ("option", "horse")])
    )
    # Count matching answers in the database
    answer_count = session.scalar(select(func.count()).select_from(select(models.Answer).filter_by(survey=survey.id)))
    assert answer_count == 2
