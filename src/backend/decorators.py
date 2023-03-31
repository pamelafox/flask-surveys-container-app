from functools import wraps

from flask import current_app, redirect, request, url_for


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth = current_app.config["AUTH"]
        if not auth.get_user():
            login_url = url_for("auth.login", next_url=request.url)
            return redirect(login_url)
        return f(*args, **kwargs)

    return decorated_function
