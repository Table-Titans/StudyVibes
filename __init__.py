from flask import Flask
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = "login"


def register_extensions(app: Flask) -> None:
    db.init_app(app)
    login_manager.init_app(app)


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    register_extensions(app)
    Bootstrap5(app)
    from routes import register_routes
    register_routes(app, db)
    return app


@login_manager.user_loader
def load_user(user_id: str):
    if not user_id:
        return None
    from sqlalchemy import text
    from models import User
    query = text("""
        SELECT user_id, email, password_hash, first_name, last_name, phone
        FROM User
        WHERE user_id = :id
    """)
    result = db.session.execute(query, {"id": user_id}).first()
    if not result:
        return None
    return User.from_record(result)
