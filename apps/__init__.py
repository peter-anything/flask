from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    flask_app = Flask(__name__)
    flask_app.config.from_object('config')
    db.init_app(flask_app)

    return flask_app


app = create_app()
