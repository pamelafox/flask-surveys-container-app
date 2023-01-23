from datetime import datetime
import os

from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from requests import RequestException

app = Flask(__name__, static_folder='static')
csrf = CSRFProtect(app)

# If RUNNING_IN_PRODUCTION is defined as an environment variable, then we're running on Azure
if not 'RUNNING_IN_PRODUCTION' in os.environ:
    # Local development, where we'll use environment variables.
    print("Loading config.development and environment variables from .env file.")
    app.config.from_object('settings.development')
else:
    # Production, we don't load environment variables from .env file but add them as environment variables in Azure.
    print("Loading config.production.")
    app.config.from_object('settings.production')

with app.app_context():
    app.config.update(
        SQLALCHEMY_DATABASE_URI=app.config.get('DATABASE_URI'),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

# Initialize the database connection
db = SQLAlchemy(app)

# Enable Flask-Migrate commands "flask db init/migrate/upgrade" to work
migrate = Migrate(app, db)

# The import must be done after db initialization due to circular import issue
from models import Survey, Answer


@app.route('/', methods=['GET'])
def index():
    return redirect(url_for('surveys_list_page'))

@app.route('/surveys', methods=['GET'])
def surveys_list_page():
    surveys = Survey.query.all()    
    return render_template('surveys_list.html', surveys=surveys)

@app.route('/surveys/new', methods=['GET'])
def surveys_create_page():
    return render_template('surveys_create.html')

@app.route('/surveys', methods=['POST'])
@csrf.exempt
def surveys_create_handler():
    question = request.values.get('survey_question')
    topic = request.values.get('survey_topic')
    options = request.values.get('survey_options')
    survey = Survey()
    survey.topic = topic
    survey.question = question
    survey.options = options
    db.session.add(survey)
    db.session.commit()
    return redirect(url_for('survey_page', survey_id=survey.id))

@app.route('/surveys/<int:survey_id>', methods=['GET'])
def survey_page(survey_id):
    survey = Survey.query.where(Survey.id == survey_id).first()
    answers = Survey.query.where(Answer.survey==survey_id)
    return render_template('survey_details.html', survey=survey, answers=answers, already_voted='survey_id' in request.cookies)

@app.route('/surveys/<int:survey_id>/answers', methods=['POST'])
@csrf.exempt
def answers_create_handler(survey_id):
    # Check cookie to prevent multiple votes
    if 'survey_id' in request.cookies:
        return redirect(url_for('survey_page', survey_id=survey_id))
    # Store their answer in database
    option = request.values.get('option')
    answer = Answer()
    answer.survey = survey_id
    answer.selected_option = option.strip()
    db.session.add(answer)
    db.session.commit()
    resp = redirect(url_for('survey_page', survey_id=survey_id))   
    # Set cookie on the response
    resp.set_cookie('survey_id', str(survey_id))
    return resp

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

if __name__ == '__main__':
   app.run()
