#!/usr/bin/env python3
"""
Session Authentication module for the API.

This module defines the SessionAuth class for handling
session-based authentication.
"""
from api.v1.auth.auth import Auth
import os
import uuid
from models.user import User


class SessionAuth(Auth):
    """
    SessionAuth class for session-based auth handling.
    Currently empty, to be expanded for session
    authentication methods.
    """
    def __init__(self):
        self.user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """ Create a session ID for a user """
        if user_id is None or not isinstance(user_id, str):
            return None

        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ Retrieve a user ID based on a session ID """
        if session_id is None or not isinstance(session_id, str):
            return None

        return self.user_id_by_session_id.get(session_id)

    def session_cookie(self, request=None) -> str:
        """ Retrieve the session ID from the request cookies """
        if request is None:
            return None

        return request.cookies.get(os.getenv('SESSION_NAME'))

    def current_user(self, request=None) -> User:
        """ Retrieve the current authenticated user
        based on session cookie """
        session_id = self.session_cookie(request)
        if session_id is None:
            return None

        user_id = self.user_id_for_session_id(session_id)
        if user_id is None:
            return None

        return User.get(user_id)

    def destroy_session(self, request=None):
        """ Destroy user session / logout """
        if request is None:
            return False

        session_id = self.session_cookie(request)
        if not session_id:
            return False

        user_id = self.user_id_for_session_id(session_id)
        if not user_id:
            return False

        if session_id in self.user_id_by_session_id:
            del self.user_id_by_session_id[session_id]
            return True
        return False
