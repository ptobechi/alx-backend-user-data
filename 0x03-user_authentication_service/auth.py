#!/usr/bin/env python3
"""
Auth class for user authentication.
"""

from db import DB
import bcrypt
import uuid
from user import User


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def _hash_password(self, password: str) -> bytes:
        """Hash a password using bcrypt.
        """
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode(), salt)
        return hashed_password

    def register_user(self, email: str, password: str):
        """Register a new user or raise an error if the user already exists.
        """
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except Exception:
            hashed_password = self._hash_password(password)
            self._db.add_user(email, hashed_password)
            return User(email, hashed_password)

    def valid_login(self, email: str, password: str) -> bool:
        """Check if the provided email and password match an existing user.
        """
        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(password.encode(), user.hashed_password)
        except Exception:
            return False

    def _generate_uuid(self) -> str:
        """Generate a new UUID and return it as a string.
        """
        return str(uuid.uuid4())

    def create_session(self, email: str) -> str:
        """Create a new session for the user with the
        given email and return the session ID.
        """
        try:
            # Find the user
            user = self._db.find_user_by(email=email)
            # Generate a new session ID
            session_id = self._generate_uuid()
            # Update the user's session ID in the database
            self._db.update_user(email=email, session_id=session_id)
            return session_id
        except Exception:
            return None

    def get_user_from_session_id(self, session_id: str):
        """Retrieve a user by their session ID.
        """
        if session_id is None:
            return None
        try:
            # Find user by session_id
            user = self._db.find_user_by(session_id=session_id)
            return user
        except Exception:
            return None

    def destroy_session(self, user_id: int):
        """
        Destroy the user's session by setting their session ID to None.
        """
        try:
            # Update the user's session ID to None
            self._db.update_user(user_id=user_id, session_id=None)
        except Exception:
            pass
