from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Rating(db.Model):
    __tablename__ = 'rating'
    id = db.Column(db.Integer, primary_key=True)
    count = db.Column(db.Integer)
    star = db.Column(db.Float)

class Episode(db.Model):
    __tablename__ = 'episode'
    id = db.Column(db.Integer, primary_key=True)
    idx = db.Column(db.Integer)
    no = db.Column(db.String)
    title = db.Column(db.String)
    image = db.Column(db.String)
    image_large = db.Column(db.String)
    plot = db.Column(db.String)
    publishedDate = db.Column(db.String)
    rating_id = db.Column(db.Integer, db.ForeignKey('rating.id'))
    rating = db.relationship('Rating', backref=db.backref('episodes', lazy=True))

class Season(db.Model):
    __tablename__ = 'season'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

class TVSeries(db.Model):
    __tablename__ = 'tv_series'
    id = db.Column(db.String, primary_key=True)
    contentType = db.Column(db.String)
    title = db.Column(db.String)
    image = db.Column(db.String)
    plot = db.Column(db.String)
    rating_id = db.Column(db.Integer, db.ForeignKey('rating.id'))
    rating = db.relationship('Rating', backref=db.backref('tv_series', lazy=True))
    genres = db.Column(db.String)
    seasons = db.relationship('Season', backref=db.backref('tv_series', lazy=True))
    episodes = db.relationship('Episode', backref=db.backref('tv_series', lazy=True))
