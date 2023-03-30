import identity
from flask import current_app, redirect, render_template, request, url_for

from backend.login import bp


@bp.route("/login")
def login():
    auth = current_app.config["AUTH"]
    return render_template(
        "auth/login.html",
        version=identity.__version__,
        **auth.log_in(
            scopes=current_app.config["SCOPE"],  # Have user consent to scopes during log-in
            redirect_uri=url_for(".auth_response", _external=True),
        ),
    )


@bp.route(current_app.config["REDIRECT_PATH"])
def auth_response():
    auth = current_app.config["AUTH"]
    result = auth.complete_log_in(request.args)
    if "error" in result:
        return render_template("auth/auth_error.html", result=result)
    return redirect(url_for(".index"))


@bp.route("/logout")
def logout():
    auth = current_app.config["AUTH"]
    return redirect(auth.log_out(url_for(".index", _external=True)))


@bp.route("/")
def index():
    auth = current_app.config["AUTH"]
    if not auth.get_user():
        return redirect(url_for(".login"))
    return render_template("auth/index.html", user=auth.get_user(), version=identity.__version__)
