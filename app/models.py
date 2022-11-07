from datetime import datetime
from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    """Data model for user accounts"""

    __tablename__ = 'users'
    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True,
    )
    name = db.Column(
        db.String(100),
        nullable=False,
        unique=False
    )
    email = db.Column(
        db.String(40),
        unique=True,
        nullable=False
    )
    password = db.Column(
        db.String(200),
        primary_key=False,
        unique=False,
        nullable=False
    )
    created_on = db.Column(
        db.DateTime,
        index=False,
        unique=False,
        nullable=False,
        default=datetime.utcnow
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

    def set_password(self, password):
        """Create hashed password"""
        self.password = generate_password_hash(
            password,
            method='sha256'
        )

    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

    # TODO: Add repr for other classes
    def __repr__(self):
        return '<User {}>'.format(self.email)


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
