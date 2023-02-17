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
import datetime

from web.apps.auth import login_required

from web.models import (
	Todo,
	Series,
	Season,
	Episode,
	File
)
from web import db

bp = Blueprint("yank", __name__)


@bp.route("/yank/<id>")
def yank(id):
	result = db.get_or_404(Series, id)
	return  render_template("yank.html", result=result)


@bp.route("/yank/insert_file", methods=("POST",))
def insert_file():
	try:
		episode_id = int(request.form['episode_id'])
	except:
		episode_id = -1

	episode = db.get_or_404(Episode, int(episode_id))
	try:
		quality = int(request.form['quality'])
		mid = int(request.form['mid'])
		mode = request.form['mode']
		if not mode:
			mode = 0
		else:
			mode = int(mode)
	except:
		flash("Wrong inputs!")
		return redirect(url_for("yank.yank", id=episode.season.series.id))

	file = File.query.filter_by(message_id=mid, episode=episode).first()
	if file != None:
		flash("MID is exists!")
		return redirect(url_for("yank.yank", id=episode.season.series.id))



	file = File(
		message_id=mid,
		quality=quality,
		mode=mode,
		episode=episode
	)

	db.session.add(file)
	db.session.commit()

	flash(f"file ({mid}) inserted")
	return redirect("/yank/" + str(episode.season.series.id) + "#" + str(episode.id))




def update_series(data, series):
	
	series.rating_count = int(data["rating"]["count"])
	series.rating_star = float(data["rating"]["star"])

	for season_data in data['seasons']:
		season = Season.query.filter_by(name=season_data['name'], series=series).first()
		if season is None:
			season = Season(name=season_data['name'], series_id=series.id)
			db.session.add(season)

		for episode_data in season_data['episodes']:
			episode = Episode.query.filter_by(no=episode_data["no"], season=season).first()
			if episode is None:
				episode = Episode(
					no = episode_data['no'],
					title = episode_data['title'],
					image = episode_data['image'],
					image_large = episode_data['image_large'],
					plot = episode_data['plot'],
					published_date = episode_data['publishedDate'],
					rating_count = int(episode_data['rating']['count']),
					rating_star = float(episode_data['rating']['star']),
					season = season
				)
				db.session.add(episode)
			else:
				episode.rating_count = int(episode_data['rating']['count'])
				episode.rating_star = float(episode_data['rating']['star'])

	series.last_update = str(datetime.datetime.now())

	db.session.commit()



@bp.route("/yank/update/<id>", methods=("POST",))
def yank_update(id):
	
	series = db.get_or_404(Series, id)
	url = f"https://imdb-api.tprojects.workers.dev/title/{series.imdb_id}"
	data = requests.get(url)
	
	if data.status_code != 200:
		flash("IMDB_ID is wrong!")
		return redirect(url_for("yank.yank", id=id))

	data = data.json()
	if data['contentType'] == "TVSeries":
		try:
			update_series(data, series)
			flash("Series updated!")
		except:
			flash("Update failed!")
	elif data['contentType'] == "Movie":
		pass
	else:
		flash("This is not movie or tv-series!")

	return redirect(url_for("yank.yank", id=id))