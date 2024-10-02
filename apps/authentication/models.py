# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask_login import UserMixin
from sqlalchemy.orm import relationship
from flask_dance.consumer.storage.sqla import OAuthConsumerMixin
from datetime import datetime
from apps import db, login_manager
from apps.authentication.util import hash_pass


class Users(db.Model, UserMixin):
    """
        This class represents a user entity in the database, extending from both db.Model and UserMixin.

        Attributes:
            id (int): Primary key for the user.
            username (str): A unique identifier for the user.
            email (str): The email associated with the user, must be unique.
            password (bytes): The hashed password for the user.
            oauth_github (str): GitHub OAuth identifier, optional.
            api_token (str): API token associated with the user, can be null.
            api_token_ts (int): Timestamp of the API token creation, can be null.
            created_at (datetime): Timestamp indicating when the user was created.
            updated_at (datetime): Timestamp indicating the last update to the user.
            api_keys (list): Relationship to APIKey objects associated with this user.

        Methods:
            __init__(self, **kwargs):
                Initializes an instance of a class with arbitrary key-value pairs provided as keyword arguments.

            __repr__(self):
                Returns a string representation of the user.

            is_token_expired(self):
                Check if the API token has expired (assuming token lifespan).
    """
    __tablename__ = 'Users'  # Ensure this is lowercase

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.LargeBinary, nullable=False)


    oauth_github = db.Column(db.String(100), nullable=True)  # For GitHub OAuth
    # Optional: Add columns for other providers if needed

    api_token = db.Column(db.String(100), nullable=True)  # Consider storing as hash
    api_token_ts = db.Column(db.Integer, nullable=True)  # Timestamp for token creation

    #created_at = db.Column(db.DateTime, default=datetime.utcnow)
    #updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship with API keys
    api_keys = db.relationship('APIKey', backref='owner', lazy=True)

    def __init__(self, **kwargs):
        """

        Initializes an instance of a class with arbitrary key-value pairs provided as keyword arguments.

        Args:
            kwargs: Arbitrary keyword arguments representing properties and their values.

        Behavior:
            - Iterables (except strings) will have only their first element retained.
            - If a 'password' key is provided, the value will be hashed before being set as an attribute.
            - All provided key-value pairs will set corresponding attributes in the instance.

        """
        for property, value in kwargs.items():
            if hasattr(value, '__iter__') and not isinstance(value, str):
                value = value[0]

            if property == 'password':
                value = hash_pass(value)  # Hash the password before storing

            setattr(self, property, value)

    def __repr__(self):
        return str(self.username)

    def is_token_expired(self):
        """Check if the API token has expired (assuming token lifespan)."""
        expiration_time = 3600  # Token lifespan in seconds (e.g., 1 hour)
        if self.api_token_ts:
            return (datetime.utcnow() - datetime.utcfromtimestamp(self.api_token_ts)).total_seconds() > expiration_time
        return True


@login_manager.user_loader
def user_loader(id):
    return Users.query.filter_by(id=id).first()


@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    user = Users.query.filter_by(username=username).first()
    return user if user else None


class OAuth(OAuthConsumerMixin, db.Model):
    __tablename__ = 'OAuth'

    user_id = db.Column(db.Integer, db.ForeignKey("Users.id", ondelete="cascade"), nullable=False)
    user = db.relationship(Users)


# Event listener to update the 'updated_at' field automatically
@db.event.listens_for(Users, 'before_update')
def receive_before_update(mapper, connection, target):
    target.updated_at = datetime.utcnow()
