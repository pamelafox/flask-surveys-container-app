# Use pytest to test the classes and methods in models.py
from backend.surveys import models


def test_survey_options_list():
    survey = models.Survey(
        topic="ice cream",
        question="What's your favorite flavor?",
        options=" chocolate\n  vanilla\n",
    )
    assert survey.options_list == ["chocolate", "vanilla"]


def test_survey_option_count_stats(session):
    survey = models.Survey(
        topic="ice cream",
        question="What's your favorite flavor?",
        options=" chocolate\n  vanilla\n",
    )
    session.add(survey)
    session.commit()
    assert survey.answer_count == 0
    answer1 = models.Answer(survey=survey.id, selected_option="chocolate")
    answer2 = models.Answer(survey=survey.id, selected_option="vanilla")
    answer3 = models.Answer(survey=survey.id, selected_option="chocolate")
    answer4 = models.Answer(survey=survey.id, selected_option="strawberry")
    session.add_all([answer1, answer2, answer3, answer4])
    session.commit()
    assert survey.answer_count == 4
    assert survey.option_stats == {"chocolate": {"count": 2, "percent": 50.0}, "vanilla": {"count": 1, "percent": 25.0}}
