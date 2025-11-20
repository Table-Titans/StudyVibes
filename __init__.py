from flask import Flask
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from config import Config

# Flask extensions (shared across modules)
db = SQLAlchemy()
# login_manager = LoginManager()


def register_extensions(app: Flask) -> None:
    """Attach shared extensions to the Flask app."""
    db.init_app(app)
    # login_manager.init_app(app)


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    register_extensions(app)

    Bootstrap5(app)

    import models

    from routes import register_routes

    register_routes(app, db)

    return app
