import identity
from flask import current_app, redirect, render_template, request, session, url_for

from backend.auth import bp


@bp.route("/login")
def login():
    auth = current_app.config["AUTH"]
    session["next_url"] = request.args.get("next_url", url_for("index"))
    return render_template(
        "auth/login.html",
        version=identity.__version__,
        **auth.log_in(scopes=current_app.config["SCOPE"], redirect_uri=url_for(".auth_response", _external=True)),
    )


@bp.route("/getAToken")
def auth_response():
    auth = current_app.config["AUTH"]
    result = auth.complete_log_in(request.args)
    if "error" in result:
        return render_template("auth/auth_error.html", result=result)
    next_url = session.pop("next_url", url_for("index"))
    return redirect(next_url)


@bp.route("/logout")
def logout():
    auth = current_app.config["AUTH"]
    return redirect(auth.log_out(url_for("index", _external=True)))
