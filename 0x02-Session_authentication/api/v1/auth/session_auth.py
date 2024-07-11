#!/usr/bin/env python3
"""
Session Authentication module for the API.

This module defines the SessionAuth class for handling
session-based authentication.
"""
from api.v1.auth.auth import Auth
import uuid


class SessionAuth(Auth):
    """
    SessionAuth class for session-based auth handling.
    Currently empty, to be expanded for session
    authentication methods.
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        Creates a Session ID for a given user_id and
        stores it in user_id_by_session_id.

        Args:
            user_id (str): The user ID for which to
            create a session.

        Returns:
            str: The generated Session ID if successful,
            None otherwise.
        """
        if user_id is None or not isinstance(user_id, str):
            return None

        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        Retrieves the user ID associated with a given session ID.

        Args:
            session_id (str): The session ID to look up.

        Returns:
            str: The user ID associated with the session ID
            if found, None otherwise.
        """
        if session_id is None or not isinstance(session_id, str):
            return None

        return self.user_id_by_session_id.get(session_id)
