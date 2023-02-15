from flask import (
	Blueprint,
	render_template,
	redirect,
	url_for,
	request,
	flash,
	session
)

import json
import requests

from web.apps.auth import login_required

from web.models import (
	Todo,
	Series,
	Season,
	Episode
)
from web import db

bp = Blueprint("yank", __name__)


@bp.route("/yank/<id>")
def yank(id):
    result = db.get_or_404(Series, id)
    return  render_template("yank.html", result=result)