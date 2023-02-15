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

bp = Blueprint("main", __name__)

@bp.route("/")
@login_required
def root():
	todo_list = Todo.query.all()[::-1]
	results = session.pop('results', [])
	return render_template("main.html", todo_list=todo_list, results=results)


@bp.route("/create_todo", methods=("POST",))
def create_todo():
	message = request.form['message']
	todo = Todo(message = message)
	db.session.add(todo)
	db.session.commit()

	return redirect(url_for("main.root"))


@bp.route("/delete_todo/<id>", methods=("POST",))
def delete_todo(id):
	todo = Todo.query.filter_by(id=id).first()
	db.session.delete(todo)
	db.session.commit()
	return redirect(url_for("main.root"))


@bp.route("/search", methods=("POST",))
def search():
	query = request.form['query']
	similar_series = Series.query.filter(Series.title.like(f"%{query}%")).all()
	results = [{"id": s.id, "title": s.title, "image": s.image} for s in similar_series]
	session['results'] = results
	return redirect(url_for("main.root"))


@bp.route("/show/<id>")
def show(id):
	series = Series.query.filter_by(imdb_id=id).first()

	if series == None: return "not found"
	
	seasons = series.seasons

	message = ""

	for season in seasons:
		episodes = season.episodes
		for episode in episodes:
			message += f"{episode.no} - {episode.title}</br>"

	return message

















def insert_tv_series(data):
	try:
		seasons = []
		episodes = []

		series = Series(
			imdb_id = data['id'],
			title = data['title'],
			image = data['image'],
			plot = data['plot'],
			rating_count = int(data['rating']['count']),
			rating_star = float(data['rating']['star']),
			genres = ",".join(data['genre'])
		)

		for i in data['seasons']:
			season = Season(name = i['name'], series=series)
			for j in i['episodes']:
				episodes.append(Episode(
					no = j['no'],
					title = j['title'],
					image = j['image'],
					image_large = j['image_large'],
					plot = j['plot'],
					published_date = j['publishedDate'],
					rating_count = int(j['rating']['count']),
					rating_star = float(j['rating']['star']),
					season = season
				))
			seasons.append(season)

		db.session.add(series)
		db.session.add_all(seasons)
		db.session.add_all(episodes)

		db.session.commit()
		
		return True
	except Exception as e:
		print(e)
		flash(e)
		return False

	





@bp.route("/create_yank", methods=("POST",))
def create_yank():
	imdb_id = request.form['imdb_id']
	url = f"https://imdb-api.tprojects.workers.dev/title/{imdb_id}"
	data = requests.get(url)

	if data.status_code != 200:
		flash("IMDB_ID is wrong!")
		return redirect(url_for("main.root"))

	yank =  Series.query.filter_by(imdb_id=imdb_id).first()
	if yank != None:
		flash("IMDB_ID is exists!")
		return redirect(url_for("main.root"))

	
	data = data.json()
	if data['contentType'] == "TVSeries":
		if insert_tv_series(data):
			flash("tv-series inserted!")
			# print("here")
			# return redirect(url_for("main.root"))
		else:
			flash(f"error: bad json!")
	elif data['contentType'] == "Movie":
		pass
	else:
		flash("This is not movie or tv-series!")

	return redirect(url_for("main.root"))

# @bp.route("/create_yank", methods=("POST",))
# def create_yank():
#     imdb_id = request.form['imdb_id']

#     yank = Yank.query.filter_by(imdb_id=imdb_id).first()

#     if yank != None:
#         flash("IMDB_ID is exists!")
#         return redirect(url_for("main.root"))

#     url = f"https://https://imdb-api.tprojects.workers.dev/title/{imdb_id}" 
#     data = requests.get(url).json()

#     if data['contentType'] not in ['Movie', 'TVSeries']:
#         flash("This reference is not movie or TVseries!")
#         return redirect(url_for("main.root"))

#     yank = Yank(imdb_id=imdb_id, title=data['title'], cover=data['full-size cover url'])
#     db.session.add(yank)
#     db.session.commit()

#     flash("Yank inserted")
#     return redirect(url_for("main.root"))