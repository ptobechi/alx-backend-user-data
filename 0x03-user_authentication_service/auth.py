#!/usr/bin/env python3
"""Authentication module"""

from db import DB
from user import User
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from bcrypt import hashpw, gensalt


class Auth:
    """Auth class to interact with the authentication database."""

    def __init__(self):
        self._db = DB()

    def _hash_password(self, password: str) -> bytes:
        """Hashes a password with bcrypt.

        Args:
            password (str): The password to hash.

        Returns:
            bytes: The salted hash of the password.
        """
        salt = gensalt()
        hashed = hashpw(password.encode('utf-8'), salt)
        return hashed

    def register_user(self, email: str, password: str) -> User:
        """Registers a new user if the email does not already exist.

        Args:
            email (str): The email of the user.
            password (str): The password of the user.

        Returns:
            User: The created User object.

        Raises:
            ValueError: If a user with the given email already exists.
        """
        try:
            # Check if user already exists
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            # User does not exist, proceed to create
            hashed_password = self._hash_password(password)
            user_id = self._db.add_user(email, hashed_password)
            return User(user_id, email, hashed_password, None, None)
