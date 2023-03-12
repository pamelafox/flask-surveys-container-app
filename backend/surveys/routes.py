from flask import redirect, render_template, request, url_for

from backend import db
from backend.surveys import bp
from backend.surveys.models import Answer, Survey


@bp.route("/", methods=["GET"])
def index():
    return redirect(url_for("surveys.surveys_list_page"))


@bp.route("/surveys", methods=["GET"])
def surveys_list_page():
    surveys = Survey.query.all()
    return render_template("surveys_list.html", surveys=surveys)


@bp.route("/surveys/new", methods=["GET"])
def surveys_create_page():
    return render_template("surveys_create.html")


@bp.route("/surveys", methods=["POST"])
def surveys_create_handler():
    question = request.values.get("survey_question")
    topic = request.values.get("survey_topic")
    options = request.values.get("survey_options")
    multiple_allowed = request.values.get("survey_multiple_allowed")
    survey = Survey()
    survey.topic = topic
    survey.question = question
    survey.options = options
    survey.multiple_allowed = multiple_allowed == "on"
    db.session.add(survey)
    db.session.commit()
    return redirect(url_for("surveys.survey_page", survey_id=survey.id))


@bp.route("/surveys/<int:survey_id>", methods=["GET"])
def survey_page(survey_id):
    survey = Survey.query.where(Survey.id == survey_id).first()
    answers = Survey.query.where(Answer.survey == survey_id)
    return render_template(
        "survey_details.html",
        survey=survey,
        answers=answers,
        already_voted=Survey.cookie_for_id(survey_id) in request.cookies,
    )


@bp.route("/surveys/<int:survey_id>/answers", methods=["POST"])
def answers_create_handler(survey_id):
    # Check cookie to prevent multiple votes
    if Survey.cookie_for_id(survey_id) in request.cookies:
        return redirect(url_for("surveys.survey_page", survey_id=survey_id))
    # Store their answer in database
    options = request.values.getlist("option")
    for option in options:
        answer = Answer()
        answer.survey = survey_id
        answer.selected_option = option.strip()
        db.session.add(answer)
        db.session.commit()
    resp = redirect(url_for("surveys.survey_page", survey_id=survey_id))
    # Set cookie on the response
    resp.set_cookie(Survey.cookie_for_id(survey_id), "answered")
    return resp
