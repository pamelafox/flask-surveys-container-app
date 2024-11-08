# Use pytest to test the classes and methods in models.py
from backend import db
from backend.surveys import models


def test_survey_options_list():
    survey = models.Survey(
        topic="ice cream",
        question="What's your favorite flavor?",
        options=" chocolate\n  vanilla\n",
    )
    assert survey.options_list == ["chocolate", "vanilla"]


def test_survey_option_count_stats(app_ctx):
    survey = models.Survey(
        topic="ice cream",
        question="What's your favorite flavor?",
        options=" chocolate\n  vanilla\n",
    )
    db.session.add(survey)
    db.session.commit()
    assert survey.query_answer_count(db.session) == 0
    answer1 = models.Answer(survey=survey.id, selected_option="chocolate")
    answer2 = models.Answer(survey=survey.id, selected_option="vanilla")
    answer3 = models.Answer(survey=survey.id, selected_option="chocolate")
    answer4 = models.Answer(survey=survey.id, selected_option="strawberry")
    db.session.add_all([answer1, answer2, answer3, answer4])
    db.session.commit()
    assert survey.query_answer_count(db.session) == 4
    assert survey.query_option_stats(db.session) == {
        "chocolate": {"count": 2, "percent": 50.0},
        "vanilla": {"count": 1, "percent": 25.0},
    }
    # Now delete all the created rows
    db.session.delete(answer1)
    db.session.delete(answer2)
    db.session.delete(answer3)
    db.session.delete(answer4)
    db.session.delete(survey)
    db.session.commit()
