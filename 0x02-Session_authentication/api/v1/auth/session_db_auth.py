#!/usr/bin/env python3
"""
Session Database Authentication Module

This module provides session-based
authentication with database storage.
"""

from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from flask import request, abort


class SessionDBAuth(SessionExpAuth):
    """
    Session Authentication with Database Storage
    """

    def create_session(self, user_id=None):
        """ Create a session and store it in the database """
        session_id = super().create_session(user_id)
        if session_id:
            new_session = UserSession(user_id=user_id,
                                      session_id=session_id
                                      )
            self._session.add(new_session)
            self._session.commit()
            return session_id
        return None

    def user_id_for_session_id(self, session_id=None):
        """ Retrieve user ID from database for a session ID """
        if session_id is None:
            return None

        session_data = self._session.query(
            UserSession).filter_by(session_id=session_id).first()
        if not session_data:
            return None

        return session_data.user_id

    def destroy_session(self, request=None):
        """ Destroy a session based on the
        session ID from request cookie """
        if request is None:
            return False

        session_id = self.session_cookie(request)
        if not session_id:
            return False

        session_data = self._session.query(UserSession).filter_by(session_id=session_id).first()
        if not session_data:
            return False

        self._session.delete(session_data)
        self._session.commit()
        return True
