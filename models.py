from datetime import datetime
from flask_login import UserMixin
from __init__ import db


class User(db.Model, UserMixin):
    __tablename__ = "User"

    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(50), nullable=True)
    last_name = db.Column(db.String(50), nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def get_id(self):
        return str(self.user_id)

    @classmethod
    def from_record(cls, record):
        mapping = record._mapping if hasattr(record, "_mapping") else record
        data = dict(mapping)
        user = cls()
        user.user_id = data.get("user_id")
        user.email = data.get("email")
        user.password_hash = data.get("password_hash")
        user.first_name = data.get("first_name")
        user.last_name = data.get("last_name")
        user.phone = data.get("phone")
        return user
