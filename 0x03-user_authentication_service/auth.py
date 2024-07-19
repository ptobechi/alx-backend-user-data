#!/usr/bin/env python3
"""Auth module to handle user authentication"""

import uuid
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


class Auth:
    """Auth class to interact with the authentication database."""

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Register a new user and return the User object"""
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hashed_password = self._hash_password(password)
            return self._db.add_user(email, hashed_password)

    def _hash_password(self, password):
        # Generate salt and hash the password
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed_password

    def valid_login(self, email: str, password: str) -> bool:
        """Check if the provided login credentials are valid"""
        try:
            user = self._db.find_user_by(email=email)
            if bcrypt.checkpw(password.encode('utf-8'), user.hashed_password):
                return True
            return False
        except NoResultFound:
            return False

    def _generate_uuid(self) -> str:
        """Generate a new UUID and return its string representation"""
        return str(uuid.uuid4())

    def create_session(self, email: str) -> str:
        """Create a session for the user identified by email"""
        try:
            user = self._db.find_user_by(email=email)
            session_id = self._generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return None
        
    def get_reset_password_token(self, email):
        """Reset Password token"""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError(f"User {email} does not exist")

        reset_token = str(uuid.uuid4())
        user.reset_token = reset_token
        self._db.commit()

        return reset_token
    
    def update_password(self, reset_token, new_password):
        # Find user by reset_token
        user = self._db.find_user_by(reset_token=reset_token)
        if not user:
            raise ValueError("Invalid reset token")

        # Hash the new password
        hashed_password = self._hash_password(new_password)

        # Update user's hashed_password and reset_token fields
        user.hashed_password = hashed_password
        user.reset_token = None

        # Commit changes to the database
        self._db.commit()
