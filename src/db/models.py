from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Program(db.Model):
    __tablename__ = "programs"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)

    lessons = db.relationship("Lesson", backref="program", lazy=True)


class Lesson(db.Model):
    __tablename__ = "lessons"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)

    words = db.Column(db.Text)
    sentences = db.Column(db.Text)
    notes = db.Column(db.Text)

    date = db.Column(db.DateTime, default=datetime.utcnow)

    program_id = db.Column(
        db.Integer,
        db.ForeignKey("programs.id"),
        nullable=False
    )


class Topic(db.Model):
    __tablename__ = "topics"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False, unique=True)

    words = db.Column(db.Text)
    sentences = db.Column(db.Text)

def create_general_topic():
    general = Topic.query.filter_by(title="General").first()
    if not general:
        general = Topic(
            title="General",
            words="",
            sentences=""
        )
        db.session.add(general)
        db.session.commit()
