import logging

from sqlalchemy import ForeignKey, String, func, select
from sqlalchemy.orm import Mapped, mapped_column

from backend import db


class Survey(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    topic: Mapped[str] = mapped_column(String(50))
    question: Mapped[str] = mapped_column(String(150))
    options: Mapped[str] = mapped_column(String(500))  # New-line separated options
    multiple_allowed: Mapped[bool] = mapped_column(default=False)

    @property
    def options_list(self):
        return [option.strip() for option in self.options.strip().split("\n")]

    @property
    def answer_count(self):
        return db.session.scalar(select(func.count(Answer.id)))

    @property
    def input_type(self):
        return "checkbox" if self.multiple_allowed else "radio"

    @property
    def option_stats(self):
        """Returns a dictionary of option counts"""
        answer_count = self.answer_count
        option_count = {option: {"count": 0, "percent": 0} for option in self.options_list}
        answers = db.session.execute(select(Answer.selected_option).filter_by(survey=self.id))
        for answer in answers:
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
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    survey: Mapped[int] = mapped_column(ForeignKey("survey.id", ondelete="CASCADE"))
    selected_option: Mapped[str] = mapped_column(String(500))
