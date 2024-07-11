#!/usr/bin/env python3
"""
Authentication module for the API
"""
from flask import request, current_app
from typing import List, TypeVar


class Auth:
    """
    Auth class to manage the API authentication
    """
    def require_auth(self, path: str,
                     excluded_paths: List[str]) -> bool:
        """
        Method to check if authentication is required
        """
        if path is None or excluded_paths is None or not excluded_paths:
            return True

        # Normalize path to ensure it ends with a slash
        if not path.endswith('/'):
            path += '/'

        # Check for wildcard matches at the end of excluded_paths
        for excluded_path in excluded_paths:
            if excluded_path.endswith('*'):
                if path.startswith(excluded_path[:-1]):
                    return False
            elif path == excluded_path:
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """
        Method to get the authorization header from a request
        """
        if request is None or "Authorization" not in request.headers:
            return None

        return request.headers['Authorization']

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Method to get the current user from a request
        """
        return None

    def session_cookie(self, request=None):
        """
        Returns the value of the session cookie named
        as defined by SESSION_NAME.

        Args:
            request (Request): The Flask request object
            containing cookies.

        Returns:
            str: The value of the session cookie if found,
            None otherwise.
        """
        if request is None:
            return None

        session_name = current_app.config.get('SESSION_NAME', '_my_session_id')
        return request.cookies.get(session_name)
