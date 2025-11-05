"""Application data models."""

from __init__ import db


class Example(db.Model):
    """Illustrative model showing how to import the shared db instance."""

    __tablename__ = "example"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)

    def __repr__(self) -> str:
        return f"<Example id={self.id!r} name={self.name!r}>"
