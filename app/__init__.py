from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import config

# Initialize extensions without binding them to an app yet
db = SQLAlchemy()
migrate = Migrate()


def create_app(config_name="local"):
    """Factory function to create and configure the Flask application."""
    # Initialize the Flask app and load the desired configuration
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Bind extensions to the application
    db.init_app(app)
    migrate.init_app(app, db)

    # Ensure routes and models are imported after app creation to avoid circular imports
    with app.app_context():
        from . import routes, models  # noqa: F401
        db.create_all()  # Create database tables if they don't exist

    return app
