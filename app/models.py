from datetime import datetime
from app import db


class User(db.Model):
    """Data model for user accounts"""

    __tablename__ = 'users'
    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False
    )
    gender_id = db.Column(
        db.Integer,
        db.ForeignKey('genders.id'),
        nullable=False
    )
    birthday = db.Column(
        db.Date,
        nullable=False
    )
    measurements = db.relationship('Measurement', back_populates='user')
    gender = db.relationship('Gender', back_populates='users')


class Gender(db.Model):
    """Data model for user gender"""

    __tablename__ = 'genders'
    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False
    )
    biology = db.Column(
        db.String(6),
        nullable=False
    )
    users = db.relationship('User', back_populates='gender')


class Measurement(db.Model):
    """Data model for users measurements"""

    __tablename__ = 'measurements'
    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False
    )
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=False
    )
    timestamp = db.Column(
        db.DateTime,
        index=True,
        default=datetime.utcnow
    )
    bmi = db.Column(
        db.Float,
        nullable=False
    )
    user = db.relationship('User', back_populates='measurements')
