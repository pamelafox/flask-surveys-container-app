import identity
from flask import current_app, redirect, render_template, request, url_for

from backend.auth import bp


@bp.route("/login")
def login():
    auth = current_app.config["AUTH"]
    return render_template(
        "auth/login.html",
        version=identity.__version__,
        **auth.log_in(
            scopes=current_app.config["SCOPE"],  # Have user consent to scopes during log-in
            redirect_uri=url_for(".auth_response", _external=True),
            state=request.args.get("next_url", url_for("index")),
        ),
    )


@bp.route("/getAToken")
def auth_response():
    auth = current_app.config["AUTH"]
    result = auth.complete_log_in(request.args)
    if "error" in result:
        return render_template("auth/auth_error.html", result=result)
    return redirect(request.args.get("state", url_for("index")))


@bp.route("/logout")
def logout():
    auth = current_app.config["AUTH"]
    return redirect(auth.log_out(url_for("index", _external=True)))
