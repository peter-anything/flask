from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config
db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    db.init_app(app)

    from app.account.views.account import account_bp
    app.register_blueprint(account_bp, url_prefix='/account')
    print(app.url_map)

    return app
