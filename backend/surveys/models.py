import logging

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String

from backend import db


class Survey(db.Model):
    __tablename__ = "survey"
    id = Column(Integer, primary_key=True)
    topic = Column(String(50))
    question = Column(String(150))
    options = Column(String(500))  # New-line separated options
    multiple_allowed = Column(Boolean, default=False)

    @property
    def options_list(self):
        return [option.strip() for option in self.options.strip().split("\n")]

    @property
    def answer_count(self):
        return Answer.query.filter_by(survey=self.id).count()

    @property
    def input_type(self):
        return "checkbox" if self.multiple_allowed else "radio"

    @property
    def option_stats(self):
        """Returns a dictionary of option counts"""
        answer_count = self.answer_count
        option_count = {option: {"count": 0, "percent": 0} for option in self.options_list}
        for answer in Answer.query.filter_by(survey=self.id):
            if answer.selected_option in option_count:
                option_count[answer.selected_option]["count"] += 1
                option_count[answer.selected_option]["percent"] = round(
                    option_count[answer.selected_option]["count"] / answer_count * 100,
                    2,
                )
            else:
                logging.warning("No matching option found for [%s]", answer.selected_option)
        return option_count

    @staticmethod
    def cookie_for_id(survey_id):
        return f"survey_id:{survey_id}"


class Answer(db.Model):
    __tablename__ = "answer"
    id = Column(Integer, primary_key=True)
    survey = Column(Integer, ForeignKey("survey.id", ondelete="CASCADE"))
    selected_option = Column(String(500))
