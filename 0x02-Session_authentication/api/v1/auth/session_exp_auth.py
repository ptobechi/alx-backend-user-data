#!/usr/bin/env python3
"""
Session Expiring Authentication Module

This module provides session-based authentication with expiration duration.
"""

from datetime import datetime, timedelta
from api.v1.auth.session_auth import SessionAuth
import os


class SessionExpAuth(SessionAuth):
    """
    Session Authentication with Expiration
    """

    def __init__(self):
        """ Initialize SessionExpAuth """
        super().__init__()
        try:
            self.session_duration = int(
                                        os.getenv("SESSION_DURATION", 0)
                                        )
        except ValueError:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """ Create a Session ID with expiration """
        session_id = super().create_session(user_id)
        if session_id:
            self.user_id_by_session_id[session_id] = {
                'user_id': user_id,
                'created_at': datetime.now()
            }
            return session_id
        return None

    def user_id_for_session_id(self, session_id=None):
        """ Retrieve user ID for a session ID with expiration """
        if session_id is None:
            return None

        session_dict = self.user_id_by_session_id.get(session_id)
        if not session_dict:
            return None

        user_id = session_dict.get('user_id')
        created_at = session_dict.get('created_at')

        if self.session_duration <= 0:
            return user_id

        if not created_at:
            return None

        expiration_time = created_at + timedelta(seconds=self.session_duration)
        if expiration_time < datetime.now():
            return None

        return user_id
