# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from apps import db
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import secrets  # For cryptographically secure key generation
import hashlib
import os

'''
Add your models below
'''


def generate_default_key_hash():
    """
    Generates a cryptographically secure hash to be used as the default API key hash.
    """
    # Generate a random 32-byte string
    random_bytes = os.urandom(32)

    # Create a SHA-256 hash of the random bytes
    hash_object = hashlib.sha256(random_bytes)

    # Return the hexadecimal digest of the hash
    return hash_object.hexdigest()
# Book Sample
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64))

# APIKey Model
class APIKey(db.Model):
    __tablename__ = 'api_key'  # Use a lowercase table name for consistency

    id = db.Column(db.Integer, primary_key=True)
   # key_hash = db.Column(db.String(128), unique=True, nullable=False, index=True)  # Hashed key, indexed for performance
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'), nullable=False)
    #created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Track key creation timestamp
    key_hash = db.Column(db.String(128), nullable=False, default=generate_default_key_hash)



    # Specify the primary condition explicitly
    user = db.relationship('Users', backref='api_key_relationship', primaryjoin='Users.id == APIKey.user_id')

    def __init__(self, key, user_id):
        # Store the key as a hash for security
        self.key_hash = generate_password_hash(key)
        self.user_id = user_id


    @staticmethod
    def generate_key():
        """Generates a cryptographically secure API key using secrets."""
        return secrets.token_urlsafe(32)  # Cryptographically secure key generation

    @classmethod
    def create_api_key(cls, user_id):
        """Create and return a new API key for a user."""
        raw_key = cls.generate_key()  # Generate a secure key
        new_key = cls(key=raw_key, user_id=user_id)
        db.session.add(new_key)
        db.session.commit()
        return raw_key  # Return the raw key, not the hash, to the user

    def check_key(self, raw_key):
        """Validates a provided key by comparing it with the stored hash."""
        return check_password_hash(self.key_hash, raw_key)

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            #"created_at": self.created_at.isoformat(),  # Include creation timestamp
            # Do not return the key_hash for security reasons
        }
