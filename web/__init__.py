from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


import os

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)
    
    app.config.from_mapping(SECRET_KEY="dev")

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite3'

    db.init_app(app)

    migrate.init_app(app, db)

    from web import models


    @app.route("/test")
    def test():
        return render_template("alter/login.html")

    # apply the blueprints to the app
    from web.apps import main, auth, yank
    app.register_blueprint(main.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(yank.bp)

    return app
