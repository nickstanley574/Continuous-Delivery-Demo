from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import config
from os import getenv

db = SQLAlchemy()
migrate = Migrate(db=db)

def create_app(config_name='local'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        from . import routes, models
        db.create_all()

    return app
