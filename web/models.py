from web import db
import datetime


class User(db.Model):
    id = db.Column(db.Integer, primary_key =True)
    username = db.Column(db.String(128), nullable = False)
    password = db.Column(db.String(256), nullable = False)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key =True)
    message = db.Column(db.String(256), nullable = False)






# Series Tables
class File(db.Model):
    __tablename__ = 'file'
    id = db.Column(db.Integer, primary_key=True)
    message_id = db.Column(db.Integer, nullable=False)
    quality = db.Column(db.String, nullable=False)
    mode = db.Column(db.Integer, nullable=False, default=0)
    episode_id = db.Column(db.Integer, db.ForeignKey('episode.id'))


class Episode(db.Model):
    __tablename__ = "episode"
    id = db.Column(db.Integer, primary_key=True)
    no = db.Column(db.String, nullable=False)
    title = db.Column(db.String, nullable=False)
    image = db.Column(db.String, nullable=False)
    image_large = db.Column(db.String, nullable=False)
    plot = db.Column(db.String, nullable=False)
    published_date = db.Column(db.String, nullable=False)
    rating_count = db.Column(db.Integer, nullable=False)
    rating_star = db.Column(db.Float, nullable=False)
    files = db.relationship('File', backref='episode')
    session_id = db.Column(db.Integer, db.ForeignKey('season.id'))

class Season(db.Model):
    __tablename__ = "season"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    episodes = db.relationship('Episode', backref='season')
    series_id = db.Column(db.Integer, db.ForeignKey('series.id'))

class Series(db.Model):
    __tablename__ = "series"
    id = db.Column(db.Integer, primary_key=True)
    imdb_id = db.Column(db.String, nullable=False)
    title = db.Column(db.String, nullable=False)
    image = db.Column(db.String, nullable=False)
    plot = db.Column(db.String, nullable=False)
    rating_count = db.Column(db.Integer, nullable=False)
    rating_star = db.Column(db.Float, nullable=False)
    genres = db.Column(db.String, nullable=False)
    last_update = db.Column(db.String, default=str(datetime.datetime.now()), nullable=True)
    seasons = db.relationship('Season', backref='series')




