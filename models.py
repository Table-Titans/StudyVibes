"""Application data models."""

from datetime import datetime
from flask_login import UserMixin
from __init__ import db


class Session(db.Model):
    __tablename__ = "StudySession"

    session_id = db.Column(db.Integer, primary_key=True)
    course_offering_id = db.Column(db.Integer, nullable=True)
    location_id = db.Column(db.Integer, nullable=True)
    organizer_id = db.Column(db.Integer, nullable=True)
    max_attendees = db.Column(db.Integer, nullable=True)
    description = db.Column(db.String(200), nullable=True)
    start_time = db.Column(db.TIMESTAMP, nullable=True)
    end_time = db.Column(db.TIMESTAMP, nullable=True)
    chill_level = db.Column(db.Integer, nullable=True)
    room_type_id = db.Column(db.Integer, nullable=True)
    
    def to_dict(self):
        """Convert session to dictionary for template rendering"""
        return {
            'id': self.session_id,
            'session_id': self.session_id,
            'course_id': self.course_offering_id,
            'location_id': self.location_id,
            'organizer_id': self.organizer_id,
            'max_attendees': self.max_attendees,
            'description': self.description,
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'chill_level': self.chill_level,
            'room_type_id': self.room_type_id
        }

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

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'phone': self.phone,
        }

    @classmethod
    def from_record(cls, record):
        """Create a detached User instance from a SQLAlchemy Row object."""
        mapping = record._mapping if hasattr(record, "_mapping") else record
        data = dict(mapping)
        user = cls()
        user.user_id = data["user_id"]
        user.email = data["email"]
        user.password_hash = data.get("password_hash")
        user.first_name = data.get("first_name")
        user.last_name = data.get("last_name")
        user.phone = data.get("phone")
        return user

class CourseOffering(db.Model):
    __tablename__ = "CourseOffering"
    
    course_offering_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    section = db.Column(db.String(20), nullable=True)
    year = db.Column(db.Integer, nullable=True)
    term = db.Column(db.Integer, nullable=True)
    
    def to_dict(self):
        return {
            'id': self.course_offering_id,
            'title': self.title,
            'section': self.section,
            'year': self.year,
            'term': self.term,
        }

class Location(db.Model):
    __tablename__ = "Location"
    
    location_id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(100), nullable=False)
    room_number = db.Column(db.String(20), nullable=False)
    
    def to_dict(self):
        return {
            'id': self.location_id,
            'address': self.address,
            'room_number': self.room_number
        }

class Example(db.Model):
    """Illustrative model showing how to import the shared db instance."""

    __tablename__ = "example"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)

    def __repr__(self) -> str:
        return f"<Example id={self.id!r} name={self.name!r}>"
