from flask import Blueprint, flash, g
from flask import redirect, render_template
from flask import request, url_for, session

from web.models import User

from werkzeug.security import check_password_hash

import functools

bp = Blueprint("auth", __name__)

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))
        return view(**kwargs)
    return wrapped_view


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get("user_id")
    if user_id is None:
        g.user = None
    else:
        g.user = (User.query.filter_by(id=user_id).first())


@bp.route("/login", methods=("GET", "POST"))
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        error = None
        user = User.query.filter_by(username=username).first()
        
        if user is None:
            error = "Incorrect username."
        elif not check_password_hash(user.password, password):
            error = "Incorrect password."
        
        if error is None:
            session.clear()
            session["user_id"] = user.id
            return redirect(url_for("main.root"))

        flash(error)

    return render_template("login.html")


@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("main.root"))